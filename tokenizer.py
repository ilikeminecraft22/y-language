def tokenize(fname):
    tokens = []

    with open(fname, "r") as code:
        for line_num, line in enumerate(code, 1):

            line = line.strip()

            if not line:
                continue

            i = 0

            while i < len(line):

                char = line[i]


                if char == "~":
                    tokens.append(("DECLARE", "~"))
                    i += 1


                elif char == "$":
                    tokens.append(("VARIABLE", "$"))
                    i += 1

                elif line.startswith("==", i):
                    tokens.append(("COMPARE", "=="))
                    i += 2

                elif line.startswith("!=", i):
                    tokens.append(("COMPARE", "!="))
                    i += 2

                elif line.startswith("<=", i):
                    tokens.append(("COMPARE", "<="))
                    i += 2

                elif line.startswith(">=", i):
                    tokens.append(("COMPARE", ">="))
                    i += 2

                elif char == "<":
                    tokens.append(("COMPARE", "<"))
                    i += 1

                elif char == ">":
                    tokens.append(("COMPARE", ">"))
                    i += 1

                elif char == "=":
                    tokens.append(("ASSIGN", "="))
                    i += 1

                elif char in "+-/":
                    tokens.append(("OPERATOR", char))
                    i += 1
                
                elif char == "*":
                    tokens.append(("STAR", "*"))
                    i += 1
                
                elif char == "#":
                    tokens.append(("RAWTYPE", "#"))
                    i += 1

                elif char == "{":
                    tokens.append(("LBRACE", "{"))
                    i += 1

                elif char == "}":
                    tokens.append(("RBRACE", "}"))
                    i += 1

                elif char == ",":
                    tokens.append(("COMMA", ","))
                    i += 1

                elif char.isdigit():

                    number = ""

                    while i < len(line) and line[i].isdigit():
                        number += line[i]
                        i += 1

                    tokens.append(("NUMBER", number))


                elif char == '"':

                    string = ""
                    i += 1

                    while i < len(line) and line[i] != '"':
                        string += line[i]
                        i += 1

                    tokens.append(("STRING", string))
                    i += 1


                elif char == "(":
                    tokens.append(("LPAREN", "("))
                    i += 1


                elif char == ")":
                    tokens.append(("RPAREN", ")"))
                    i += 1

                elif char == "#":
                    tokens.append(("RAWTYPE", "#"))
                    i += 1

                elif char == "%":

                    code = ""
                    i += 1

                    while i < len(line) and line[i] != "%":
                        code += line[i]
                        i += 1

                    tokens.append(("C_CODE", code))
                    i += 1

                elif char.isalpha() or char == "_":

                    name = ""

                    while i < len(line) and (line[i].isalnum() or line[i] == "_"):
                        name += line[i]
                        i += 1


                    if name == "print":
                        tokens.append(("PRINT", name))

                    elif name == "true":
                        tokens.append(("BOOLEAN", True))

                    elif name == "false":
                        tokens.append(("BOOLEAN", False))

                    elif name == "func":
                        tokens.append(("FUNC", name))

                    elif name == "ret":
                        tokens.append(("RETURN", name))

                    elif name == "while":
                        tokens.append(("WHILE", name))

                    elif name in ["int", "float", "char", "bool"]:
                        tokens.append(("TYPE", name))

                    elif name == "load":
                        tokens.append(("INCLUDE", name))

                    else:
                        tokens.append(("IDENTIFIER", name))


                else:
                    i += 1


            tokens.append(("NLINE", "\n"))


    return tokens