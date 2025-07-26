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
# c.) Parser functions, d.) Parser state, e.) Parse table
#
# To create a custom parser, just add new tokens / states here
#

# Quick into: The lexer creates a stack of tokens. The parser scans
# the tokens, and walks the state machine for matches. If match
# is encountered, the parser calls the function in the state table,
# and / or changes state. Reduce is called after the state has been
# successfully digested. For more info see lex / yacc literature.
'''

tok2 = {}; tok3 = {}

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

INI_STATE, STR_STATE, STR_STATE2, ESC_STATE, COMM_STATE, STATE_NOCH, \
STATE_CHG, STATE_DOWN, STATE_ESCD = range(9)

STATEX, TOKENX, REGEX, STATEX = range(4)

IDEN2   = "[A-Za-z_][A-Za-z0-9_]*"
HEX2    = "0x[0-9a-fA-F]+"
NOIDEN  = "[^a-zA-Z0-9_]"
WSPC    = "[ \t\n]"

def tok(name):
    #print("adding:", name)
    if name in tok2.keys():
        print("Warn: dup token", name)
        pass
    else:
        pass
        uni = punique()
        tok2[name] = uni
        tok3[uni] = name
    return name

def state2str(state):
    strx = "None"
    if state == INI_STATE: strx =    "INI_STATE"
    if state == STR_STATE: strx =    "STR_STATE"
    if state == STR_STATE2: strx =   "STR_STATE2"
    if state == ESC_STATE: strx =    "ESC_STATE"
    if state == COMM_STATE: strx =   "COMM_STATE"
    return strx

# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token match.
#
# The order of the definitions matter. First token match is returned.
# List high prioty items first. List longer items befors short ones.
#
# Elements:
#  ---| parsertate | tok | token regex | compiled regex | state change |---
#
# When editing this table, update tok and tokens together.

try:
    xtokens =  (
    # State    # Token      # Regex              # Notes
    (INI_STATE, "eolnl",    "\\\\\n"         ),
    (INI_STATE, "bsla",     "\\\\"           ),

    (INI_STATE, "ifdef2",    "%ifdef" + WSPC        ),
    (INI_STATE, "elifdef2",  "%elifdef" + WSPC      ),
    (INI_STATE, "define2",   "%define" + WSPC       ),
    (INI_STATE, "else2",    "%else" + WSPC          ),
    (INI_STATE, "endif2",   "%endif" + WSPC         ),

    (INI_STATE, "if",       "if" + WSPC             ),
    (INI_STATE, "elif",     "elif" + WSPC           ),
    (INI_STATE, "else",     "else" + WSPC           ),
    #(INI_STATE, "endif",    "endif" + WSPC         ),

    (INI_STATE, "func",      "func" + WSPC          ),
    (INI_STATE, "enter",     "enter" + WSPC         ),
    (INI_STATE, "leave",     "leave" + WSPC         ),
    (INI_STATE, "return",    "return" + WSPC        ),
    (INI_STATE, "loop",      "loop" + WSPC        ),

    (INI_STATE, "type",      "type" + WSPC          ),
    (INI_STATE, "aggr",      "aggr" + WSPC          ),

    (INI_STATE, "S8"    ,    "S8"            ),
    (INI_STATE, "S16"   ,    "S16"           ),
    (INI_STATE, "S32"   ,    "S32"           ),
    (INI_STATE, "S64"   ,    "S64"           ),
    (INI_STATE, "S128"  ,    "S128"          ),
    (INI_STATE, "U8"    ,    "U8"            ),
    (INI_STATE, "U16"   ,    "U16"           ),
    (INI_STATE, "U32"   ,    "U32"           ),
    (INI_STATE, "U64"   ,    "U64"           ),
    (INI_STATE, "U128"  ,    "U128"          ),

    (INI_STATE, "hex",      HEX2             ),
    (INI_STATE, "oct",      "0o[0-7]+"       ),
    (INI_STATE, "bin",      "0b[0-1]+"       ),
    (INI_STATE, "oct2",     "0y[0-17]+"      ),
    (INI_STATE, "bin2",     "0z[0-1]+"       ),

    (INI_STATE, "comm2d",    "\#\#.*\n"      ),
    (INI_STATE, "comm2d",    "\/\/\/.*\n"    ),
    (INI_STATE, "comm2",     "\#.*\n"        ),
    (INI_STATE, "comm2",     "\/\/.*\n"      ),

    (INI_STATE, "num",      "[0-9]+"         ),

    (INI_STATE, "bs",       "\b"             ),
    (INI_STATE, "quote",    "\""             ),
    (INI_STATE, "squote",   "\'"             ),
    (INI_STATE, "ident",    IDEN2            ),

    (INI_STATE, "peq",      "\+="            ),  # Add to
    (INI_STATE, "meq",      "\-="            ),  # Sub from
    (INI_STATE, "deq",      "=="             ),  # Equal
    (INI_STATE, "ndeq",     "!="             ),  # Not Equal
    (INI_STATE, "teq",      "==="            ),  # Identical
    (INI_STATE, "tneq",     "!=="            ),  # Not Identical
    (INI_STATE, "put",      "=>"             ),  # Put into
    (INI_STATE, "gett",     "<="             ),  # Get from
    (INI_STATE, "dref",     "->"             ),  # Reference
    (INI_STATE, "aref",     "<-"             ),  # De ref
    (INI_STATE, "idev",     "\/\%"           ),  # Int divide
    (INI_STATE, "and",      "\&\&"           ),  # Logical and
    (INI_STATE, "or",       "\|\|"           ),  # Logical or
    (INI_STATE, "xor",      "\^\^"           ),  # Logical or

    (INI_STATE, "at",       "@"              ),
    (INI_STATE, "excl",     "!"              ),
    (INI_STATE, "tilde",    "~"              ),
    (INI_STATE, "under",    "_"              ),

    (INI_STATE, "comm3",    "\/\*"           ),

    (INI_STATE, "(",        "\("             ),
    (INI_STATE, ")",        "\)"             ),
    (INI_STATE, "=",        "="              ),
    (INI_STATE, "<",        "<"              ),
    (INI_STATE, ">",        ">"              ),
    (INI_STATE, "&",        "&"              ),
    (INI_STATE, "*",        "\*"             ),
    (INI_STATE, "+",        "\+"             ),
    (INI_STATE, "-",        "\-"             ),
    (INI_STATE, "/",        "/"              ),
    (INI_STATE, "[",        "\["             ),
    (INI_STATE, "]",        "\]"             ),
    (INI_STATE, "{",        "\{"             ),
    (INI_STATE, "}",        "\}"             ),
    (INI_STATE, "semi",     ";"              ),
    (INI_STATE, "colon",    ":"              ),
    (INI_STATE, "::",       "::"             ),     # Double colon
    (INI_STATE, "dot",      "\."             ),

    (INI_STATE, "<<",       "<<"             ),     # Shift <
    (INI_STATE, ">>",       ">>"             ),
    (INI_STATE, "<<<",      "<<<"            ),     # Rotate <
    (INI_STATE, ">>>",      ">>>"            ),     # Rotate >
    (INI_STATE, "++",       "\+\+"           ),
    (INI_STATE, "--",       "\-\-"           ),

    (INI_STATE, "caret",    "\^"             ),
    (INI_STATE, "cent",     "%"              ),
    (INI_STATE, "sp",       " "              ),
    (INI_STATE, "tab",      "\t"             ),

    (INI_STATE, "nl",       "\n"             ),
    (INI_STATE, "comma",    ","              ),
    # Fallback here
    (INI_STATE, "any",      "."              ),

    # String states
    (STR_STATE, "sbsla",     "\\\\"         ),
    (STR_STATE, "dquote",    "\""           ),
    (STR_STATE, "sany",      "."            ),

    # String states2
    (STR_STATE2, "sbsla2",     "\\\\"       ),
    (STR_STATE2, "dsquote",    "\'"         ),
    (STR_STATE2, "ssany",      "."          ),

    # Comm states
    (COMM_STATE, "cbsla",     "\\\\"        ),
    (COMM_STATE, "ecomm3",    "\*\/"        ),
    (COMM_STATE, "cany",      "."           ),

    # Escape states
    (ESC_STATE, "shex",     "[0-9A-Za-z]+"  ),
    (ESC_STATE, "n",        "n"             ),
    (ESC_STATE, "r",        "r"             ),
    (ESC_STATE, "a",        "a"             ),
    (ESC_STATE, "0",        "0"             ),
    (ESC_STATE, "quote",    "\""            ),
    (ESC_STATE, "anyx",     "."             ),
    )

except KeyError as err:
    print("Cannot precomp", err, sys.exc_info())
    raise

#print("tok2", tok2)

rtok =  {}
for aa in tok2:
    rtok[tok2[aa]] = aa

#print("rtok", rtok)

# EOF
