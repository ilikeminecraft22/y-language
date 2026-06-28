# Y Language Syntax

Y is a small systems programming language designed to generate C/C++
code. It focuses on simple syntax while keeping direct access to native
types and C code.

------------------------------------------------------------------------

# Hello World

``` y
func #int main()
{
    print("Hello World!")
    ret 0
}
```

------------------------------------------------------------------------

# Variables

Variables are declared using `~`.

Syntax:

``` y
~#type name = value
```

Example:

``` y
~#int health = 100
~#float speed = 5
```

The type after `#` is passed directly into C/C++.

------------------------------------------------------------------------

# Assignment

Variables can be changed using `$`.

Example:

``` y
~#int health = 100

$health = 50
```

------------------------------------------------------------------------

# Functions

Functions use `func`.

Example:

``` y
func #void load()
{
    print("Loaded")
}
```

Generates:

``` cpp
extern "C" void load()
{
    printf("%s", "Loaded");
}
```

------------------------------------------------------------------------

# Function Arguments

Arguments are typed.

Example:

``` y
func #int add(#int a, #int b)
{
    ret $a + $b
}
```

------------------------------------------------------------------------

# Returning Values

Use `ret`.

Example:

``` y
func #int getHealth()
{
    ret 100
}
```

------------------------------------------------------------------------

# Printing

Use:

``` y
print(value)
```

Example:

``` y
print("Hello")
print(123)
```

------------------------------------------------------------------------

# Operators

Supported:

    +
    -
    *
    /

------------------------------------------------------------------------

# Comparisons

Supported:

    ==
    !=
    <
    >
    <=
    >=

------------------------------------------------------------------------

# While Loops

Syntax:

``` y
while condition
{

}
```

------------------------------------------------------------------------

# Raw C/C++ Code

Y allows direct C/C++ code injection using `%`.

Example:

``` y
%printf("Hello from C");%
```

This is inserted directly into the generated C++.

------------------------------------------------------------------------

# Function Calls

Example:

``` y
load()
```

------------------------------------------------------------------------

# Compiler Modes

## Build Object File

``` bash
yc -b program.y program.o
```

## Build Executable

``` bash
yc -e program.y program
```

## Build Dynamic Library

``` bash
yc -d mod.y mod
```

Creates:

Linux:

    mod.so

Windows:

    mod.dll

------------------------------------------------------------------------

# Design Philosophy

Y is not designed to replace C or C++.

It is a cleaner syntax layer for making native programs, plugins, mods,
and libraries while keeping compatibility with existing C/C++ code.
