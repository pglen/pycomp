#!/usr/bin/env python3

''' This is a parser skeleton for language development
        This file defines the tokens and parser states
'''

#from __future__ import absolute_import
from __future__ import print_function

import  complib.parser as parser
import  complib.lexdef as lexdef

from complib.utils import *

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

parser.IGNORE   = [punique(),      "ignore"]
parser.INIT     = [punique(),      "init"]
parser.SPAN     = [punique(),      "span"]
parser.SPANTXT  = [punique(),      "spantxt"]
parser.IDENT    = [punique(),      "ident"]
parser.KEY      = [punique(),      "key"]
parser.VAL      = [punique(),      "val"]
parser.EQ       = [punique(),      "eq"]
parser.KEYVAL   = [punique(),      "keyval"]
parser.ITALIC   = [punique(),      "italic"]
parser.EITALIC  = [punique(),      "eitalic"]
parser.BOLD     = [punique(),      "bold"]
parser.EBOLD    = [punique(),      "ebold"]
parser.ITBOLD   = [punique(),      "itbold"]
parser.EITBOLD  = [punique(),      "eitbold"]
parser.UL       = [punique(),      "ul"]
parser.EUL      = [punique(),      "eul"]
parser.DUL      = [punique(),      "dul"]
parser.EDUL     = [punique(),      "edul"]
parser.RED      = [punique(),      "red"]
parser.ERED     = [punique(),      "ered"]
parser.BGRED    = [punique(),     "bgred"]
parser.EBGRED   = [punique(),    "ebgred"]
parser.GREEN    = [punique(),      "green"]
parser.EGREEN   = [punique(),      "egreen"]
parser.BGGREEN  = [punique(),    "bggreen"]
parser.EBGGREEN = [punique(),    "ebggreen"]
parser.BLUE     = [punique(),      "blue"]
parser.EBLUE    = [punique(),      "eblue"]
parser.BGBLUE   = [punique(),    "bgblue"]
parser.EBGBLUE  = [punique(),    "ebgblue"]
parser.STRIKE   = [punique(),      "strike"]
parser.ESTRIKE  = [punique(),      "estrike"]
parser.LARGE    = [punique(),       "large"]
parser.ELARGE   = [punique(),       "elarge"]
parser.XLARGE   = [punique(),      "xlarge"]
parser.EXLARGE  = [punique(),      "exlarge"]
parser.XXLARGE  = [punique(),     "xlarge"]
parser.EXXLARGE = [punique(),     "exlarge"]
parser.SMALL    = [punique(),       "small"]
parser.ESMALL   = [punique(),       "esmall"]
parser.XSMALL   = [punique(),      "xsmall"]
parser.EXSMALL  = [punique(),      "exsmall"]
parser.CENT     = [punique(),        "cent"]
parser.ECENT    = [punique(),        "ecent"]
parser.RIGHT    = [punique(),       "right"]
parser.ERIGHT   = [punique(),       "eright"]
parser.WRAP     = [punique(),        "wrap"]
parser.EWRAP    = [punique(),        "ewrap"]
parser.LINK     = [punique(),        "link"]
parser.ELINK    = [punique(),        "elink"]
parser.IMAGE    = [punique(),       "image"]
parser.EIMAGE   = [punique(),       "eimage"]
parser.SUB      = [punique(),         "sup"]
parser.ESUB     = [punique(),         "esup"]
parser.SUP      = [punique(),         "sub"]
parser.ESUP     = [punique(),         "esub"]
parser.FILL     = [punique(),        "fill"]
parser.EFILL    = [punique(),        "efill"]
parser.FIXED    = [punique(),       "fixed"]
parser.EFIXED   = [punique(),       "efixed"]
parser.INDENT   = [punique(),      "indent"]
parser.EINDENT  = [punique(),      "eindent"]
parser.MARGIN   = [punique(),      "margin"]
parser.EMARGIN  = [punique(),      "emargin"]
parser.LMARGIN  = [punique(),     "lmargin"]
parser.ELMARGIN = [punique(),     "elmargin"]
parser.HID      = [punique(),         "hid"]
parser.EIHID    = [punique(),        "ehid"]
parser.NCOL     = [punique(),        "ncol"]
parser.ENCOL    = [punique(),        "encol"]
parser.NBGCOL   = [punique(),      "nbgcol"]
parser.ENBNCOL  = [punique(),      "enbgcol"]

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
TXTCLASS = lexdef.tok2["ident"], lexdef.tok2["eq"], lexdef.tok2["lt"], \
            #lexdef.tok2["str"], lexdef.tok2["str2"],                     \
            # lexdef.tok2["str3"],
            # lexdef.tok2["gt"], lexdef.tok2["nl"],\
            #     lexdef.tok2["sp"], lexdef.tok2["any"],

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

    [ parser.INIT,      None,   None,                    TXTCLASS,  cb.Text,     parser.IGNORE, 0 ],
    [ parser.SPAN,      None,   lexdef.tok2["ident"],    None,      None,        parser.KEY, 1 ],
    [ parser.KEYVAL,    None,   lexdef.tok2["ident"],    None,      cb.Keyval,   parser.KEY, 1 ],
    [ parser.KEY,       None,   lexdef.tok2["eq"],       None,      None,        parser.VAL, 1 ],
    [ parser.VAL,       None,   lexdef.tok2["ident"],    None,      cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.VAL,       None,   lexdef.tok2["str"],      None,      cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.VAL,       None,   lexdef.tok2["str2"],     None,      cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.VAL,       None,   lexdef.tok2["str4"],     None,      cb.Keyval,   parser.IGNORE, 0 ],
    [ parser.SPAN,      None,   lexdef.tok2["sp"],       None,      None,        parser.IGNORE, 0 ],

    [ parser.SPANTXT,   None,   None,                   TXTCLASS,   cb.Text,        parser.IGNORE, 0 ],
    [ parser.ITALIC,    None,   None,                   TXTCLASS,   cb.Text,        parser.IGNORE, 0 ],
    [ parser.BOLD,      None,   None,                   TXTCLASS,   cb.Text,        parser.IGNORE, 0 ],
    ]

PARSE_IF, PARSE_ARG, PARSE_VAL = range(3)

parser.table = [
    #[parser.PARSE_IF, lexdef.tok2["if"], lexdef.tok2["paren"],
        [ lexdef.tok2["if"], lexdef.tok2["paren"], ],
    ]

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
