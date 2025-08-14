#!/usr/bin/env python3

''' This is a parser skeleton for language development
        This file defines the tokens and parser states
'''

try:
    from complib.utils import *
except:
    print(__file__, ":local import:")
    from utils import *

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

from enum import Enum

class ST(Enum):
    INI_STATE = 0; STR_STATE = 1; STR2_STATE = 2;
    COMM_STATE = 3; ESC_STATE = 4; HEX_STATE = 5;
    UNI_STATE = 6

#print(dir(ST.INI_STATE))

STATEX, TOKENX, REGEX, STATEX = range(4)

IDEN2   = "[A-Za-z_][A-Za-z0-9_]*"
HEX2    = "0x[0-9a-fA-F]+"
NOIDEN  = "[^a-zA-Z0-9_]"
WSPC    = "[ \t\n]"

def tok(name):
    '''  Create token on the fly, if there is one already, return it.
    '''
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
    # State    # Token          # Regex              # Notes
    (ST.INI_STATE.value, "eolnl",        "\\\\\n"            ),
    (ST.INI_STATE.value, "bsla",         "\\\\"              ),

    (ST.INI_STATE.value, "ifdef2",       "%ifdef" + WSPC     ),
    (ST.INI_STATE.value, "elifdef2",     "%elifdef" + WSPC   ),
    (ST.INI_STATE.value, "define2",      "%define" + WSPC    ),
    (ST.INI_STATE.value, "else2",        "%else" + WSPC      ),
    (ST.INI_STATE.value, "endif2",       "%endif" + WSPC     ),

    (ST.INI_STATE.value, "if",           "if" + WSPC         ),
    (ST.INI_STATE.value, "elif",         "elif" + WSPC       ),
    (ST.INI_STATE.value, "else",         "else" + WSPC       ),
    #ST.(INI_STATE.value, "endif",       "endif" + WSPC      ),

    (ST.INI_STATE.value, "func",         "func" + WSPC       ),
    (ST.INI_STATE.value, "enter",        "enter" + WSPC      ),
    (ST.INI_STATE.value, "leave",        "leave" + WSPC      ),
    (ST.INI_STATE.value, "return",       "return" + WSPC     ),
    (ST.INI_STATE.value, "loop",         "loop" + WSPC       ),

    (ST.INI_STATE.value, "type",         "type" + WSPC       ),
    (ST.INI_STATE.value, "aggr",         "aggr" + WSPC       ),
    (ST.INI_STATE.value, "enum",         "enum" + WSPC       ),

    (ST.INI_STATE.value, "S8" ,          "S8"                ),
    (ST.INI_STATE.value, "S16",          "S16"               ),
    (ST.INI_STATE.value, "S32",          "S32"               ),
    (ST.INI_STATE.value, "S64",          "S64"               ),
    (ST.INI_STATE.value, "S128",         "S128"              ),
    (ST.INI_STATE.value, "U8" ,          "U8"                ),
    (ST.INI_STATE.value, "U16",          "U16"               ),
    (ST.INI_STATE.value, "U32",          "U32"               ),
    (ST.INI_STATE.value, "U64",          "U64"               ),
    (ST.INI_STATE.value, "U128",         "U128"              ),

    (ST.INI_STATE.value, "hex",          HEX2                ),
    (ST.INI_STATE.value, "oct",          "0o[0-7]+"          ),
    (ST.INI_STATE.value, "bin",          "0b[0-1]+"          ),
    (ST.INI_STATE.value, "oct2",         "0y[0-17]+"         ),
    (ST.INI_STATE.value, "bin2",         "0z[0-1]+"          ),

    (ST.INI_STATE.value, "comm2d",       "\#\#.*\n"          ),
    (ST.INI_STATE.value, "comm2d",       "\/\/\/.*\n"        ),
    (ST.INI_STATE.value, "comm2",        "\#.*\n"            ),
    (ST.INI_STATE.value, "comm2",        "\/\/.*\n"          ),

    (ST.INI_STATE.value, "num",          "[0-9]+"            ),

    (ST.INI_STATE.value, "bs",           "\b"                ),
    (ST.INI_STATE.value, "quote",        "\""                ),
    (ST.INI_STATE.value, "squote",       "\'"                ),
    (ST.INI_STATE.value, "ident",        IDEN2               ),

    (ST.INI_STATE.value, "peq",          "\+="               ),  # Add to
    (ST.INI_STATE.value, "meq",          "\-="               ),  # Sub from
    (ST.INI_STATE.value, "deq",          "=="                ),  # Equal
    (ST.INI_STATE.value, "ndeq",         "!="                ),  # Not Equal
    (ST.INI_STATE.value, "teq",          "==="               ),  # Identical
    (ST.INI_STATE.value, "tneq",         "!=="               ),  # Not Identical
    (ST.INI_STATE.value, "put",          "=>"                ),  # Put into
    (ST.INI_STATE.value, "gett",         "<="                ),  # Get from
    (ST.INI_STATE.value, "dref",         "->"                ),  # Reference
    (ST.INI_STATE.value, "aref",         "<-"                ),  # De ref
    (ST.INI_STATE.value, "idev",         "\/\%"              ),  # Int divide
    (ST.INI_STATE.value, "and",          "\&\&"              ),  # Logical and
    (ST.INI_STATE.value, "or",           "\|\|"              ),  # Logical or
    (ST.INI_STATE.value, "xor",          "\^\^"              ),  # Logical or

    (ST.INI_STATE.value, "at",           "@"                 ),
    (ST.INI_STATE.value, "excl",         "!"                 ),
    (ST.INI_STATE.value, "tilde",        "~"                 ),
    (ST.INI_STATE.value, "under",        "_"                 ),

    (ST.INI_STATE.value, "comm3",        "\/\*"              ),

    (ST.INI_STATE.value, "(",            "\("                ),
    (ST.INI_STATE.value, ")",            "\)"                ),
    (ST.INI_STATE.value, "=",            "="                 ),
    (ST.INI_STATE.value, "<",            "<"                 ),
    (ST.INI_STATE.value, ">",            ">"                 ),
    (ST.INI_STATE.value, "&",            "&"                 ),
    (ST.INI_STATE.value, "*",            "\*"                ),
    (ST.INI_STATE.value, "+",            "\+"                ),
    (ST.INI_STATE.value, "-",            "\-"                ),
    (ST.INI_STATE.value, "/",            "/"                 ),
    (ST.INI_STATE.value, "[",            "\["                ),
    (ST.INI_STATE.value, "]",            "\]"                ),
    (ST.INI_STATE.value, "{",            "\{"                ),
    (ST.INI_STATE.value, "}",            "\}"                ),
    (ST.INI_STATE.value, "semi",         ";"                 ),
    (ST.INI_STATE.value, "colon",        ":"                 ),
    (ST.INI_STATE.value, "::",           "::"                ),  # Double colon
    (ST.INI_STATE.value, "dot",          "\."                ),

    (ST.INI_STATE.value, "<<",           "<<"                ),  # Shift <
    (ST.INI_STATE.value, ">>",           ">>"                ),
    (ST.INI_STATE.value, "<<<",          "<<<"               ),  # Rotate <
    (ST.INI_STATE.value, ">>>",          ">>>"               ),  # Rotate >
    (ST.INI_STATE.value, "++",           "\+\+"              ),
    (ST.INI_STATE.value, "--",           "\-\-"              ),

    (ST.INI_STATE.value, "caret",        "\^"                ),
    (ST.INI_STATE.value, "cent",         "%"                 ),
    (ST.INI_STATE.value, "sp",           " "                 ),
    (ST.INI_STATE.value, "tab",          "\t"                ),
    (ST.INI_STATE.value, "nl",           "\n"                ),
    (ST.INI_STATE.value, "comma",        ","                 ),

    # Fallback here
    (ST.INI_STATE.value, "any",          "."                 ),

    # String states
    (ST.STR_STATE.value, "sbsla",        "\\\\"              ),
    (ST.STR_STATE.value, "dquote",       "\""                ),
    (ST.STR_STATE.value, "sany",         "."                 ),

    # String states2
    (ST.STR2_STATE.value, "sbsla2",     "\\\\"               ),
    (ST.STR2_STATE.value, "dquote2",    "\'"                 ),
    (ST.STR2_STATE.value, "sany2",      "."                  ),

    # Comm states
    #ST.(COMM_STATE.value, "cbsla",     "\\\\"               ),
    (ST.COMM_STATE.value, "ecomm3",     "\*\/"               ),
    (ST.COMM_STATE.value, "cany",       "."                  ),

    # Escape states
    (ST.ESC_STATE.value, "anyx",        "."                  ),

    (ST.UNI_STATE.value, "unihex",      "[0-9A-Fa-f]{4,8}"   ),
    (ST.UNI_STATE.value, "anyu",        "."                  ),

    (ST.HEX_STATE.value, "eschex",      "[0-9A-Fa-f]{1,2}"   ),
    (ST.HEX_STATE.value, "anyh",        "."                  ),
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
