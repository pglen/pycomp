#!/usr/bin/env python3

''' This is a parser skeleton for language development
        This file defines the tokens and parser states
'''

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
# Some tokens have no phase entries, these are used on summary output

#from enum import Enum
#class ST(Enum):
#    INI_STATE = 0; STR_STATE = 1; STR2_STATE = 2;
#    COMM_STATE = 3; ESC_STATE = 4; HEX_STATE = 5;
#    UNI_STATE = 6
#print(dir(ST.INI_STATE))

(STATEX, TOKENX, REGEX, STATEX2, ) = range(4)
(INI_STATE, STR_STATE, STR2_STATE, COMM_STATE, ESC_STATE, HEX_STATE,
UNI_STATE, ) =  range(7)

def state2str(state):

    ''' Convert state to string '''
    strx = "None"
    if state == STATEX:        strx = "STATEX"
    if state == TOKENX:        strx = "TOKENX"
    if state == REGEX:         strx = "REGEX"
    if state == STATEX2:       strx = "STATEX2"
    if state == INI_STATE:     strx = "INI_STATE"
    if state == STR_STATE:     strx = "STR_STATE"
    if state == STR2_STATE:    strx = "STR2_STATE"
    if state == COMM_STATE:    strx = "COMM_STATE"
    if state == ESC_STATE:     strx = "ESC_STATE"
    if state == HEX_STATE:     strx = "HEX_STATE"
    if state == UNI_STATE:     strx = "UNI_STAT"
    return strx

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
    # State     # Token          # Regex              # Notes
    (INI_STATE, "eolnl",        r"\\\\\n"            ),
    (INI_STATE, "bsla",         r"\\\\"              ),

    (INI_STATE, "ifdef2",       r"%ifdef" + WSPC     ),
    (INI_STATE, "elifdef2",     r"%elifdef" + WSPC   ),
    (INI_STATE, "define2",      r"%define" + WSPC    ),
    (INI_STATE, "else2",        r"%else" + WSPC      ),
    (INI_STATE, "endif2",       r"%endif" + WSPC     ),

    (INI_STATE, "if",           r"if" + WSPC         ),
    (INI_STATE, "elif",         r"elif" + WSPC       ),
    (INI_STATE, "else",         r"else" + WSPC       ),
    #(INI_STATE, "endif",       r"endif" + WSPC      ),

    (INI_STATE, "func",         r"func" + WSPC       ),
    (INI_STATE, "enter",        r"enter" + WSPC      ),
    (INI_STATE, "leave",        r"leave" + WSPC      ),
    (INI_STATE, "return",       r"return" + WSPC     ),
    (INI_STATE, "loop",         r"loop" + WSPC       ),

    (INI_STATE, "type",         r"type" + WSPC       ),
    (INI_STATE, "aggr",         r"aggr" + WSPC       ),
    (INI_STATE, "enum",         r"enum" + WSPC       ),

    (INI_STATE, "S8" ,          r"S8"                ),
    (INI_STATE, "S16",          r"S16"               ),
    (INI_STATE, "S32",          r"S32"               ),
    (INI_STATE, "S64",          r"S64"               ),
    (INI_STATE, "S128",         r"S128"              ),
    (INI_STATE, "U8" ,          r"U8"                ),
    (INI_STATE, "U16",          r"U16"               ),
    (INI_STATE, "U32",          r"U32"               ),
    (INI_STATE, "U64",          r"U64"               ),
    (INI_STATE, "U128",         r"U128"              ),

    (INI_STATE, "hex",          HEX2                ),
    (INI_STATE, "oct",          r"0o[0-7]+"          ),
    (INI_STATE, "bin",          r"0b[0-1]+"          ),
    (INI_STATE, "oct2",         r"0y[0-17]+"         ),
    (INI_STATE, "bin2",         r"0z[0-1]+"          ),

    (INI_STATE, "comm2d",       r"\#\#.*\n"          ),
    (INI_STATE, "comm2d",       r"\/\/\/.*\n"        ),
    (INI_STATE, "comm2",        r"\#.*\n"            ),
    (INI_STATE, "comm2",        r"\/\/.*\n"          ),

    (INI_STATE, "num",          r"[0-9]+"            ),

    (INI_STATE, "bs",           "\b"                ),
    (INI_STATE, "quote",        r"\""                ),
    (INI_STATE, "squote",       r"\'"                ),
    (INI_STATE, "ident",        IDEN2               ),

    (INI_STATE, "peq",          r"\+="               ),  # Add to
    (INI_STATE, "meq",          r"\-="               ),  # Sub from
    (INI_STATE, "deq",          r"=="                ),  # Equal
    (INI_STATE, "ndeq",         r"!="                ),  # Not Equal
    (INI_STATE, "teq",          r"==="               ),  # Identical
    (INI_STATE, "tneq",         r"!=="               ),  # Not Identical
    (INI_STATE, "put",          r"=>"                ),  # Put into
    (INI_STATE, "gett",         r"<="                ),  # Get from
    (INI_STATE, "dref",         r"->"                ),  # Reference
    (INI_STATE, "aref",         r"<-"                ),  # De ref
    (INI_STATE, "idev",         r"\/\%"              ),  # Int divide
    (INI_STATE, "and",          r"\&\&"              ),  # Logical and
    (INI_STATE, "or",           r"\|\|"              ),  # Logical or
    (INI_STATE, "xor",          r"\^\^"              ),  # Logical or

    (INI_STATE, "at",           r"@"                 ),
    (INI_STATE, "excl",         r"!"                 ),
    (INI_STATE, "tilde",        r"~"                 ),
    (INI_STATE, "under",        r"_"                 ),

    (INI_STATE, "comm3",        r"\/\*"              ),

    (INI_STATE, "(",            r"\("                ),
    (INI_STATE, ")",            r"\)"                ),
    (INI_STATE, "=",            r"="                 ),
    (INI_STATE, "<",            r"<"                 ),
    (INI_STATE, ">",            r">"                 ),
    (INI_STATE, "&",            r"&"                 ),
    (INI_STATE, "*",            r"\*"                ),
    (INI_STATE, "+",            r"\+"                ),
    (INI_STATE, "-",            r"\-"                ),
    (INI_STATE, "/",            r"/"                 ),
    (INI_STATE, "[",            r"\["                ),
    (INI_STATE, "]",            r"\]"                ),
    (INI_STATE, "{",            r"\{"                ),
    (INI_STATE, "}",            r"\}"                ),
    (INI_STATE, "semi",         r";"                 ),
    (INI_STATE, "colon",        r":"                 ),
    (INI_STATE, "::",           r"::"                ),  # Double colon
    (INI_STATE, "dot",          r"\."                ),

    (INI_STATE, "<<",           r"<<"                ),  # Shift <
    (INI_STATE, ">>",           r">>"                ),
    (INI_STATE, "<<<",          r"<<<"               ),  # Rotate <
    (INI_STATE, ">>>",          r">>>"               ),  # Rotate >
    (INI_STATE, "++",           r"\+\+"              ),
    (INI_STATE, "--",           r"\-\-"              ),

    (INI_STATE, "caret",        r"\^"                ),
    (INI_STATE, "cent",         r"%"                 ),
    (INI_STATE, "sp",           r" "                 ),
    (INI_STATE, "tab",          r"\t"                ),
    (INI_STATE, "nl",           r"\n"                ),
    (INI_STATE, "comma",        r","                 ),

    #callback here
    (INI_STATE, "any",          r"."                 ),

    #string state
    (STR_STATE, "sbsla",        r"\\\\"              ),
    (STR_STATE, "dquote",       r"\""                ),
    (STR_STATE, "sany",         r"."                 ),

    #string state
    (STR2_STATE, "sbsla2",     r"\\\\"               ),
    (STR2_STATE, "dquote2",    r"\'"                 ),
    (STR2_STATE, "sany2",      r"."                  ),

    #comm states
    #(COMM_STATE, "cbsla",     r"\\\\"               ),
    (COMM_STATE, "ecomm3",     r"\*\/"               ),
    (COMM_STATE, "cany",       r"."                  ),

    #escape state
    (ESC_STATE, "anyx",        r"."                  ),

    (UNI_STATE, "unihex",      r"[0-9A-Fa-f]{4,8}"   ),
    (UNI_STATE, "anyu",        r"."                  ),

    (HEX_STATE, "eschex",      r"[0-9A-Fa-f]{1,2}"   ),
    (HEX_STATE, "anyh",        r"."                  ),
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
