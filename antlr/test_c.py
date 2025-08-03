#!/usr/bin/env   python3

import sys

from antlr4 import *
from tmp.CLexer import CLexer
from tmp.CParser import CParser

def main(argv):
    input_stream = InputStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.primaryExpression() # Call the root rule
    print("\ntree:", tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
