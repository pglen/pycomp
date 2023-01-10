#!/usr/bin/env python3

''' This is a parser skeleton for language development
        This file defines the tokens and parser states
'''

#from __future__ import absolute_import
from __future__ import print_function

from complib.utils import *

'''
# We initialize parser variables in the context of the parser module.
#
# a.) Token definitions, b.) Lexer tokens,
# c.) Parser functions,  d.) Parser state, e.) Parse table
#
# To create a custom parser, just add new tokens / states
#

# Quick into: The lexer creates a stack of tokens. The parser scans
# the tokens, and walks the state machine for matches. If match
# is encountered, the parser calls the function in the state table,
# and / or changes state. Reduce is called after the state has been
# successfully digested. For more info see lex / yacc literature.
'''

tok2 = {}

# ------------------------------------------------------------------------
# Token definitions:
#
# [ Use textual context nn[idx][1] for development, numeric nn[idx][0]
# for production.]
#
# The order of the definitions do not matter.
#
# To add a new syntactic element, search for an existing feature (like 'wrap')
# Add the new element into the a.) definition, b.) regex defintion,
# c.) state definition, d.) state table, e.) action function. (ouch)
#
# The script is self checking, will report on missing defintions. However,
#   it can not (will not) report on syntactic anomalies of the target
#   language itself.
# The punique() routine will let the token receive a new value with
#   every iteration
# Some tokens have no pase entries, these are used on summary output

# Create token on the fly, if there is one already, return it.

def tok(name):
    if name in tok2:
        #print("Warn: dup token", name)
        pass
    else:
        tok2[name] = punique()
    return tok2[name]

INI_STATE, STR_STATE, ESC_STATE     = range(3)
STATE_NOCH, STATE_CHG, STATE_DOWN, STATE_ESCD   = range(4)

# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token match.
#
# The order of the definitions matter. First token match is returned.
#
# Elements:
#  ---| parsertate | tok | token regex | compiled regex | state change |---
#
# When editing this table, update tok and tokens together.

try:
    tokens =  [

    [INI_STATE, tok("eolnl"),     "\\\\\n"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("bsl"),        "\\\\"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("ifdef"),     "#ifdef"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("define"),    "#define"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("else2"),     "#else"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("endif2"),    "#endif"             ,  None, STATE_NOCH, ],

    [INI_STATE, tok("#"),         "#"                  ,  None, STATE_NOCH, ],

    [INI_STATE, tok("endif"),      "endif"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("if"),         "if"                ,  None, STATE_NOCH, ],

    [INI_STATE, tok("char"),       "char"              ,  None, STATE_NOCH, ],
    [INI_STATE, tok("short" ),     "short"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("int"   ),     "int"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("long"  ),     "long"              ,  None, STATE_NOCH, ],
    [INI_STATE, tok("uchar" ),     "uchar"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("ushort"),     "ushort"            ,  None, STATE_NOCH, ],
    [INI_STATE, tok("uint"  ),     "uint"              ,  None, STATE_NOCH, ],
    [INI_STATE, tok("ulong" ),     "ulong"             ,  None, STATE_NOCH, ],
    [INI_STATE, tok("S8"    ),     "S8"                ,  None, STATE_NOCH, ],
    [INI_STATE, tok("S16"   ),     "S16"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("S32"   ),     "S32"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("S64"   ),     "S64"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("S128"  ),     "S128"              ,  None, STATE_NOCH, ],
    [INI_STATE, tok("U8"    ),     "U8"                ,  None, STATE_NOCH, ],
    [INI_STATE, tok("U16"   ),     "U16"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("U32"   ),     "U32"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("U64"   ),     "U64"               ,  None, STATE_NOCH, ],
    [INI_STATE, tok("U128"  ),     "U128"              ,  None, STATE_NOCH, ],

    [INI_STATE, tok("str4"),      "\#[0-9a-zA-Z]"     ,  None, STATE_NOCH, ],
    [INI_STATE, tok("str3"),      "(\\\\[0-7]+)+"      ,  None, STATE_NOCH, ],

    [INI_STATE, tok("hex"),       "0x[0-9a-fA-F]+"     ,  None, STATE_NOCH, ],
    [INI_STATE, tok("oct"),       "0o[0-17]+"          ,  None, STATE_NOCH, ],
    [INI_STATE, tok("bin"),       "0b[0-1]+"           ,  None, STATE_NOCH, ],
    [INI_STATE, tok("oct2"),       "0y[0-17]+"          ,  None, STATE_NOCH, ],
    [INI_STATE, tok("bin2"),       "0z[0-1]+"           ,  None, STATE_NOCH, ],

    [INI_STATE, tok("num"),       "[0-9]+"             ,  None, STATE_NOCH, ],

    [INI_STATE, tok("quote"),     "\""                 ,  None, STATE_CHG,  ],
    [INI_STATE, tok("str"),       "\".*?\""            ,  None, STATE_NOCH, ],
    [INI_STATE, tok("str2"),      "\'.*?\'"            ,  None, STATE_NOCH, ],
    [INI_STATE, tok("ident"),     "[A-Za-z0-9_\-\./]+" ,  None, STATE_NOCH, ],

    [INI_STATE, tok("comm"),      "\n##.*"             ,  None, STATE_NOCH, ],

    [INI_STATE, tok("peq"),       "\+="                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("meq"),       "\-="                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("deq"),       "=="                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("put"),       "=>"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("dref"),      "->"                 ,  None, STATE_NOCH, ],

    [INI_STATE, tok("at"),        "@"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("exc"),       "!"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("tilde"),     "~"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("under"),     "_"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("eq"),        "="                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("lt"),        "<"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("gt"),        ">"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("and"),       "&"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("star"),      "\*"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("caret"),     "^"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("perc"),      "%"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("div"),       "/"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("sp"),        " +"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("nl"),        r"\n"                ,  None, STATE_NOCH, ],
    [INI_STATE, tok("lbrack"),    "\["                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("rbrack"),    "\]"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("lbrace"),    "\("                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("rbrace"),    "\)"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("lcurl"),     "\{"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("rcurl"),     "\}"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tok("comma"),     ","                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("colon"),     ";"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tok("scolon"),    ":"                  ,  None, STATE_NOCH, ],

    [INI_STATE, tok("any"),       "."                  ,  None, STATE_NOCH, ],

    # String states
    [STR_STATE, tok("bsl"),       "\\\\"               ,  None, STATE_CHG, ],
    [STR_STATE, tok("quote"),     "\""                 ,  None, STATE_DOWN, ],
    [STR_STATE, tok("any"),       "."                  ,  None, STATE_NOCH, ],

    # Escape states
    [ESC_STATE, tok("shex"),      "[0-9A-Za-z]+"       ,  None, STATE_ESCD, ],
    [ESC_STATE, tok("n"),         "n"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tok("r"),         "r"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tok("a"),         "a"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tok("0"),         "0"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tok("quote"),     "\""                 ,  None, STATE_ESCD, ],
    [ESC_STATE, tok("anyx"),       "."                 ,  None, STATE_ESCD, ],
    ]

except KeyError as err:
    print("Cannot precomp", err, sys.exc_info())
    raise

#print("tok2", tok2)

rtok =  {}
for aa in tok2:
    rtok[tok2[aa]] = aa

#print("rtok", rtok)

# EOF
