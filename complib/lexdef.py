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
# To create a custom parser, just add new tokens / states
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

INI_STATE, STR_STATE, STR_STATE2, ESC_STATE     = range(4)
STATE_NOCH, STATE_CHG, STATE_DOWN, STATE_ESCD   = range(4)
STATEX, TOKENX, REGEX, STATEX = range(4)

IDEN2 = "[A-Za-z_][A-Za-z0-9_]*"
HEX2  = "0x[0-9a-fA-F]+"

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
    # State     Token      # Regex         # State Change
    (INI_STATE, "eolnl",    "\\\\\n"        , STATE_NOCH, ),
    (INI_STATE, "bsla",      "\\\\"         , STATE_NOCH, ),
    (INI_STATE, "ifdef",    "%ifdef"        , STATE_NOCH, ),
    (INI_STATE, "elifdef",  "%elifdef"      , STATE_NOCH, ),
    (INI_STATE, "define",   "%define"       , STATE_NOCH, ),
    (INI_STATE, "else2",    "%else"         , STATE_NOCH, ),
    (INI_STATE, "endif2",   "%endif"        , STATE_NOCH, ),

    (INI_STATE, "if",       "if"            , STATE_NOCH, ),
    (INI_STATE, "elif",     "elif"          , STATE_NOCH, ),
    (INI_STATE, "else",     "else"          , STATE_NOCH, ),
    (INI_STATE, "endif",    "endif"         , STATE_NOCH, ),

    (INI_STATE, "S8"    ,    "S8"           , STATE_NOCH, ),
    (INI_STATE, "S16"   ,    "S16"          , STATE_NOCH, ),
    (INI_STATE, "S32"   ,    "S32"          , STATE_NOCH, ),
    (INI_STATE, "S64"   ,    "S64"          , STATE_NOCH, ),
    (INI_STATE, "S128"  ,    "S128"         , STATE_NOCH, ),
    (INI_STATE, "U8"    ,    "U8"           , STATE_NOCH, ),
    (INI_STATE, "U16"   ,    "U16"          , STATE_NOCH, ),
    (INI_STATE, "U32"   ,    "U32"          , STATE_NOCH, ),
    (INI_STATE, "U64"   ,    "U64"          , STATE_NOCH, ),
    (INI_STATE, "U128"  ,    "U128"         , STATE_NOCH, ),

    #(INI_STATE, "str4",     "\#[0-9a-zA-Z]" ,  STATE_NOCH, ),
    #(INI_STATE, "str3",     "(\\\\[0-7]+)+" ,  STATE_NOCH, ),

    (INI_STATE, "hex",      HEX2            , STATE_NOCH, ),
    (INI_STATE, "oct",      "0o[0-7]+"      , STATE_NOCH, ),
    (INI_STATE, "bin",      "0b[0-1]+"      , STATE_NOCH, ),
    (INI_STATE, "oct2",     "0y[0-17]+"     , STATE_NOCH, ),
    (INI_STATE, "bin2",     "0z[0-1]+"      , STATE_NOCH, ),

    (INI_STATE, "comm2",     "\#.*\n"       , STATE_NOCH, ),
    (INI_STATE, "comm2",     "\/\/.*\n"     , STATE_NOCH, ),

    (INI_STATE, "num",      "[0-9]+"        , STATE_NOCH, ),

    (INI_STATE, "bs",       "\b"            , STATE_CHG,  ),
    (INI_STATE, "quote",    "\""            , STR_STATE,  ),
    (INI_STATE, "squote",   "\'"            , STR_STATE2, ),
    (INI_STATE, "ident",    IDEN2           , STATE_NOCH, ),

    (INI_STATE, "peq",      "\+="           , STATE_NOCH, ),
    (INI_STATE, "meq",      "\-="           , STATE_NOCH, ),
    (INI_STATE, "deq",      "=="            , STATE_NOCH, ),
    (INI_STATE, "put",      "=>"            , STATE_NOCH, ),
    (INI_STATE, "dref",     "->"            ,  STATE_NOCH, ),

    (INI_STATE, "at",       "@"             , STATE_NOCH, ),
    (INI_STATE, "exc",      "!"             , STATE_NOCH, ),
    (INI_STATE, "tilde",    "~"             ,  STATE_NOCH, ),
    (INI_STATE, "under",    "_"             ,  STATE_NOCH, ),

    (INI_STATE, "(",        "\("            ,  STATE_NOCH, ),
    (INI_STATE, ")",        "\)"            , STATE_NOCH, ),
    (INI_STATE, "=",       "="              , STATE_NOCH, ),
    (INI_STATE, "<",        "<"             , STATE_NOCH, ),
    (INI_STATE, ">",        ">"             , STATE_NOCH, ),
    (INI_STATE, "&",        "&"             , STATE_NOCH, ),
    (INI_STATE, "*",        "\*"            , STATE_NOCH, ),
    (INI_STATE, "+",        "\+"            , STATE_NOCH, ),
    (INI_STATE, "/",        "/"             , STATE_NOCH, ),
    (INI_STATE, "[",        "\["            , STATE_NOCH, ),
    (INI_STATE, "]",        "\]"            , STATE_NOCH, ),
    (INI_STATE, "{",        "\{"            , STATE_NOCH, ),
    (INI_STATE, "}",        "\}"            , STATE_NOCH, ),
    (INI_STATE, ":",        ";"             , STATE_NOCH, ),
    (INI_STATE, ";",        ":"             , STATE_NOCH, ),

    (INI_STATE, "caret",    "\^"            , STATE_NOCH, ),
    (INI_STATE, "%",        "%"             , STATE_NOCH, ),
    (INI_STATE, "sp",       " "             , STATE_NOCH, ),
    (INI_STATE, "tab",      "\t"            , STATE_NOCH, ),

    (INI_STATE, "nl",       "\n"            , STATE_NOCH, ),
    (INI_STATE, "comma",    ","             , STATE_NOCH, ),
    # Fallback here
    (INI_STATE, "any",      "."             , STATE_NOCH, ),

    # String states
    (STR_STATE, "sbsla",     "\\\\"         ,  STATE_CHG, ),
    (STR_STATE, "dquote",     "\""          ,  STATE_DOWN, ),
    (STR_STATE, "sany",      "."            ,  STATE_NOCH, ),

    # String states2
    (STR_STATE2, "sbsla",     "\\\\"        ,  STATE_CHG, ),
    (STR_STATE2, "dsquote",    "\'"         ,  STATE_DOWN, ),
    (STR_STATE2, "ssany",      "."          ,  STATE_NOCH, ),

    # Escape states
    (ESC_STATE, "shex",     "[0-9A-Za-z]+"   , STATE_ESCD, ),
    (ESC_STATE, "n",        "n"              , STATE_ESCD, ),
    (ESC_STATE, "r",        "r"              , STATE_ESCD, ),
    (ESC_STATE, "a",        "a"              , STATE_ESCD, ),
    (ESC_STATE, "0",        "0"              , STATE_ESCD, ),
    (ESC_STATE, "quote",    "\""             , STATE_ESCD, ),
    (ESC_STATE, "anyx",     "."              , STATE_ESCD, ),
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
