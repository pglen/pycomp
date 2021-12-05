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

tokdef = \
         {
         "#define"  : punique(),
         "#undef"   : punique(),
         "#ifdef"   : punique(),
         "#elifdef" : punique(),
         "#else"    : punique(),
         "#endif"   : punique(),
         "#"        : punique(),
         "bs"        : punique(),
         "if"       : punique(),
         "quote"    : punique(),
         "ident"    : punique(),
         "str"      : punique(),
         "str2"     : punique(),
         "str3"     : punique(),
         "str4"     : punique(),
         "comm"     : punique(),
         "eq"       : punique(),
         "lt"       : punique(),
         "gt"       : punique(),
         "sp"       : punique(),
         "tab"      : punique(),
         "tab2"     : punique(),
         "eolnl"    : punique(),
         "nl"       : punique(),
         "n"        : punique(),
         "r"        : punique(),
         "0"        : punique(),

         # Fall through
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
# Lexer tokens. The lexer will search for the next token.
# When editing, update tokdef and tokens together.
#
# The order of the definitions matter. First token match is returned.
#
# Elements:
#  --- enum parstate - tokdef - token regex - compiled regex --

tokens =  [

    [INI_STATE, tokdef["eolnl"],     "\\\\\n"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["bs"],        "\\\\"                 ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["#"],         "#"                    ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["ident"],     "[A-Za-z0-9_\-\./]+"   ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["str4"],      "\#[0-9a-zA-Z]+"       ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["str3"],      "(\\\\[0-7]+)+"        ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["quote"],     "\""                   ,  None, STATE_CHG,  ],
    [INI_STATE, tokdef["str"],       "\".*?\""              ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["str2"],      "\'.*?\'"              ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["comm"],      "\n##.*"               ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["eq"],        "="                    ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["lt"],        "<"                    ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["gt"],        ">"                    ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["sp"],        " "                    ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["nl"],        r"\n"                  ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["any"],       "a"                    ,  None, STATE_NOCH, ],
    [INI_STATE, tokdef["any"],       "."                    ,  None, STATE_NOCH, ],

    # String state
    [STR_STATE, tokdef["bs"],        "\\\\"                 ,  None, STATE_CHG, ],
    [STR_STATE, tokdef["quote"],     "\""                   ,  None, STATE_DOWN, ],
    [STR_STATE, tokdef["any"],       "."                    ,  None, STATE_NOCH, ],

    # Escape state
    [ESC_STATE, tokdef["quote"],       "\""                 ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["n"],         "n"                    ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["r"],         "r"                    ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["0"],         "0"                    ,  None, STATE_ESCD, ],
    [ESC_STATE, tokdef["any"],       "."                    ,  None, STATE_NOCH, ],

    ]

# EOF
