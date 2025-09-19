#!/usr/bin/env python3

''' This is a parser skeleton for language development
        This file defines the tokens and token states
'''

from complib.utils import *
import complib.lexfunc as lexfunc

# We initialize parser variables in the context of the parser module.
#
# a.) Token definitions, b.) Lexer tokens,
# c.) Parser functions, d.) Parser state, e.) Parse table
#
# To create a custom parser, just add new tokens / states here
#

class StI():

    ''' Store one stamp. (used to be a list, but got out of hand)
    '''

    def __init__(self, stampx):
        self.num  = stampx[0]
        self.xstr = stampx[1]
        self.reg  = stampx[2]

    def __str__(self):
        return "[ " + str(self.num) + " = " + pp(str(self.xstr)) + " " \
               + pp(str(self.reg)) + " ]"

# Quick into: The lexer creates a stack of tokens. The parser scans
# the tokens, and walks the state machine for matches. If match
# is encountered, the parser calls the function in the state table,
# and / or changes state. Reduce is called after the state has been
# successfully digested. For more info see lex / yacc literature.

class LexI():

    ''' Store one lexed item (used to be a list, but got out of hand)
    '''

    def __init__(self, stampx = [], mstr = "", startx = 0, endx = 0):
        self.state = INI_STATE
        self.stamp = stampx
        self.mstr = mstr        # Main payload
        self.start = startx
        self.end = endx
        # Init future vars (just to show what comes)
        self.flag = 0           # State information
        self.linenum = 0
        self.linestart = 0
        self.lineoffs = 0
        self.pos = 0
        self.val = 0.0          # if number
        self.ival = 0           # if integer
        self.wantstate = None

        # Decode and mold
        if self.stamp.xstr == "num":
            self.ival = int(self.mstr)

        if self.stamp.xstr == "hex":
            self.stamp.xstr = "num"
            self.ival = int(self.mstr[2:], 16)

        if self.stamp.xstr == "oct":
            self.stamp.xstr = "num"
            self.ival = int(self.mstr[2:], 8)

        if self.stamp.xstr == "bin":
            self.stamp.xstr = "num"
            self.ival = int(self.mstr[2:], 2)

        #print("inited", str(self))

    def copy(self, other):
        other.state = self.state
        other.stamp = self.stamp
        other.mstr = self.mstr
        other.start = self.start
        other.end = self.end
        other.flag = self.flag
        other.val = self.val
        other.ival = self.ival
        other.wantstate = self.wantstate

    def __str__(self):
        '''   Deliver it in an easy to see format  '''
        strx = "[ " + pp(self.stamp.xstr) + " -> " + pp(self.mstr) + \
                        " ival = " + pp(str(self.ival)) + \
                        " flag = " + pp(str(self.flag)) + \
                        " ]"
        #" want = " + state2str(self.wantstate) + \
        return strx

    def dump(self):
        strx = " [ Lex: " + padx("'" + str(self.stamp) + "' => '" + \
                        cesc(self.mstr) + "'", 20) + \
                        " flag = " + padx("%d" % (self.flag)) + \
                        " st/en = " + padx("%d:%d" % (self.start, self.end), 8) +  \
                        " val = "  + ("%d" % (self.val)) + \
                        " ival = " + ("%d" % (self.ival)) + \
                        " line = " + ("%d" % (self.linenum+1)) + \
                        " offs = " + ("%d" % (self.lineoffs+1)) + \
                        " lsta = " + ("%d" % (self.linestart)) + \
                        " ] "
        #" want = " + state2str(self.wantstate) + \
        return strx

# Lexer states
(INI_STATE, STR_STATE, STR2_STATE, COMM_STATE, COMM_STATED, ESC_STATE, HEX_STATE,
    UNI_STATE, POP_STATE) =  range(9)

def state2str(state):

    ''' Convert state to string '''
    if state == None:
        return "NoneState"

    strx = "InvalState"
    if state == INI_STATE:     strx = "INI_STATE"
    if state == STR_STATE:     strx = "STR_STATE"
    if state == STR2_STATE:    strx = "STR2_STATE"
    if state == COMM_STATE:    strx = "COMM_STATE"
    if state == COMM_STATED:   strx = "COMM_STATED"
    if state == ESC_STATE:     strx = "ESC_STATE"
    if state == HEX_STATE:     strx = "HEX_STATE"
    if state == UNI_STATE:     strx = "UNI_STATE"
    return strx

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

# Regex shortcuts
IDEN2   = "[A-Za-z_][A-Za-z0-9_]*"
HEX2    = "0x[0-9a-fA-F]+"
HEX2u   = "0X[0-9a-fA-F]+"
NOIDEN  = "[^a-zA-Z0-9_]"
FLOATX  = "[0-9]*\.[0-9]*([Ee][0-9]+)?"

# Tokens that start with a keyword are still valid. Like: func_hello
IDEN3   = "[A-Za-z0-9_]+"

# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token match.
#
# The order of the definitions matter. First token match is returned
# before later match. List high prioty items first, and list longer
# items befors short ones.
#
# Elements of the list:
#       parser_state | token_val | token_regex | new_state_flag | call_action
# Filled in automatically:
#       compiled regex

# The token (name) is an approximate textual representation of
# the token. This way it is eazy to see the kind of token in the parser.

try:
    # State     # Token         # Regex             # New State    # OPT Notes
    # --------  -------         -------             ------------
    xtokens =  (
    (INI_STATE, "eolnl",        r"\\\\\n",          None, None ),
    (INI_STATE, "bsla",         r"\\\\" ,           None, None ),

    (INI_STATE, "ifdef2",       r"%ifdef",          None, None ),
    (INI_STATE, "elifdef2",     r"%elifdef",        None, None ),
    (INI_STATE, "define2",      r"%define",         None, None ),
    (INI_STATE, "else2",        r"%else",           None, None ),
    (INI_STATE, "endif2",       r"%endif",          None, None ),

    (INI_STATE, "if",           r"if" + IDEN3,      None, None ),
    (INI_STATE, "if",           r"if",              None, None ),
    (INI_STATE, "elif",         r"elif" + IDEN3,    None, None ),
    (INI_STATE, "elif",         r"elif" ,           None, None ),
    (INI_STATE, "else",         r"else"  + IDEN3,   None, None ),
    (INI_STATE, "else",         r"else",            None, None ),
    (INI_STATE, "endif",        r"endif"  + IDEN3,  None, None ),
    (INI_STATE, "endif",        r"endif",           None, None ),

    (INI_STATE, "ident",        r"func" + IDEN3,    None, None ),
    (INI_STATE, "func",         r"func",            None, None ),
    (INI_STATE, "enter",        r"enter" + IDEN3,   None, None ),
    (INI_STATE, "enter",        r"enter",           None, None ),
    (INI_STATE, "leave",        r"leave" + IDEN3,   None, None ),
    (INI_STATE, "leave",        r"leave",           None, None ),
    (INI_STATE, "return",       r"return" + IDEN3,  None, None ),
    (INI_STATE, "return",       r"return" ,         None, None ),
    (INI_STATE, "loop",         r"loop" + IDEN3,    None, None ),
    (INI_STATE, "loop",         r"loop",            None, None ),
    (INI_STATE, "extern",       r"extern",          None, None ),

    (INI_STATE, "type",         r"type" + IDEN3,    None, None ),
    (INI_STATE, "type",         r"type",            None, None ),
    (INI_STATE, "aggr",         r"aggr" + IDEN3,    None, None ),
    (INI_STATE, "aggr",         r"aggr",            None, None ),
    (INI_STATE, "enum",         r"enum"  + IDEN3,   None, None ),
    (INI_STATE, "enum",         r"enum",            None, None ),

    (INI_STATE, "float",        r"float",           None, None ),
    (INI_STATE, "double",       r"double",          None, None ),
    (INI_STATE, "quad",         r"quad",            None, None ),

    (INI_STATE, "decl",         r"[sS]8",           None, None ),
    (INI_STATE, "decl",         r"[sS]16" ,         None, None ),
    (INI_STATE, "decl",         r"[sS]32" ,         None, None ),
    (INI_STATE, "decl",         r"[sS]64" ,         None, None ),
    (INI_STATE, "decl",         r"[sS]128",         None, None ),
    (INI_STATE, "decl",         r"[uU]8",            None, None ),
    (INI_STATE, "decl",         r"[uU]16" ,         None, None ),
    (INI_STATE, "decl",         r"[uU]32" ,         None, None ),
    (INI_STATE, "decl",         r"[uU]64" ,         None, None ),
    (INI_STATE, "decl",         r"[uU]128",         None, None ),
    (INI_STATE, "arr",          r"arr" ,            None, None ),

    (INI_STATE, "hex",          HEX2u  ,            None, None ),
    (INI_STATE, "hex",          HEX2   ,            None, None ),
    (INI_STATE, "oct",          r"0o[0-7]+",        None, None ),
    (INI_STATE, "oct",          r"0y[0-7]+",        None, None ),
    (INI_STATE, "bin",          r"0b[0-1]+",        None, None ),
    (INI_STATE, "bin",          r"0z[0-1]+",        None, None ),

    (INI_STATE, "comm4d",       r"\#\#.*\n",        None, None ),
    (INI_STATE, "comm4",        r"\#.*\n" ,         None, None ),
    (INI_STATE, "comm2d",       r"\/\/\/.*\n",      None, None ),
    (INI_STATE, "comm2",        r"\/\/.*\n",        None, None ),

    (INI_STATE, "num2",         FLOATX  ,           None, None),
    (INI_STATE, "num",          r"[-]*[0-9]+",      None, None),

    (INI_STATE, "bs",           "\b"    ,           None, None),
    (INI_STATE, "quote",        r"\""   ,  STR_STATE, lexfunc.func_start_str),
    (INI_STATE, "squote",       r"\'"   ,  STR2_STATE,lexfunc.func_start_str),
    (INI_STATE, "ident",        IDEN2   ,           None, None),

    (INI_STATE, "<<",           r"<<"   ,           None, None),  # Shift left <<
    (INI_STATE, ">>",           r">>"   ,           None, None),  # Shift right >>
    (INI_STATE, "<<<",          r"<<<"  ,           None, None),  # Rotate left <<<
    (INI_STATE, ">>>",          r">>>"  ,           None, None),  # Rotate right >>>
    (INI_STATE, "++",           r"\+\+" ,           None, None),
    (INI_STATE, "--",           r"\-\-" ,           None, None),

    (INI_STATE, "peq",          r"\+=>" ,           None, None),  # Add to
    (INI_STATE, "meq",          r"\-=>" ,           None, None),  # Sub from
    (INI_STATE, "deq",          r"=="   ,           None, None),  # Equal
    (INI_STATE, "ndeq",         r"!="   ,           None, None),  # Not Equal
    (INI_STATE, "teq",          r"==="  ,           None, None),  # Identical
    (INI_STATE, "tneq",         r"!=="  ,           None, None),  # Not Identical
    (INI_STATE, "=>",           r"=>"   ,           None, None),  # Assignment
    (INI_STATE, "=",            r"="    ,           None, None),  # Assignment
    (INI_STATE, "dref",         r"->"   ,           None, None),  # Reference
    (INI_STATE, "aref",         r"<-"   ,           None, None),  # De ref
    (INI_STATE, "idev",         r"\/\%" ,           None, None),  # Int divide
    (INI_STATE, "and",          r"\&\&" ,           None, None),  # Logical and
    (INI_STATE, "or",           r"\|\|" ,           None, None),  # Logical or
    (INI_STATE, "xor",          r"\^\^" ,           None, None),  # Logical xor

    (INI_STATE, "at",           r"@"    ,           None, None),  # At
    (INI_STATE, "excl",         r"!"    ,           None, None),  # Not
    (INI_STATE, "tilde",        r"~"    ,           None, None),  # Tilde
    (INI_STATE, "under",        r"_"    ,           None, None),  # Underscore

    (INI_STATE, "comm3d",       r"\/\*\*",          COMM_STATED, None),
    (INI_STATE, "comm3",        r"\/\*" ,           COMM_STATE, None),

    (INI_STATE, "(",            r"\("   ,           None, None),
    (INI_STATE, ")",            r"\)"   ,           None, None),
    (INI_STATE, "<",            r"<"    ,           None, None),
    (INI_STATE, ">",            r">"    ,           None, None),
    (INI_STATE, "&",            r"&"    ,           None, None),
    (INI_STATE, "expo",         r"\*\*" ,           None, None),
    (INI_STATE, "*",            r"\*"   ,           None, None),
    (INI_STATE, "+",            r"\+"   ,           None, None),
    (INI_STATE, "-",            r"\-"   ,           None, None),
    (INI_STATE, "/",            r"/"    ,           None, None),
    (INI_STATE, "[",            r"\["   ,           None, None),
    (INI_STATE, "]",            r"\]"   ,           None, None),
    (INI_STATE, "{",            r"\{"   ,           None, None),
    (INI_STATE, "}",            r"\}"   ,           None, None),
    (INI_STATE, ";",            r";"    ,           None, None),  # Semi Colon
    (INI_STATE, ":",            r":"    ,           None, None),  # Colon
    (INI_STATE, "::",           r"::"   ,           None, None),  # Double colon
    (INI_STATE, "dot",          r"\."   ,           None, None),

    (INI_STATE, "caret",        r"\^"   ,           None, None),
    (INI_STATE, "cent",         r"%"    ,           None, None),

    # We parse white spaces, let the parser deal with it
    (INI_STATE, "sp",           r" "    ,           None, None),
    (INI_STATE, "tab",          r"\t"   ,           None, None),
    (INI_STATE, "nl",           r"\n"   ,           None, None),
    (INI_STATE, ",",            r","    ,           None, None),

    (INI_STATE, "any",          r"."    ,           None, None),

    # String states
    (STR_STATE, "sbsla",        r"\\"   ,           ESC_STATE, lexfunc.func_start_esc),
    (STR_STATE, "dquote",       r"\""   ,           POP_STATE, None),
    (STR_STATE, "sany",         r"."    ,           None, None),

    # string2 states
    (STR2_STATE, "sbsla2",     r"\\"    ,           ESC_STATE, None),
    (STR2_STATE, "dquote2",    r"\'"    ,            POP_STATE, None),
    (STR2_STATE, "sany2",      r"."     ,           None, None),

    # comm states
    (COMM_STATE,  "ecomm3",     r"\*\/" ,           POP_STATE, None ),
    (COMM_STATE,  "cany",      "(?s)."  ,            None, None ),
    (COMM_STATED, "ecomm3d",    r"\*\/" ,            POP_STATE, None ),
    (COMM_STATED, "canyd",     r"(?s)." ,            None, None ),

    # escape states
    #(ESC_STATE, "squote",      r"\'"   ,           None, None ),
    (ESC_STATE, "anyx",        r"."     ,           None, None ),

    # unicode states
    (UNI_STATE, "unihex",      r"[0-9A-Fa-f]{4,8}",         None, None ),
    (UNI_STATE, "anyu",        r"."     ,           None, None ),

    # hex characters
    (HEX_STATE, "eschex",      r"[0-9A-Fa-f]{1,2}", None, None ),
    (HEX_STATE, "anyh",        r"."     ,           None, None ),
    )

except KeyError as err:
    print("Cannot precomp", err, sys.exc_info())
    raise

# EOF
