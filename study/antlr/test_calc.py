#!/usr/bin/env   python3

import sys

from antlr4 import *
from tmp.calcLexer import calcLexer
from tmp.calcParser import calcParser
from tmp.calcVisitor import calcVisitor

def main(arg):
    #input_stream = InputStream(argv[1])
    input_stream = InputStream(arg)
    lexer = calcLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = calcParser(stream)
    tree = parser.equation() # Call the root rule
    #print("\ntree:", tree.toStringTree(recog=parser))
    visitor = calcVisitor()
    return visitor.visit(tree)

if __name__ == '__main__':

     while True:
        print(">>> ", end='')
        line = input()
        print(main(line))
