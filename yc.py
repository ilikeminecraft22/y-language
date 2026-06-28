from tokenizer import tokenize
import sys
import subprocess

# ---------- AST ----------

class Number:
    def __init__(self, value):
        self.value = value


class String:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name

class Binary:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Declare:
    def __init__(self, datatype, name, value):
        self.datatype = datatype
        self.name = name
        self.value = value

class Print:
    def __init__(self, value):
        self.value = value

class Boolean:
    def __init__(self, value):
        self.value = value

class Compare:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class If:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Function:
    def __init__(self, return_type, name, args, body):
        self.return_type = return_type
        self.name = name
        self.args = args
        self.body = body

class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Return:
    def __init__(self, value):
        self.value = value

class CCode:
    def __init__(self, code):
        self.code = code

class Include:
    def __init__(self, name):
        self.name = name


def collect_block(tokens, start):
    body = []
    depth = 0

    i = start

    while i < len(tokens):

        if tokens[i][0] == "LBRACE":
            depth += 1

        elif tokens[i][0] == "RBRACE":
            if depth == 0:
                break
            depth -= 1

        body.append(tokens[i])
        i += 1

    return body, i

# ---------- Parser ----------

def parse_expression(tokens):

    if not tokens:
        raise Exception("Expected expression")

    left = tokens.pop(0)

    if left[0] == "NUMBER":
        node = Number(left[1])

    elif left[0] == "STRING":
        node = String(left[1])

    elif left[0] == "BOOLEAN":
        node = Boolean(left[1])

    elif left[0] == "VARIABLE":

        if not tokens or tokens[0][0] != "IDENTIFIER":
            raise Exception("Expected variable name after '$'")

        node = Variable(tokens.pop(0)[1])

    else:
        raise Exception(f"Unknown expression: {left}")

    while tokens and tokens[0][0] in ("OPERATOR", "COMPARE"):

        op = tokens.pop(0)[1]
        right = parse_expression(tokens)

        if op in ["<", ">", "<=", ">=", "==", "!="]:
            node = Compare(node, op, right)

        else:
            node = Binary(node, op, right)

    return node


def parse(tokens):

    ast = []
    i = 0

    while i < len(tokens):

        token = tokens[i]

        if token[0] == "DECLARE":

            i += 1

            datatype = ""


            if tokens[i][0] == "RAWTYPE":

                i += 1


                while tokens[i][0] != "IDENTIFIER":

                    datatype += tokens[i][1]

                    i += 1


            name = tokens[i][1]


            expr_tokens = []

            i += 2


            while i < len(tokens) and tokens[i][0] != "NLINE":

                expr_tokens.append(tokens[i])

                i += 1


            value = parse_expression(expr_tokens)


            ast.append(
                Declare(datatype, name, value)
            )
        # print(...)
        elif token[0] == "PRINT":

            expr_tokens = []

            i += 2  # skip PRINT (

            while i < len(tokens) and tokens[i][0] != "RPAREN":
                expr_tokens.append(tokens[i])
                i += 1

            value = parse_expression(expr_tokens)

            ast.append(
                Print(value)
            )

            i += 1  # skip RPAREN
        elif token[0] == "VARIABLE":

            name = tokens[i + 1][1]

            expr_tokens = []

            i += 3  # skip $ name =

            while i < len(tokens) and tokens[i][0] != "NLINE":
                expr_tokens.append(tokens[i])
                i += 1

            ast.append(
                Assign(name, parse_expression(expr_tokens))
            )

        elif token[0] == "FUNC":

            i += 1

            return_type = ""


            if tokens[i][0] == "RAWTYPE":

                i += 1

                while tokens[i][0] != "IDENTIFIER":

                    return_type += tokens[i][1]

                    i += 1


            name = tokens[i][1]


            args = []


            i += 2  # skip func type name (


            while tokens[i][0] != "RPAREN":

                if tokens[i][0] == "TYPE":

                    arg_type = tokens[i][1]

                    arg_name = tokens[i + 1][1]


                    args.append(
                        (arg_type, arg_name)
                    )


                    i += 2

                else:
                    i += 1



            i += 2 # skip ) {


            body_tokens = []


            while tokens[i][0] != "RBRACE":

                body_tokens.append(tokens[i])
                i += 1


            body = parse(body_tokens)


            ast.append(
                Function(
                    return_type,
                    name,
                    args,
                    body
                )
            )

        elif token[0] == "RETURN":

            expr_tokens = []

            i += 1

            while tokens[i][0] != "NLINE":
                expr_tokens.append(tokens[i])
                i += 1

            ast.append(
                Return(parse_expression(expr_tokens))
            )

        elif token[0] == "IDENTIFIER" and tokens[i+1][0] == "LPAREN":

            args = []

            i += 2

            expr_tokens = []

            while tokens[i][0] != "RPAREN":

                if tokens[i][0] == "COMMA":

                    args.append(
                        parse_expression(expr_tokens)
                    )

                    expr_tokens = []

                else:
                    expr_tokens.append(tokens[i])

                i += 1


            if expr_tokens:
                args.append(
                    parse_expression(expr_tokens)
                )


            ast.append(
                Call(token[1], args)
            )

        elif token[0] == "WHILE":
            condition_tokens = []

            i += 1

            while tokens[i][0] != "LBRACE":
                condition_tokens.append(tokens[i])
                i += 1


            body_tokens, i = collect_block(tokens, i+1)

            ast.append(
                While(
                    parse_expression(condition_tokens),
                    parse(body_tokens)
                )
            )
        
        elif token[0] == "C_CODE":
            ast.append(
                CCode(token[1])
            )

        elif token[0] == "INCLUDE":

            i += 1

            ast.append(
                Include(tokens[i][1])
            )

        i += 1  # skip NLINE
        
    return ast


# ---------- C generator ----------

def gen_expr(node):

    if isinstance(node, Number):
        return node.value

    if isinstance(node, String):
        return f'"{node.value}"'

    if isinstance(node, Variable):
        return node.name

    if isinstance(node, Boolean):
        return "true" if node.value else "false"

    if isinstance(node, Binary):
        return f"({gen_expr(node.left)} {node.op} {gen_expr(node.right)})"

    if isinstance(node, Compare):
        return f"({gen_expr(node.left)} {node.op} {gen_expr(node.right)})"
    
    if isinstance(node, Call):

        args = ", ".join(
            gen_expr(x)
            for x in node.args
        )

        return f"{node.name}({args})"


def generate_c(ast):

    c = ""

    c += "#include <stdio.h>\n\n"


    for node in ast:

        if isinstance(node, Function):

            args = ", ".join(
                f"{t} {n}"
                for t,n in node.args
            )

            c += f'extern "C" {node.return_type} {node.name}({args}) {{\n'


            for item in node.body:


                if isinstance(item, Print):

                    value = gen_expr(item.value)

                    if isinstance(item.value, String):
                        c += f'    printf("%s", {value});\n'

                    else:
                        c += f'    printf("%d", {value});\n'
                
                elif isinstance(item, CCode):

                    c += f"    {item.code}\n"

                elif isinstance(item, Return):

                    c += f"    return {gen_expr(item.value)};\n"


            c += "}\n\n"



        if isinstance(node, Include):
            c += f'#include {node.name}\n'

        elif isinstance(node, Declare):

            c += (
                f"{node.datatype} {node.name} = "
                f"{gen_expr(node.value)};\n"
            )


        elif isinstance(node, Assign):

            c += (
                f"{node.name} = "
                f"{gen_expr(node.value)};\n"
            )


        elif isinstance(node, Print):

            value = gen_expr(node.value)

            if isinstance(node.value, String):
                c += f'printf("%s", {value});\n'

            else:
                c += f'printf("%d", {value});\n'
        
        elif isinstance(node, While):

            c += f"while({gen_expr(node.condition)}) {{\n"

            for item in node.body:
                c += generate_node(item)

            c += "}\n"

    return c

# ---------- run ----------

if len(sys.argv) < 2:
    print(
        "yc requires 1 or more arguments!\n"
        "usage: yc <option> <filename>\n"
        "open help with yc -h"
    )
    exit(1)


if sys.argv[1] == "-h":

    print("--yc help menu--")
    print(" -h - shows help")
    print(" -b - build object file")
    print(" -e - build executable")
    print(" -c - removes built file")
    print(" -t - prints output in text")
    print(" -d - creates a shared library (.dll/.so)")

    exit(0)


if sys.argv[1] == "-b":

    source = sys.argv[2]
    output = sys.argv[3]

    tokens = tokenize(source)

    ast = parse(tokens)

    c_code = generate_c(ast)


    with open("out.cpp", "w") as outp:
        outp.write(c_code)


    subprocess.run([
        "g++",
        "-c",
        "out.cpp",
        "-o",
        output
    ])


elif sys.argv[1] == "-e":

    source = sys.argv[2]
    output = sys.argv[3]

    tokens = tokenize(source)

    ast = parse(tokens)

    c_code = generate_c(ast)


    with open("out.cpp", "w") as outp:
        outp.write(c_code)


    subprocess.run([
        "g++",
        "out.cpp",
        "-o",
        output
    ])

elif sys.argv[1] == "-d":

    source = sys.argv[2]
    output = sys.argv[3]

    tokens = tokenize(source)

    ast = parse(tokens)

    c_code = generate_c(ast)


    with open("out.cpp", "w") as outp:
        outp.write(c_code)


    if sys.platform == "win32":

        subprocess.run([
            "g++",
            "-shared",
            "out.cpp",
            "-o",
            output + ".dll"
        ])

    else:

        subprocess.run([
            "g++",
            "-fPIC",
            "-shared",
            "out.cpp",
            "-o",
            output + ".so"
        ])

elif sys.argv[1] == "-c":

    subprocess.run([
        "rm",
        "-f",
        "out.cpp"
    ])

elif sys.argv[1] == "-t":
    print(generate_c(parse(tokenize(sys.argv[2]))))