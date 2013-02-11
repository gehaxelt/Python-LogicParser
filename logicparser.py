#!/usr/bin/python2.7
import sys

#Returns the first token and the rest list
def getToken(tokens):
    if len(tokens) > 0:
        token = tokens[0]
        del tokens[0]
        return [token,tokens]
    else:
        return ["error_end",[]]

#Scan Tokens
def scan(input):
    expanded_input = input.replace('(', ' ( ').replace(')', ' ) ')
    tokens = expanded_input.split()
    return tokens
    
#Parses and, or
def parseOperator(tokens):
    token, tokens = getToken(tokens)
    if token == "and":
        return ["and",tokens]
    elif token == "or":
        return ["or",tokens]
    elif token == "->":
        return ["->",tokens]
    elif token == "<->":
        return ["<->",tokens]
    elif token == "xor":
        return ["xor",tokens]
    else:
        return ["error",tokens]

# Parses close
def parseClose(tokens):
    token, tokens = getToken(tokens)
    if token == ")":
        return ["",tokens]
    else:
        return ["error",tokens]

#Parses an expression
def parseExpr(tokens):
    token, tokens = getToken(tokens)
    if token == "T":
        return ["T",tokens]
    elif token == "F":
        return ["F",tokens]
    elif token == "not":
        exp1, rest1 = parseExpr(tokens)
        return [["not",exp1],rest1]
    elif token == "(":
        exp1, rest1     = parseExpr(tokens)
        operator, rest2 = parseOperator(rest1)
        exp2, rest3     = parseExpr(rest2)
        exp4,rest4      = parseClose(rest3)
        if exp4 == "error":
            return ["error_close",[]]
        return [[operator,exp1,exp2],rest4]
    else:
        ["error_end",[]]  

#Parse tokens
def parse(tokens):
    try: 
    
        expr, rest = parseExpr(tokens)

        if len(rest) > 0 or (expr == "error"):
            return "error"
        return expr
    except:
        return "Parsing error"

#Evaluate logic expression
def logiceval(expr):
    try:
        if "Error" in expr:
            return "Syntaxfehler"
        token, tokens = getToken(expr)

        if token == "T":
            return True
        elif token == "F":
            return False
        elif token == "not":
            return not logiceval(getToken(tokens))
        elif token == "and":
            return logiceval(getToken(tokens)) and logiceval(getToken(getToken(tokens)))
        elif token == "or":
            return logiceval(getToken(tokens)) or logiceval(getToken(getToken(tokens)))
        elif token == "->":
            left = logiceval(getToken(tokens))
            if left:
                return False
            else:
                return True 
        elif token == "<->":
            left = logiceval(getToken(tokens))
            right = logiceval(getToken(getToken(tokens)))
            if (left and right) or (not left and not right):
                return True
            else:
                return False
        elif token == "xor":
            left = logiceval(getToken(tokens))
            right = logiceval(getToken(getToken(tokens)))
            if (left and not right) or (not left and right):
                return True
            else:
                return False
        else:
            return "error"
    except:
        return "Evaluation error"
        
#Main function
def main():
    if len(sys.argv) > 1:
        userinput = sys.argv[1]
    else:
        userinput = raw_input("Logic term: ")
    print logiceval(parse(scan(userinput)))

main()
