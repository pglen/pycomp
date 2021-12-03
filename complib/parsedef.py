#!/usr/bin/env python3

''' This is a parser skeleton for language development
        This file defines the tokens and parser states
'''

#from __future__ import absolute_import
from __future__ import print_function

import  complib.parser as parser
import  complib.stack as stack
import  complib.lexdef as lexdef
import  complib.lexer as lexer
import  complib.lexdef as lexdef

# This parser digests formatted text similar to what the 'C' language does
# Was created to quickly write assempbler fragments
# See SYNTAX for details on text formats

# Connect parser token to lexer item. This way the definitions are synced
# without the need for double definition

# Quick into: The lexer creates a stack of tokens. The parser scans
# the tokens, and walks the state machine for matches. If match
# is encountered, the parser calls the function in the state table,
# and / or changes state. Reduce is called after the state has been
# successfully digested. For more info see lex / yacc literature.

# ------------------------------------------------------------------------
# Parser state machine states. The state machine runs through the whole
# file stepping the rules. The functions may do anything, including reduce.
# Blank reduce may be executed with the state transition set to 'REDUCE'
#
# The number is the state, the string is for debugging / analyzing
# Once ready, operate on the numbers for speed.
# The E-states are not used, kept it for extensibility.

parser.IGNORE   = [parser.punique(),      "ignore"]
parser.INIT     = [parser.punique(),      "init"]
parser.SPAN     = [parser.punique(),      "span"]
parser.SPANTXT  = [parser.punique(),      "spantxt"]
parser.IDENT    = [parser.punique(),      "ident"]
parser.KEY      = [parser.punique(),      "key"]
parser.VAL      = [parser.punique(),      "val"]
parser.EQ       = [parser.punique(),      "eq"]
parser.KEYVAL   = [parser.punique(),      "keyval"]
parser.ITALIC   = [parser.punique(),      "italic"]
parser.EITALIC  = [parser.punique(),      "eitalic"]
parser.BOLD     = [parser.punique(),      "bold"]
parser.EBOLD    = [parser.punique(),      "ebold"]
parser.ITBOLD   = [parser.punique(),      "itbold"]
parser.EITBOLD  = [parser.punique(),      "eitbold"]
parser.UL       = [parser.punique(),      "ul"]
parser.EUL      = [parser.punique(),      "eul"]
parser.DUL      = [parser.punique(),      "dul"]
parser.EDUL     = [parser.punique(),      "edul"]
parser.RED      = [parser.punique(),      "red"]
parser.ERED     = [parser.punique(),      "ered"]
parser.BGRED    = [parser.punique(),     "bgred"]
parser.EBGRED   = [parser.punique(),    "ebgred"]
parser.GREEN    = [parser.punique(),      "green"]
parser.EGREEN   = [parser.punique(),      "egreen"]
parser.BGGREEN  = [parser.punique(),    "bggreen"]
parser.EBGGREEN = [parser.punique(),    "ebggreen"]
parser.BLUE     = [parser.punique(),      "blue"]
parser.EBLUE    = [parser.punique(),      "eblue"]
parser.BGBLUE   = [parser.punique(),    "bgblue"]
parser.EBGBLUE  = [parser.punique(),    "ebgblue"]
parser.STRIKE   = [parser.punique(),      "strike"]
parser.ESTRIKE  = [parser.punique(),      "estrike"]
parser.LARGE    = [parser.punique(),       "large"]
parser.ELARGE   = [parser.punique(),       "elarge"]
parser.XLARGE   = [parser.punique(),      "xlarge"]
parser.EXLARGE  = [parser.punique(),      "exlarge"]
parser.XXLARGE  = [parser.punique(),     "xlarge"]
parser.EXXLARGE = [parser.punique(),     "exlarge"]
parser.SMALL    = [parser.punique(),       "small"]
parser.ESMALL   = [parser.punique(),       "esmall"]
parser.XSMALL   = [parser.punique(),      "xsmall"]
parser.EXSMALL  = [parser.punique(),      "exsmall"]
parser.CENT     = [parser.punique(),        "cent"]
parser.ECENT    = [parser.punique(),        "ecent"]
parser.RIGHT    = [parser.punique(),       "right"]
parser.ERIGHT   = [parser.punique(),       "eright"]
parser.WRAP     = [parser.punique(),        "wrap"]
parser.EWRAP    = [parser.punique(),        "ewrap"]
parser.LINK     = [parser.punique(),        "link"]
parser.ELINK    = [parser.punique(),        "elink"]
parser.IMAGE    = [parser.punique(),       "image"]
parser.EIMAGE   = [parser.punique(),       "eimage"]
parser.SUB      = [parser.punique(),         "sup"]
parser.ESUB     = [parser.punique(),         "esup"]
parser.SUP      = [parser.punique(),         "sub"]
parser.ESUP     = [parser.punique(),         "esub"]
parser.FILL     = [parser.punique(),        "fill"]
parser.EFILL    = [parser.punique(),        "efill"]
parser.FIXED    = [parser.punique(),       "fixed"]
parser.EFIXED   = [parser.punique(),       "efixed"]
parser.INDENT   = [parser.punique(),      "indent"]
parser.EINDENT  = [parser.punique(),      "eindent"]
parser.MARGIN   = [parser.punique(),      "margin"]
parser.EMARGIN  = [parser.punique(),      "emargin"]
parser.LMARGIN  = [parser.punique(),     "lmargin"]
parser.ELMARGIN = [parser.punique(),     "elmargin"]
parser.HID      = [parser.punique(),         "hid"]
parser.EIHID    = [parser.punique(),        "ehid"]
parser.NCOL     = [parser.punique(),        "ncol"]
parser.ENCOL    = [parser.punique(),        "encol"]
parser.NBGCOL   = [parser.punique(),      "nbgcol"]
parser.ENBNCOL  = [parser.punique(),      "enbgcol"]

# ------------------------------------------------------------------------
# State groups for recursion:

# Color instructions: (not used)

STATECOL = [parser.RED, parser.GREEN, parser.BLUE]

# These are states that have recursive actions:
# (like bold in italic or size in color etc ...) Note specifically, that
# the SPAN state is not in this list, as inside span definitions formatting
# does not make sence. This parser ignores such occurances.

STATEFMT = [parser.INIT,  parser.BOLD, parser.ITALIC, parser.RED,
            parser.GREEN, parser.BLUE, parser.BGRED, parser.BGGREEN,
            parser.BGBLUE, parser.UL, parser.DUL, parser.STRIKE,
            parser.SMALL, parser.NCOL, parser.NBGCOL, parser.XSMALL,
            parser.LARGE, parser.XLARGE, parser.XXLARGE,
            parser.SUB, parser.SUP, parser.LINK, parser.CENT,
            parser.RIGHT, parser.WRAP, parser.FILL, parser.INDENT,
            parser.SPANTXT, parser.FIXED, parser.MARGIN, parser.LMARGIN ]

# ------------------------------------------------------------------------
# Text display state:

class ParseState():

    def __init__(self):

        self.font = ""
        self.bold = False;  self.itbold = False;   self.italic = False
        self.ul = False; self.dul = False
        self.red = False;  self.blue = False; self.green = False
        self.bgred = False;  self.bgblue = False; self.bggreen = False
        self.strike = False; self.large = False; self.small = False; self.xsmall = False
        self.xlarge = False; self.xxlarge = False; self.center = False
        self.wrap = False; self.hidden = False; self.color =  ""; self.right = False
        self.indent = 0; self.margin = 0; self.size = 0; self.font = "";
        self.fixed = False; self.bgcolor = ""
        self.sub = False; self.sup = False; self.image = ""; self.link = ""; self.lmargin = 0
        self.fill = False; self.tab = 0

    def clear(self):
        for aa in self.__dict__:
            if aa[:2] == "__":
                continue
            if isinstance(self.__dict__[aa], bool):
                   self.__dict__[aa] = False
            elif isinstance(self.__dict__[aa], int):
                   self.__dict__[aa] = 0
            elif isinstance(self.__dict__[aa], str):
                   self.__dict__[aa] = ""
            else:
                print ("  Other", aa, type(self.__dict__[aa]))
                pass

# ------------------------------------------------------------------------
# Class of tokens for simple alternates:

# This token class is for generic text.
TXTCLASS = lexdef.tokdef["ident"], lexdef.tokdef["eq"], lexdef.tokdef["lt"], \
            lexdef.tokdef["str"], lexdef.tokdef["str2"],                     \
             lexdef.tokdef["str3"], lexdef.tokdef["gt"], lexdef.tokdef["nl"],\
                 lexdef.tokdef["sp"], lexdef.tokdef["any"],

ts = ParseState()

# Callback class, extraction of callback functions from the pangview parser.
# The class ParseState is the format controlling class, Mainview is the target
# window, and the Emit() function is to aid debug. These funtions may also
# manipulate the parser stack. Note the naming convention like Bold() for
# bold start, eBold() for bold end.

class parserCallBack():

    def __init__(self, ParseState, Emit, Pvg):
        self.ParseState = ParseState
        self.emit = Emit
        self.pvg = Pvg
        self.oldstate = None

    def Token(self, tk):
        print("Token", tk)
        pass

    def Span(self):
        pass
    def Bold(self):
        pass
    def Italic(self):
        pass
    def ItBold(self):
        pass
    def Underlin(self):
        pass
    def Dunderli(self):
        pass
    def Red(self):
        pass
    def Bgred(self):
        pass
    def Blue(self):
        pass
    def Bgblue(self):
        pass
    def Green(self):
        pass
    def Bggreen(self):
        pass
    def Strike(self):
        pass
    def Large(self):
        pass
    def Xlarge(self):
        pass
    def Xxlarge(self):
        pass
    def Small(self):
        pass
    def Xsmall(self):
        pass
    def Center(self):
        pass
    def Right(self):
        pass
    def Wrap(self):
        pass
    def Link(self):
        pass
    def Image(self):
        pass
    def Sub(self):
        pass
    def Sup(self):
        pass
    def Fill(self):
        pass
    def Fixed(self):
        pass
    def Indent(self):
        pass
    def Margin(self):
        pass
    def Lmargin(self):
        pass
    def Hid(self):
        pass
    def Ncol(self):
        pass
    def Ncol2(self):
        pass
    def Nbgcol(self):
        pass
    def Text(self, arg1, arg2, arg3):
        #print("text", arg1, arg2, arg3)
        pass
    def Keyval(self):
        #print("keyval")
        pass

def emit(sss):
    print("sss", sss)

cb = parserCallBack(ts, emit, None)

# ------------------------------------------------------------------------
# Parse table.
#
# Specify state machine state, token to see for action or class to see for
# action, function to execute when match encountered, the new parser
# state when match encountered, continuation flag for reduce. (will
# reduce until cont flag == 0) See reduce example for key->val.
#
# Alternatives can be specified with multiple lines for the same state.
# New parser state field overrides state set by function. (set to IGNORE)
#
# Parser ignores unmatched entries.
#    (Bad for languages, good for error free parsing like text parsing)
#
# Parser starts in INIT. Parser skips IGNORE. (in those cases, usually
# the function sets the new state)
#
# Use textual context for development, numeric for production
#
# This table specifies a grammar for text processing, similar to Pango
#
#     -- State -- StateClass -- Token -- TokenClass -- Function -- newState -- cont. flag

parser.parsetable = [

    [ parser.INIT,   None,   None,                      TXTCLASS, cb.Text,     parser.IGNORE, 0 ],
    [ parser.SPAN,   None,   lexdef.tokdef["ident"],    None,     None,        parser.KEY, 1 ],
    [ parser.KEYVAL, None,   lexdef.tokdef["ident"],    None,     cb.Keyval,   parser.KEY, 1 ],
    [ parser.KEY,    None,   lexdef.tokdef["eq"],       None,     None,        parser.VAL, 1 ],
    [ parser.VAL,    None,   lexdef.tokdef["ident"],    None,     cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.VAL,    None,   lexdef.tokdef["str"],      None,     cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.VAL,    None,   lexdef.tokdef["str2"],     None,     cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.VAL,    None,   lexdef.tokdef["str4"],     None,     cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.SPAN,   None,   lexdef.tokdef["sp"],       None,     None,        parser.IGNORE, 0 ],

    [ parser.SPANTXT, None, None,            TXTCLASS,      cb.Text,    parser.IGNORE, 0 ],
    [ parser.ITALIC,   None, None,           TXTCLASS,     cb.Text,     parser.IGNORE, 0 ],
    [ parser.BOLD,     None, None,           TXTCLASS,     cb.Text,     parser.IGNORE, 0 ],
    ]

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
