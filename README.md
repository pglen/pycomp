# pyvcomp

## Parallel compiler to output assembler for OS construction

Under construction; check back later (Thu 25.Sep.2025)

   This compiler fills the gap between assembler / c / python. High
level conveniences with the possibility to add low level code.

 Features:

    Only 3 major keywords: "func { }" "loop { }" "if {{ }}".
    Added enter/leave on function level and loop level for cleaner code.

  This parser has limited need for backtracking, as the grammar's concept
is sentence based. The termination of the sentence is either a lexical
completion, a new line or a semi colon.

Example code:

    arr : strx = "Hello World\n"
    printf(strx)

```
PYVCOMP parallel compiler.
Usage: pyvcomp.py [options] filename [filename(s)] ... [options]
Available options:
    -C val  --code val          Code to compile.
    -D val  --define val        Define variable. (multiple defines accepted)
    -H      --help2             Show more help.
    -O val  --outdir val        Directory for out files. Def=./out
    -V      --version           Print version number and build date.
    -c      --comp_only         Compile only.
    -d val  --debug val         Debug level. Def=0 0=>none 9=>noisy.
    -e      --emit              Emit parse string.
    -h      --help              Show help. (this screen)
    -j      --just_lex          Only execute lexer.
    -o val  --outfile val       Name of output file.
    -p      --pre_only          Pre-process only.
    -r      --rdocstr           Show document strings
    -u      --uresults          Show results
    -v      --verbose           Set verbosity level.
    -w val  --workdir val       Directory for temp files. Def=./tmp
    -x      --xlexer_show       Show lexer output
Argument values are identical for the short form and long form options.
Def: stands for default value. Options after file names are also interpreted.
```

| File | Sub | Description |  Notes |
|----- |---------|------------|------------|
|Makefile   |        |Make it here|
|pyvcomp.py |        |Main file |
|README.md  |        |This file|
|examples   |        |Directory for syntax tests|
|complib/   |        |The compiler directory|
|codegen/   |        |The code generation directory|
|docs/      | pcomp_syntax.odt | Language documentation
|  -        | lexdef.py     |Lexical definitions| This is the token definition file |
|  -        | lexer.py      |Lexer code|
|  -        | lindef.py     |Parser definitions| This is the actual grammar|
|  -        | linparse.py   |Parser proper|
|  -        | stack.py      |Helper stack|
|  -        | utils.py      |Helper miscellanea|
|  -        | garbage       |Ignore this -- was for testing / experimenting|

## History:

Wed 16.Jul.2025  Moved from pgpygtk
Thu 18.Sep.2025  Added float, down functions
Thu 25.Sep.2025  Expression parser operational

## Testing:

The testvdrive utility tests functionality on the test / expect basis. A
sample output from the utility below:

Expr1            	 OK
Expr2            	 OK
Expr3            	 OK
Expr4            	 OK
str2             	 OK
str3             	 OK
str4             	 OK

The testvdrive utility is available on pypi.

# EOF
