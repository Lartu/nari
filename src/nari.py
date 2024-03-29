import sys
import math
import readline

# constants
VERSION = "@MAYORVERSION"
COMMIT = "@COMMITVERSION"

# global variables
stack = []
variables = {}
aux = {}
printedSomething = False
lineNumber = 1
interactiveMode = False

def versionInfo():
    print(f"\n This is \033[1;33mNari {VERSION}.{COMMIT}\033[0m. Squeak!")
    print(f" Copyright 2016 - 2019, \033[1;35mMartín del Río\033[0m (www.lartu.net).")

def startInteractiveMode():
    global interactiveMode
    interactiveMode = True
    versionInfo()
    print("")
    while True:
        try:
            line = input("\033[1;31m>\033[1;33m>\033[1;32m>\033[0m ")
        except KeyboardInterrupt:
            print(f"\nPlease enter \033[1;35mquit\033[0m to exit.")
        except:
            print("\nPlease try again.")
        try:
            runCode(line)
        except KeyboardInterrupt:
            print(f" Interrupted. Please enter \033[1;35mquit\033[0m to exit.\n")
        except SystemExit:
            raise
        except BaseException as e:
            #print(e)
            pass
    quit(0)

def displayDocsInfo():
    print(" Complete documentation for Nari should be found on this system")
    print(" using \033[1;35m'man nari'\033[0m. If you have access to the internet, the")
    print(" documentation can also be found online at \033[1;33mgithub.com/lartu/nari/docs\033[0m.")

def evaluateParameters():
    # If we have less than 2 parameters, then the user just ran 'nari'
    if len(sys.argv) < 2:
        startInteractiveMode()
    else:
        # Evaluate each parameter passed
        for arg in sys.argv:
            if arg == "-h" or arg == "--help":
                print("\n \033[1;33mUsage:\033[0m")
                print("    nari")
                print("    nari <filename>|-c")
                print("    nari -v|-h")
                print("\n \033[1;33mOptions:\033[0m")
                print("    -v --version         Display Nari version information")
                print("    -h --help            Display this information")
                print("    -c                   Read source from standard input\n")
                displayDocsInfo()
                print("")
                quit(0)
            elif arg == "-v" or arg == "--version":
                versionInfo()
                print("\n The source for Nari is available at \033[1;33mwww.github.com/lartu/nari\033[0m.")
                displayDocsInfo()
                print("\n Nari may be copied only under the terms of the GNU General")
                print(" Public License 3.0, which may be found in the Nari repository.")
                print("\n Compiled on \033[1;35m@COMPILEDATE\033[0m at \033[1;35m@COMPILEHOUR\033[0m.\n")
                quit(0)
            elif arg == "-c": # Read from command line
                sourceFile = None
            else:
                sourceFile = arg
        # If no source file was provided
        if sourceFile == "":
            throwError("Please provide a valid source file.")
        return sourceFile

def loadSourceFile(sourceFile):
    if sourceFile == None:
        sourceCode = ""
        for line in sys.stdin:
            sourceCode += line
        return sourceCode
    else:
        try:
            sourceCode = open(sourceFile, "r").read()
            return sourceCode
        except:
            throwError(f"Error loading file '{sourceFile}'.")

def splitTokens(sourceCode):
    tokens = []
    currentToken = ""
    inString = False
    inComment = False
    inBlock = True
    escapingCharacter = False
    lineNumber = 1
    for c in sourceCode:
        if not(inString) and c == "#":
            inComment = not(inComment)
        elif inComment:
            continue
        elif not(inString) and not(inComment) and (c.isspace() or c == "]"):
            currentToken = currentToken.strip()
            if len(currentToken) > 0:
                tokens.append(currentToken)
            currentToken = ""
            if c == "\n":
                lineNumber += 1
            elif c == "]":
                tokens.append("]")
        elif c == '"' and not(escapingCharacter):
            inString = not(inString)
            currentToken += c
        elif c == '\\':
            if inString:
                escapingCharacter = True
            else:
                throwError(f"escape sequence found outside string.")
        elif escapingCharacter:
            if c == '"' or c == "\\":
                currentToken += c
            elif c == "n":
                currentToken += "\n"
            elif c == "r":
                currentToken += "\r"
            elif c == "t":
                currentToken += "\t"
            else:
                throwError(f"unknown escape sequence \\{c}.")
            escapingCharacter = False
        elif c == "[" and not(inString):
            tokens.append("[")
        else:
            currentToken += c
    if inString:
        throwError(f"a string has not been properly closed.")
    return tokens

def isNumber(val):
    try:
        val = float(val)
        return True   
    except ValueError:
        return False

def lexTokens(tokens, _from=0):
    # Token types:
    # 0 - string
    # 1 - number
    # 2 - statement
    # 3 - 
    # 4 - variable ticket
    # 5 - auxiliar function
    # 6 - list
    # 7 - map
    # 8 - null
    # 9 - block
    tokenList = []
    inBlock = 0;
    i = _from
    while i < len(tokens):
        token = tokens[i]
        if token == "]":
            inBlock -= 1
            if inBlock < 0:
                break
        if inBlock == 0:
            if token[0] == '"':
                tokenList.append((token[1:-1], 0))
            elif token[0] == '@':
                tokenList.append((token, 4))
            elif isNumber(token):
                tokenList.append((float(token), 1))
            elif token[0] == "[":
                tokenList.append((lexTokens(tokens, i + 1), 9))
            elif token[0] != "]":
                tokenList.append((token, 2))
        if token == "[":
            inBlock += 1
        i += 1
    if i == len(tokens) and inBlock != 0:
        throwError(f"a block has not been properly closed.");
    return tokenList

def throwError(msg):
    if printedSomething:
        print("")
    print(f"Error: {msg}");
    if interactiveMode:
        raise Exception('Interactive Error')
    else:
        quit(1)

def popStack(command):
    global stack
    if len(stack) > 0:
        return stack.pop()
    else:
        throwError(f"empty stack when trying to execute {command}.");

def getVar(token):
    if token[0] in variables:
        return variables[token[0]]
    else:
        return ("", 8)

def nariPrint(token, notTuple = False):
    # Printing numbers
    if token[1] == 1:
        print(('%.15f' % token[0]).rstrip('0').rstrip('.'), end = '')
    # Print list
    elif token[1] == 6:
        print("(", end = '')
        for i in range(0, len(token[0])):
            nariPrint(token[0][i])
            if i < len(token[0])-1:
                print(", ", end = '')
        print(")", end = '')
    # Printing everything else
    else:
        print(token[0], end = '')

def nariJoin(a, b, lineNumber):
    # Get variable values from tickets
    if a[1] == 4:
        a = getVar(a)
    if b[1] == 4:
        b = getVar(b)
    # Join strings and numbers
    if (a[1] == 0 or a[0] == 1)  and (b[1] == 0 or b[1] == 1):
        return (str(b[0]) + str(a[0]), 0)
    else:
        throwError(f"trying to join incompatible types.")

def getNextToken(tokens, i, skip):
    while i < len(tokens):
        if skip == 0:
            return tokens[i]
        if tokens[i][1] != 3:
            skip -= 1
        i += 1

def execute(tokens):
    global stack
    global variables
    global printedSomething
    global lineNumber
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t[1] == 0 or t[1] == 1 or t[1] == 4: # Number, Strings or variable tickets
            stack.append(t)
        elif t[1] == 9: # Blocks
            execute(t[0])
        elif t[1] == 2: # Statements
            if t[0] == "print":
                nariPrint(popStack(t[0]))
                printedSomething = True
            elif t[0] == "join":
                stack.append(nariJoin(popStack(t[0]), popStack(t[0]), lineNumber))
            elif t[0] == "+":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != 1 or a[1] != 1:
                    throwError(f"trying to add non-numeric values.")
                else:
                    stack.append((a[0] + b[0], 1))
            elif t[0] == "-":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != 1 or a[1] != 1:
                    throwError(f"trying to subtract non-numeric values.")
                else:
                    stack.append((b[0] - a[0], 1))
            elif t[0] == "*":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != 1 or a[1] != 1:
                    throwError(f"trying to multiply non-numeric values.")
                else:
                    stack.append((a[0] * b[0], 1))
            elif t[0] == "/":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != 1 or a[1] != 1:
                    throwError(f"trying to divide non-numeric values.")
                else:
                    stack.append((b[0] / a[0], 1))
            elif t[0] == "%":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != 1 or a[1] != 1:
                    throwError(f"trying to modulo non-numeric values.")
                else:
                    stack.append((float(int(b[0]) % int(a[0])), 1))
            elif t[0] == "copy":
                if len(stack) == 0:
                    throwError(f"empty stack when trying to copy")
                stack.append((stack[len(stack)-1][0], stack[len(stack)-1][1]))
            elif t[0] == "del":
                popStack(t[0])
            elif t[0] == "=":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != b[1] or a[0] != b[0]:
                    stack.append((0, 1))
                else:
                    if a[1] == 1:
                        if math.isclose(a[0], b[0], rel_tol=1e-6):
                            stack.append((1, 1))
                        else:
                            stack.append((0, 1))
                    elif a[0] == b[0]:
                        stack.append((1, 1))
                    else:
                        stack.append((0, 1))
            elif t[0] == "<":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != b[1] or (a[1] != 0 and a[1] != 1):
                     throwError(f"trying to compare order of invalid values.")
                elif b[0] < a[0]:
                    stack.append((1, 1))
                else:
                    stack.append((0, 1))
            elif t[0] == "while":
                if i + 2 == len(tokens) or getNextToken(tokens, i, 1)[1] != 9 or getNextToken(tokens, i, 2)[1] != 9:
                    throwError(f"two blocks expected after while.")
                while True:
                    execute(getNextToken(tokens, i, 1)[0])
                    guard = popStack(t[0])
                    if guard[1] != 1:
                        throwError(f"while guard is not a number.")
                    elif math.isclose(guard[0], 0, rel_tol=1e-6):
                        break
                    else:
                        execute(getNextToken(tokens, i, 2)[0])
                i += 2
            elif t[0] == "if":
                if i + 2 == len(tokens) or getNextToken(tokens, i, 1)[1] != 9 or getNextToken(tokens, i, 2)[1] != 9:
                    throwError(f"two blocks expected after if.")
                execute(getNextToken(tokens, i, 1)[0])
                guard = popStack(t[0])
                guardIsTrue = not(math.isclose(guard[0], 0, rel_tol=1e-6))
                hasElse = (i + 4 < len(tokens) and getNextToken(tokens, i, 3)[1] == 2 and getNextToken(tokens, i, 3)[0] == "else")
                if guard[1] != 1:
                    throwError(f"if guard is not a number.")
                elif guardIsTrue:
                    execute(getNextToken(tokens, i, 2)[0])
                elif hasElse: #else
                    if getNextToken(tokens, i, 4)[1] == 9:
                        execute(getNextToken(tokens, i, 4)[0])
                    else:
                        throwError(f"block expected after else of if stated.")
                if hasElse:
                    i += 4
                else:
                    i += 2
            elif t[0] == "aux":
                if i + 2 >= len(tokens) or getNextToken(tokens, i, 1)[1] != 2 or getNextToken(tokens, i, 2)[1] != 9:
                    throwError(f"name and block expected after aux.")
                aux[getNextToken(tokens, i, 1)[0]] = getNextToken(tokens, i, 2)[0]
                i += 2
            elif t[0] == "return":
                return
            elif t[0] == "quit":
                quit(0)
            elif t[0] == "input":
                try:
                    value = input()
                    stack.append((value, 0))
                except:
                    throwError(f"input error.")
            elif t[0] == "tonum": # Should be moved into a library TODO
                a = popStack(t[0])
                if a[1] != 0:
                    throwError(f"cannot cast non-string value to number.")
                try:
                    stack.append((float(a[0]), 1))
                except:
                    throwError(f"cannot cast value to number.")
            elif t[0] == "isnum": # Should be moved into a library TODO
                a = popStack(t[0])
                if a[1] != 0:
                    throwError(f"cannot check if non-string value is numeric.")
                if(isNumber(a[0])):
                    stack.append((1, 1))
                else:
                    stack.append((0, 1))
            elif t[0] == "at":
                a = popStack(t[0])
                b = popStack(t[0])
                if not(a[1] == 1 and (b[1] == 0 or b[1] == 6)) and not((a[1] == 1 or a[1] == 0) and b[1] == 7):
                    throwError(f"trying to access an index of an element that is neither a string nor a list nor a map.")
                elif b[1] == 7:
                    if a[0] in b[0]:
                        stack.append(b[0][a[0]])
                    else:
                        throwError(f"map has no key called {a[0]}.")
                else:
                    stack.append(b[0][int(a[0])])
            elif t[0] == "size":
                b = popStack(t[0])
                if b[1] != 0 and b[1] != 6 and b[1] != 7:
                    throwError(f"trying to get length of an element that is neither a string nor a list nor a map.")
                else:
                    stack.append((len(b[0]), 1))
            elif t[0] == "remove":
                a = popStack(t[0])
                b = popStack(t[0])
                if not(a[1] == 1 and b[1] == 6) and not((a[1] == 1 or a[1] == 0) and b[1] == 7):
                    throwError(f"trying to remove an index of an element that is not a list nor a map.")
                elif b[1] == 7:
                    if a[0] in b[0]:
                        b[0].pop(a[0])
                    else:
                        throwError(f"map has no key called {a[0]}.")                
                else:
                    b[0].pop(int(a[0]))
                stack.append((b[0], b[1]))
            elif t[0] == "()":
                stack.append(([], 6))
            elif t[0] == "{}":
                stack.append(({}, 7))
            elif t[0] == "push":
                a = popStack(t[0])
                b = popStack(t[0])
                if b[1] != 6:
                    throwError(f"cannot push to non-list.")
                else:
                    b[0].append(a)
                    stack.append((b[0], 6))
            elif t[0] == "scribe":
                b = popStack(t[0])
                a = popStack(t[0])
                c = popStack(t[0])
                if c[1] != 7:
                    throwError(f"cannot scribe to non-map.")
                if b[1] != 0 and b[1] != 1:
                    throwError(f"cannot scribe to non-numeric or non-string keys.")
                else:
                    c[0][b[0]] = a
                    stack.append((c[0], 7))
            elif t[0] == "set":
                a = popStack(t[0])
                b = popStack(t[0])
                if a[1] != 4:
                    throwError(f"cannot set to non-variable-ticket.")
                else:
                    variables[a[0]] = b
            elif t[0] == "get":
                a = popStack(t[0])
                if a[1] != 4:
                    throwError(f"cannot set to non-variable-ticket.")
                else:
                    stack.append(variables[a[0]])
            else: # If its not a known statement then it is an auxiliar function
                if t[0] in aux:
                    execute(aux[t[0]])
                else:
                    throwError(f"unknown function {t[0]} called.")
        i += 1

def runCode(sourceCode):
    tokens = splitTokens(sourceCode + " ")
    tokens = lexTokens(tokens)
    execute(tokens)

def main():
    try:
        sourceFile = evaluateParameters()
        sourceCode = loadSourceFile(sourceFile)
        runCode(sourceCode)
        quit(0)
    except KeyboardInterrupt:
        quit(0)

# Execute Nari
main()
