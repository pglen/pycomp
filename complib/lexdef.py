#!/usr/bin/env python3

''' This is a parser skeleton for language development
        This file defines the tokens and token states
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

# The order of the definitions only matters as lexing priority. Longer
# tokens should be at the top, fallback alternates at the buttom.
#
# To add a new syntactic element, search for an existing feature (like 'func')
# Add the new element into the a.) definition, b.) regex defintion,
# c.) state definition, d.) state table, e.) action function.
#
# The script is self checking, will report on missing defintions. However,
# it can not (will not) report on syntactic anomalies of the target
# language itself.

class LexI():

    ''' Store one lexed item (used to be a list, but got out of hand)
    '''

    def __init__(self, stampx = [], mstr = "", startx = 0, endx = 0):
        self.state = INI_STATE
        self.stamp = stampx
        self.mstr = mstr        # Main payload
        self.start = startx
        self.end = endx
        self.flag = 0           # State information
        self.val = 0.0
        self.ival = 0

    def copy(self, other):
        other.state = self.state
        other.stamp = self.stamp
        other.mstr = self.mstr
        other.start = self.start
        other.end = self.end
        other.flag = self.flag
        other.val = self.val
        other.ival = self.ival

    def __str__(self):
        '''   Deliver it in an easy to see format  '''
        return  "[ " + pp(self.stamp[1]) + " = " + pp(self.mstr) + ", " + \
                        pp(str(self.flag)) + " ] "

    def dump(self):
        strx = "[ Lex: " + padx("'" + str(self.stamp) + "' => '" + \
                        cesc(self.mstr) + "'", 20)  + \
                        "flag = " + padx("%d" % (self.flag)) + \
                        "pos = "  + padx("%d:%d" % (self.start, self.end), 8) +  \
                        "val = "  + padx("%d" % (self.val)) + \
                        "ival = " + padx("%d" % (self.ival)) + \
                        "]"
        return strx

# Lexer states
(INI_STATE, STR_STATE, STR2_STATE, COMM_STATE, COMM_STATED, ESC_STATE, HEX_STATE,
    UNI_STATE, ) =  range(8)

def state2str(state):

    ''' Convert state to string '''

    strx = "None"
    if state == INI_STATE:     strx = "INI_STATE"
    if state == STR_STATE:     strx = "STR_STATE"
    if state == STR2_STATE:    strx = "STR2_STATE"
    if state == COMM_STATE:    strx = "COMM_STATE"
    if state == COMM_STATED:   strx = "COMM_STATED"
    if state == ESC_STATE:     strx = "ESC_STATE"
    if state == HEX_STATE:     strx = "HEX_STATE"
    if state == UNI_STATE:     strx = "UNI_STATE"
    return strx

# Regex shortcuts
IDEN2   = "[A-Za-z_][A-Za-z0-9_]*"
HEX2    = "0x[0-9a-fA-F]+"
NOIDEN  = "[^a-zA-Z0-9_]"

# Tokens that start with a keyword is still valid  like: func_hello
IDEN3   = "[A-Za-z0-9_]+"

# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token match.
#
# The order of the definitions matter. First token match is returned
# before later match. List high prioty items first, and list longer
# items befors short ones.
#
# Elements of the list:
#       parser state | token | token regex
# Filled in automatically:
#       compiled regex | state change

# The token (name) is an approximate texttual representation of
# the token. This way it is eazy to see the kind of token in the parser.

try:
    xtokens =  (
    # State     # Token         # Regex             # OPT Notes
    # --------  -------         -------             ------------
    (INI_STATE, "eolnl",        r"\\\\\n"           ),
    (INI_STATE, "bsla",         r"\\\\"             ),

    (INI_STATE, "ifdef2",       r"%ifdef"           ),
    (INI_STATE, "elifdef2",     r"%elifdef"         ),
    (INI_STATE, "define2",      r"%define"          ),
    (INI_STATE, "else2",        r"%else"            ),
    (INI_STATE, "endif2",       r"%endif"           ),

    (INI_STATE, "if",           r"if"  + IDEN3      ),
    (INI_STATE, "if",           r"if"               ),
    (INI_STATE, "elif",         r"elif"  + IDEN3    ),
    (INI_STATE, "elif",         r"elif"             ),
    (INI_STATE, "else",         r"else"   + IDEN3   ),
    (INI_STATE, "else",         r"else"             ),
    (INI_STATE, "endif",        r"endif"   + IDEN3  ),
    (INI_STATE, "endif",        r"endif"            ),

    (INI_STATE, "ident",        r"func" + IDEN3     ),
    (INI_STATE, "func",         r"func"             ),
    (INI_STATE, "enter",        r"enter" + IDEN3    ),
    (INI_STATE, "enter",        r"enter"            ),
    (INI_STATE, "leave",        r"leave" + IDEN3    ),
    (INI_STATE, "leave",        r"leave"            ),
    (INI_STATE, "return",       r"return" + IDEN3   ),
    (INI_STATE, "return",       r"return"           ),
    (INI_STATE, "loop",         r"loop"  + IDEN3    ),
    (INI_STATE, "loop",         r"loop"             ),

    (INI_STATE, "type",         r"type"  + IDEN3    ),
    (INI_STATE, "type",         r"type"             ),
    (INI_STATE, "aggr",         r"aggr"  + IDEN3    ),
    (INI_STATE, "aggr",         r"aggr"             ),
    (INI_STATE, "enum",         r"enum"   + IDEN3   ),
    (INI_STATE, "enum",         r"enum"             ),

    (INI_STATE, "dbl",          r"double"           ),
    (INI_STATE, "float",        r"float"            ),

    (INI_STATE, "decl" ,        r"[sS]8"            ),
    (INI_STATE, "decl",         r"[sS]16"           ),
    (INI_STATE, "decl",         r"[sS]32"           ),
    (INI_STATE, "decl",         r"[sS]64"           ),
    (INI_STATE, "decl",         r"[sS]128"          ),
    (INI_STATE, "decl" ,        r"[uU]8"            ),
    (INI_STATE, "decl",         r"[uU]16"           ),
    (INI_STATE, "decl",         r"[uU]32"           ),
    (INI_STATE, "decl",         r"[uU]64"           ),
    (INI_STATE, "decl",         r"[uU]128"          ),

    (INI_STATE, "hex",          HEX2                ),
    (INI_STATE, "oct",          r"0o[0-7]+"         ),
    (INI_STATE, "bin",          r"0b[0-1]+"         ),
    (INI_STATE, "oct2",         r"0y[0-17]+"        ),
    (INI_STATE, "bin2",         r"0z[0-1]+"         ),

    (INI_STATE, "comm2d",       r"\#\#.*\n"         ),
    (INI_STATE, "comm2d",       r"\/\/\/.*\n"       ),
    (INI_STATE, "comm2",        r"\#.*\n"           ),
    (INI_STATE, "comm2",        r"\/\/.*\n"         ),

    (INI_STATE, "num",          r"[0-9]+"           ),

    (INI_STATE, "bs",           "\b"                ),
    (INI_STATE, "quote",        r"\""               ),
    (INI_STATE, "squote",       r"\'"               ),
    (INI_STATE, "ident",        IDEN2               ),

    (INI_STATE, "peq",          r"\+="              ),  # Add to
    (INI_STATE, "meq",          r"\-="              ),  # Sub from
    (INI_STATE, "deq",          r"=="               ),  # Equal
    (INI_STATE, "ndeq",         r"!="               ),  # Not Equal
    (INI_STATE, "teq",          r"==="              ),  # Identical
    (INI_STATE, "tneq",         r"!=="              ),  # Not Identical
    (INI_STATE, "put",          r"=>"               ),  # Put into
    (INI_STATE, "gett",         r"<="               ),  # Get from
    (INI_STATE, "dref",         r"->"               ),  # Reference
    (INI_STATE, "aref",         r"<-"               ),  # De ref
    (INI_STATE, "idev",         r"\/\%"             ),  # Int divide
    (INI_STATE, "and",          r"\&\&"             ),  # Logical and
    (INI_STATE, "or",           r"\|\|"             ),  # Logical or
    (INI_STATE, "xor",          r"\^\^"             ),  # Logical or

    (INI_STATE, "at",           r"@"                ),
    (INI_STATE, "excl",         r"!"                ),
    (INI_STATE, "tilde",        r"~"                ),
    (INI_STATE, "under",        r"_"                ),

    (INI_STATE, "comm3d",       r"\/\*\*"           ),
    (INI_STATE, "comm3",        r"\/\*"             ),

    (INI_STATE, "(",            r"\("               ),
    (INI_STATE, ")",            r"\)"               ),
    (INI_STATE, "=",            r"="                ),
    (INI_STATE, "<",            r"<"                ),
    (INI_STATE, ">",            r">"                ),
    (INI_STATE, "&",            r"&"                ),
    (INI_STATE, "*",            r"\*"               ),
    (INI_STATE, "+",            r"\+"               ),
    (INI_STATE, "-",            r"\-"               ),
    (INI_STATE, "/",            r"/"                ),
    (INI_STATE, "[",            r"\["               ),
    (INI_STATE, "]",            r"\]"               ),
    (INI_STATE, "{",            r"\{"               ),
    (INI_STATE, "}",            r"\}"               ),
    (INI_STATE, ";",            r";"                ),
    (INI_STATE, ":",            r":"                ),
    (INI_STATE, "::",           r"::"               ),  # Double colon
    (INI_STATE, "dot",          r"\."               ),

    (INI_STATE, "<<",           r"<<"               ),  # Shift <
    (INI_STATE, ">>",           r">>"               ),
    (INI_STATE, "<<<",          r"<<<"              ),  # Rotate <
    (INI_STATE, ">>>",          r">>>"              ),  # Rotate >
    (INI_STATE, "++",           r"\+\+"             ),
    (INI_STATE, "--",           r"\-\-"             ),

    (INI_STATE, "caret",        r"\^"               ),
    (INI_STATE, "cent",         r"%"                ),
    # We parse white spaces, let the parser deal with it
    (INI_STATE, "sp",           r" "                ),
    (INI_STATE, "tab",          r"\t"               ),
    (INI_STATE, "nl",           r"\n"               ),
    (INI_STATE, "comma",        r","                ),

    #callback here
    (INI_STATE, "any",          r"."                ),

    #string state
    (STR_STATE, "sbsla",        r"\\\\"             ),
    (STR_STATE, "dquote",       r"\""               ),
    (STR_STATE, "sany",         r"."                ),

    #string state
    (STR2_STATE, "sbsla2",     r"\\\\"              ),
    (STR2_STATE, "dquote2",    r"\'"                ),
    (STR2_STATE, "sany2",      r"."                 ),

    #comm states
    #(COMM_STATE, "cbsla",     r"\\\\"              ),
    (COMM_STATE,  "ecomm3",     r"\*\/"              ),
    (COMM_STATE,  "cany",       "(?s)."                 ),
    (COMM_STATED, "ecomm3d",    r"\*\/"              ),
    (COMM_STATED, "canyd",      r"(?s)."                 ),

    #escape state
    (ESC_STATE, "anyx",        r"."                 ),

    (UNI_STATE, "unihex",      r"[0-9A-Fa-f]{4,8}"  ),
    (UNI_STATE, "anyu",        r"."                 ),

    (HEX_STATE, "eschex",      r"[0-9A-Fa-f]{1,2}"  ),
    (HEX_STATE, "anyh",        r"."                 ),
    )

except KeyError as err:
    print("Cannot precomp", err, sys.exc_info())
    raise

# EOF
