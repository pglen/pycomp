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
         "if"       : punique(),
         "public"   : punique(),
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
         "nl"       : punique(),
         "any"      : punique(),
         }

#print("tokdef", tokdef)
#rtokdef =  {}
#for aa in tokdef:
#    rtokdef[tokdef[aa]] = aa
#print("rtokdef", rtokdef)

INI_STATE, STR_STATE, SOME_STATE = range(3)

# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token.
# When editing, update tokdef and tokens together.
#
# The order of the definitions matter. First token match is returned.
#
# Please note for simplicity we defined a stateless lexer. For example,
# the str is delimited by "" and str2 is delimited by '' to allow
# quotes in the str. For more complex string with quotes in it, escape
# the quotes. (\48)
#
# Elements:
#  --- enum parstate - tokdef - token regex - compiled regex --

tokens =  [
    [INI_STATE, tokdef["#"],         "#"             ,      None  ],
    [INI_STATE, tokdef["ident"],     "[A-Za-z0-9_\-\./]+",  None, ],
    [INI_STATE, tokdef["str4"],      "\#[0-9a-zA-Z]+",      None, ],
    [INI_STATE, tokdef["str3"],      "(\\\\[0-7]+)+",       None, ],
    [INI_STATE, tokdef["str"],       "\".*?\""       ,      None, ],
    [INI_STATE, tokdef["str2"],      "\'.*?\'"       ,      None, ],
    [INI_STATE, tokdef["comm"],      "\n##.*"          ,    None, ],
    [INI_STATE, tokdef["eq"],        "="             ,      None, ],
    [INI_STATE, tokdef["lt"],        "<"             ,      None, ],
    [INI_STATE, tokdef["gt"],        ">"             ,      None, ],
    [INI_STATE, tokdef["sp"],        " "             ,      None, ],
    [INI_STATE, tokdef["nl"],        r"\n"            ,     None, ],
    [INI_STATE, tokdef["any"],       "."             ,      None, ],
    ]

# EOF




