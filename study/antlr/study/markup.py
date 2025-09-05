#!/usr/bin/env   python3

import sys

from antlr4 import *
from MarkupLexer import MarkupLexer
from MarkupParser import MarkupParser

def main(argv):
    input_stream = InputStream(argv[1])
    lexer = MarkupLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MarkupParser(stream)
    tree = parser.r_file() # Call the root rule
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
