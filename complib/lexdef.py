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
# it can not (will not) report on syntactic anomalies of the target
#  language itself.
# The parser_punique() will let the token receive a new value with
#  every iteration
# Some tokens have no pase entries, these are used on summary output

tokdef = \
         {
         "#define"  : punique(),
         "#undef"   : punique(),
         "#ifdef"   : punique(),
         "#elifdef" : punique(),
         "#else"    : punique(),
         "#endif"   : punique(),
         "#"        : punique(),

         "comma"    : punique(),
         "colon"    : punique(),
         "scolon"    : punique(),
         "num"    : punique(),
         "hex"    : punique(),
         "oct"    : punique(),
         "bin"    : punique(),

         "shex"    : punique(),

         # Basic types
         "char"      : punique(),       # 8
         "short"     : punique(),       # 16
         "int"       : punique(),       # 32
         "long"      : punique(),       # 64

         "uchar"      : punique(),
         "ushort"     : punique(),
         "uint"       : punique(),
         "ulong"      : punique(),

         "S8"        : punique(),       # 8
         "S16"       : punique(),       # 16
         "S32"       : punique(),       # 32
         "S64"       : punique(),       # 64
         "S128"      : punique(),       # 128

         "U8"        : punique(),
         "U16"       : punique(),
         "U32"       : punique(),
         "U64"       : punique(),
         "U128"      : punique(),

         "bs"       : punique(),
         "if"       : punique(),
         "quote"    : punique(),
         "ident"    : punique(),
         "str"      : punique(),
         "str2"     : punique(),
         "str3"     : punique(),
         "str4"     : punique(),
         "strx"     : punique(),
         "comm"     : punique(),
         "eq"       : punique(),
         "lt"       : punique(),
         "gt"       : punique(),
         "sp"       : punique(),
         "lbrack"   : punique(),
         "rbrack"   : punique(),
         "lbrace"   : punique(),
         "rbrace"   : punique(),
         "lcurl"   : punique(),
         "rcurl"   : punique(),
         "tab"      : punique(),
         "tab2"     : punique(),
         "eolnl"    : punique(),
         "nl"       : punique(),
         "n"        : punique(),
         "r"        : punique(),
         "a"        : punique(),
         "0"        : punique(),

         # Fall through
         "anyx"     : punique(),
         "any"      : punique(),
         }

#print("tokdef", tokdef)
rtokdef =  {}
for aa in tokdef:
        rtokdef[tokdef[aa]] = aa

#print("rtokdef", rtokdef)

INI_STATE, STR_STATE, ESC_STATE     = range(3)
STATE_NOCH, STATE_CHG, STATE_DOWN, STATE_ESCD   = range(4)

# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token match.
#
# The order of the definitions matter. First token match is returned.
#
# Elements:
#  ---| parsertate | tokdef | token regex | compiled regex | state change |---
#
# When editing this table, update tokdef and tokens together.

try:
    tokens =  [

    [INI_STATE, tokdef["eolnl"],     "\\\\\n"             ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["bs"],        "\\\\"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["#"],         "#"                  ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["char"],       "char"              ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["short" ],     "short"             ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["int"   ],     "int"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["long"  ],     "long"              ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["uchar" ],     "uchar"             ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["ushort"],     "ushort"            ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["uint"  ],     "uint"              ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["ulong" ],     "ulong"             ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["S8"    ],     "S8"                ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["S16"   ],     "S16"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["S32"   ],     "S32"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["S64"   ],     "S64"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["S128"  ],     "S128"              ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["U8"    ],     "U8"                ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["U16"   ],     "U16"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["U32"   ],     "U32"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["U64"   ],     "U64"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["U128"  ],     "U128"              ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["str4"],      "\#[0-9a-zA-Z]+"     ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["str3"],      "(\\\\[0-7]+)+"      ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["hex"],       "0x[0-9a-fA-F]+"     ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["oct"],       "0o[0-17]+"          ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["bin"],       "0b[0-1]+"           ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["oct"],       "0y[0-17]+"          ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["bin"],       "0z[0-1]+"           ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["num"],       "[0-9]+"             ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["quote"],     "\""                 ,  None, STATE_CHG,  ],
    [INI_STATE, tokdef["str"],       "\".*?\""            ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["str2"],      "\'.*?\'"            ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["ident"],     "[A-Za-z0-9_\-\./]+" ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["comm"],      "\n##.*"             ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["eq"],        "="                  ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["lt"],        "<"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["gt"],        ">"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["sp"],        " "                  ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["nl"],        r"\n"                ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["lbrack"],    "\["                 ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["rbrack"],    "\]"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["lbrace"],    "\("                 ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["rbrace"],    "\)"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["lcurl"],     "\{"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["rcurl"],     "\}"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["comma"],     ","                  ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["colon"],     ";"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["scolon"],    ":"                  ,  None, STATE_NOCH, ],

    [INI_STATE, tokdef["any"],       "."                  ,  None, STATE_NOCH, ],

    # String states
    [STR_STATE, tokdef["bs"],        "\\\\"               ,  None, STATE_CHG, ],
    [STR_STATE, tokdef["quote"],     "\""                 ,  None, STATE_DOWN, ],
    [STR_STATE, tokdef["any"],       "."                  ,  None, STATE_NOCH, ],

    # Escape states
    [ESC_STATE, tokdef["shex"],      "[0-9A-Za-z]+"       ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["n"],         "n"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["r"],         "r"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["a"],         "a"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["0"],         "0"                  ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["quote"],     "\""                 ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["anyx"],       "."                 ,  None, STATE_ESCD, ],
    ]

except:
    print("Cannot precomp", sys.exc_info())
    raise

# EOF
