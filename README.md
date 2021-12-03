# pycomp

## Simple py compiler to output assembler for OS construction

Under construction; check back later

pycomp.py: Version 0.1 - Utility for compiling a pcomp file.

```
Usage: pycomp.py [options] filename

  Options are:
            -d level  - Debug level (1-10)
            -o file   - Outfile name
            -e        - Emit parse string
            -V        - Version
            -v        - Verbose
            -s        - Show parser states
            -t        - Show timing
            -x        - Show lexer output
            -p        - Show parser messages
            -h        - Help
```

| File | Description |  Notes |
|--------------|------------|------------|
|Makefile          |Make it here|
|pycomp.py         |main file to drive it|
|README.md         |This file|
|tests             |Directory for syntax tests|
|complib/          |The compiler |
|  -  garbage       |Ignore this|
|  -  lexdef.py     |Lexical definitions| This is the token definition file |
|  -  lexer.py      |Lex parser|
|  -  parsedef.py   |Parser definitions| This is the actual grammer|
|  -  parser.py     |Parser proper|
|  -  stack.py      |Helper stack|
|  -  utils.py      |Helper miscellanea|

