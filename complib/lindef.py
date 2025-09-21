#!/usr/bin/env python

''' Definitions for the linear parser

# We initialize parser variables in the context of the parser module.
#
# The parser will look up if current state is in the list of parser states.
#   If there is a match, the tokens are compared. If there is a match, the
#   new parser state is set, and the specified parser function is executed.
#   This parser has limited need for backtracking, as the grammer concept
#   is sentence based. The termination of the sentence is either a new
#   line or a semi colon.
# Examples:
#    u32 : varname = varval ;
#    func callme("hello World")
# Space / Tab is skipped / ignored, newline and ';' is interpretd as a
# sequence terminator,  See grammer spec for more details.

'''

from complib.utils import *
from complib.linfunc  import *
import complib.lexdef  as lexdef

def defpvg(xpvg):
    global pvg
    pvg = xpvg
    #print("got pvg", pvg)

class Stamp:

    ''' The class that holds the token descriptions for the parser '''

    def __init__(self, statex, tokenx, nstatex, dncall, upcall, pushx,
                                groupx = None, flagsx = None):
        # Extend to array if a number passed
        if type(statex) == type(0):
            self.state = (statex,)
            #print("type cast", self.state)
        else:
            self.state  = statex
        # Extend to array if a number passed
        if type(tokenx) == type(""):
            self.tokens  = (tokenx,)
            #print("token type cast", self.token)
        else:
            self.tokens  = tokenx

        self.nstate = nstatex
        self.push   = pushx
        self.dncall = dncall
        self.upcall = upcall
        self.group  = groupx
        self.flags  = flagsx

    def dump(self):

        states =  ""
        for aa in self.state:
            states += ST.get(aa) + " "
        strx  =  "[ " + states + " "
        tokens = ""
        for aa in self.tokens:
            tokens += aa + " "
        strx +=  pp(tokens) + " "
        strx +=  ST.get(self.nstate) + " ]"
        return strx

    def __str__(self):

        states =  ""
        for aa in self.state:
            states += ST.get(aa) + " "
        if self.upcall:
            fname = str(self.upcall.__name__)
        else:
            fname = "NoUPFunc"
        if self.dncall:
            fnameD = str(self.dncall.__name__)
        else:
            fnameD = "NoDNFunc"

        strx = "cState: " + states + " "  + pp(str(self.tokens)) \
                + " nState: " + ST.get(self.nstate) + " " + fnameD \
                + " " + fname + " " + str(self.push)
        return strx

# List of identities for declaration
IDEN = ("ident", "num", "num2", "str", "arr", "float", "dbl",  "dbl2", )

# Changed to auto add new state (note: no dup checking)
ST = linpool.Xenum()
def C(vvv):
    return ST.val(vvv)

# Compund states for matching multiple states
STBASE =  C("STATEINI"), C("SFUNBODY")

# Parse tables consist of:
#       a.) Parser state or states
#       b.) Token definition or tokens
#       c.) New parser state
#       e.) Parser function to call on up state
#       f.) Parser function to call on down state
#       g.) Push flag
#
# To create a custom rule, just add new tokens / states in
#   the definition section. the D* declarations are xtracted subsections.

# The entries to be matched agains the parse array.
# state(s)  token(s)  newState  downFunction  upFunction  pushFlag
# -------   -------   --------  ------------- ----------- --------

Dfuncx = ( \
    # Function Declaration
    Stamp(C("STATEANY"),  "func",   C("STFUNC"),    None,  None, False),
    Stamp(C("STFUNC"),    "ident",  C("STFUNC2"),   None,  funcs.start, False),
    Stamp(C("STFUNC2"),   "(",      C("SFUNARG"),   None,  None, False),
    Stamp(C("SFUNARG"),   "decl",   C("SFUNARG2"),  None,  funcs.arg_start, False),
    Stamp(C("SFUNARG2"),  ":",      C("SFUNARG3"),  None,  None, False),
    Stamp(C("SFUNARG3"),  "ident",  C("SFUNARG4"),  None,  None, False),
    Stamp(C("SFUNARG4"),  ",",      C("SFUNARG3"),  None,  None, False),
    Stamp(C("SFUNARG4"),  "=",      C("SFUNARG4"),  None,  None, False),
    Stamp(C("SFUNARG4"),  "ident",  C("SFUNARG3"),  None,  None, False),
    Stamp(C("SFUNARG4"),  "num",    C("SFUNARG3"),  None,  None, False),
    Stamp(C("SFUNARG3"),  "nl",     C("STPOP"),     None,  None, False),
    Stamp(C("SFUNARG3"),  "comm2",  C("STPOP"),     None,  None, False),

    Stamp(C("SFUNARG"),  ")",      C("STFUNC3"),    None,  funcs.args, False),
    Stamp(C("SFUNARG3"), ")",      C("STFUNC3"),    None,  funcs.args, False),
    Stamp(C("STFUNC3"),  "{",      C("SFUNBODY"),   None,  None, False),
    Stamp(C("SFUNBODY"), "return", C("SFUNCRET"),   None,  None, False),
    Stamp(C("SFUNCRET"), "ident",  C("SFUNBODY"),   None,  None, False),
    Stamp(C("SFUNBODY"), "}",      C("STATEINI"),   None,  funcs.end, False),
    )

Drassn  = (
    # Right side assignment
    #Stamp(C("STARITH"),  "=>",     C("STRASSN3"),  None,  None, False),
    #Stamp(C("STRASSN3"), "num",    C("STRASSN4"),  None,  assn.rassn, False),
    #Stamp(C("STRASSN3"), "num2",   C("STRASSN4"),  None,  assn.rassn, False),
    #Stamp(C("STRASSN3"), "ident",  C("STRASSN4"),  None,  assn.rassn, False),
    #Stamp(C("STRASSN4"),  ";",     C("STPOP"),     None,  assn.rassn_stop, False),
    #Stamp(C("STRASSN4"),  "nl",    C("STPOP"),     None,  assn.rassn_stop, False),
    )

Dfcall  = (
    # Function call
    Stamp(C("STARITH"),   "(",      C("CFUNC3"),  None, fcall.start, False),
    Stamp(C("CFUNC3"),    "num",    C("CFUNC4"),  None, fcall.val, False),
    Stamp(C("CFUNC3"),    "ident",  C("CFUNC4"),  None, fcall.val, False),
    Stamp(C("CFUNC3"),    "str",    C("CFUNC4"),  None, fcall.val, False),

    Stamp(C("CFUNC3"),    ")",      C("STATEINI"), None, fcall.end,  False),
    Stamp(C("CFUNC4"),    ")",      C("STATEINI"), None, fcall.end,  False),

    Stamp(C("CFUNC4"),    ",",      C("CFUNC3"),    None, fcall.comma, False),
    Stamp(C("CFUNC4"),    "nl",     C("STATEINI"),  None, fcall.end,   False),
    Stamp(C("CFUNC4"),    ";",      C("STATEINI"),  None, fcall.end,   False),
    )

Dtest = (
    # Assignments / Start of arithmetic
    #Stamp(C("DECL4"), "=",         C("STARITH"),  None,  None, False),
    #Stamp(C("DECL5"), "ident",     C("DECL6"),    None,  func_decl_val, False),
    #Stamp(C("DECL5"), "num",       C("DECL6"),    None,  func_decl_val, False),
    #Stamp(C("DECL5"), "num2",      C("DECL6"),    None,  func_decl_val, False),
    #Stamp(C("DECL5"), "str",       C("DECL6"),    None,  func_decl_val, False),

    #Stamp(C("DECL6"), ",",         C("DECL3"),    None,  func_decl_comma, False),
    #Stamp(C("DECL6"), ";",         C("STPOP"),    None,  func_decl_stop, False),
    #Stamp(C("DECL6"), "nl",        C("STPOP"),    None,  func_decl_stop, False),
    #Stamp(C("DECL6"), "comm2",     C("STPOP"),    None,  func_decl_stop, False),
    #Stamp(C("DECL6"), "comm4",     C("STPOP"),    None,  func_decl_stop, False),
    #Stamp(C("DECL6"), "comm2d",    C("STPOP"),    None,  func_decl_stop, False),
    #Stamp(C("DECL6"), "comm4d",    C("STPOP"),    None,  func_decl_stop, False),

    #Stamp(C("STARITH"),  "=",      C("STASSN"),   None,  func_assn_start, False),
    #Stamp(C("STASSN"),   "ident",  C("STARITH"),  None,  func_assn, False),
    #Stamp(C("STASSN"),   "num",    C("STARITH"),  None,  func_assn, False),
    #Stamp(C("STASSN"),   "str",    C("STARITH"),  None,  func_assn, False),
    #Stamp(C("STARITH"),  ";",      C("STPOP"),    None,   func_assn_stop, False),
    #Stamp(C("STARITH"),  "nl",     C("STPOP"),    None,   func_assn_stop, False),
)

Darith = (
    # Arithmetics (+ - * / sqr assn)
    Stamp(C("STARITH"), "=",       C("SFASSN"),   None,  arith.arithop, False),
    Stamp(C("SFASSN"),  "ident",    C("STARITH"),  None,  arith.assnexpr, False),
    Stamp(C("SFASSN"),  "num",      C("STARITH"),  None,  arith.assnexpr, False),
    Stamp(C("SFASSN"),  "num2",     C("STARITH"),  None,  arith.assnexpr, False),
    Stamp(C("SFASSN"),  "str",      C("STARITH"),  None,  arith.assnexpr, False),

    Stamp(C("STARITH"), "=>",      C("SFPUT"),    None,  arith.arithop, False),
    Stamp(C("SFPUT"),   "ident",   C("STARITH"),  None,  arith.mulexpr, False),
    Stamp(C("SFPUT"),   "num",     C("STARITH"),  None,  arith.mulexpr, False),

    Stamp(C("STARITH"), "expo",    C("SFSQR"),    None,  arith.arithop, False),
    Stamp(C("SFSQR"),   "ident",   C("STARITH"),  None,  arith.expexpr, False),
    Stamp(C("SFSQR"),   "num",     C("STARITH"),  None,  arith.expexpr, False),

    #Stamp(C("STATEANY"),   "(",   C("STIGN"),    None,  misc.func_parent, False),
    #Stamp(C("STATEANY"),   ")",   C("STIGN"),    None,  misc.func_parent, False),

    #Stamp(C("SFPAR"), "ident",    C("STARITH"),  None,  None, False),
    #Stamp(C("SFPAR"), "num",      C("STARITH"),  None,  None, False),

    #Stamp(C("STARITH"), ")",      C("SFPAR2"),   None,  misc.func_parent, False),
    #Stamp(C("SFPAR2"), "ident",   C("STARITH"),  None,  arith.mulexpr, False),
    #Stamp(C("SFPAR2"), "num",     C("STARITH"),  None,  arith.mulexpr, False),

    Stamp(C("STARITH"), "*",       C("SFMUL"),    None,  arith.arithop, False),
    Stamp(C("SFMUL"),   "ident",   C("STARITH"),  None,  arith.mulexpr, False),
    Stamp(C("SFMUL"),   "num",     C("STARITH"),  None,  arith.mulexpr, False),
    Stamp(C("SFMUL"),   "num2",    C("STARITH"),  None,  arith.mulexpr, False),

    Stamp(C("STARITH"), "/",       C("SFDIV"),    None,  arith.arithop, False),
    Stamp(C("SFDIV"),   "ident",   C("STARITH"),  None,  arith.divexpr, False),
    Stamp(C("SFDIV"),   "num",     C("STARITH"),  None,  arith.divexpr, False),

    Stamp(C("STARITH"), "+",       C("SFADD"),    None,  arith.arithop, False),
    Stamp(C("SFADD"),   "ident",   C("STARITH"),  None,  arith.addexpr, False),
    Stamp(C("SFADD"),   "num",     C("STARITH"),  None,  arith.addexpr, False),
    Stamp(C("SFMUL"),   "num2",    C("STARITH"),  None,  arith.mulexpr, False),

    Stamp(C("STARITH"), "-",       C("SFSUB"),     None, arith.arithop, False),
    Stamp(C("SFSUB"),   "ident",   C("STARITH"),   None, arith.subexpr, False),
    Stamp(C("SFSUB"),   "num",     C("STARITH"),   None, arith.subexpr, False),

    Stamp(C("STARITH"), "<<",      C("SFSHIFT"),  None,  arith.arithop, False),
    Stamp(C("SFSHIFT"), "ident",   C("STARITH"),  None,  arith.expr, False),
    Stamp(C("SFSHIFT"), "num",     C("STARITH"),  None,  arith.expr, False),

    Stamp(C("STARITH"),  ">>",     C("SFRSHIFT"), None,  arith.arithop, False),
    Stamp(C("SFRSHIFT"), "ident",  C("STARITH"),  None,  arith.expr, False),
    Stamp(C("SFRSHIFT"), "num",    C("STARITH"),  None,  arith.expr, False),

    #Stamp(C("STARITH"), ";",      C("STPOP"),    None,  arith.arith_stop, False),
    #Stamp(C("STARITH"), "nl",     C("STPOP"),    None,  arith.arith_stop, False),
    )

FLOAT   = "float", "double", "quad",

Ddecl = (
    # Declarations
    Stamp(STBASE,   "decl",      C("DECL2"),   None,   decl.start, True),
    Stamp(STBASE,   FLOAT,       C("DECL2"),   None,   decl.start, True),

    Stamp(C("DECL2"),   ":",     C("DECL3"),   None,   decl.col, False),
    Stamp(C("DECL3"),   "ident", C("STARITH"), None,   decl.ident, False),
    Stamp(C("STARITH"), ",",     C("DECL3"),   None,   decl.comma, False),

    Stamp(C("STARITH"), ";",     C("STPOP"),   decl.down, None, False),
    Stamp(C("STARITH"), "nl",    C("STPOP"),   decl.down, None, False),

    Stamp(STBASE,       "arr",   C("DECLA"),   None,   decl.astart, True),
    Stamp(C("DECLA"),   ":",     C("DECLA2"),  None,   decl.acol, False),
    Stamp(C("DECLA2"),  "ident", C("STTARI"),  None,   decl.aident, False),
    Stamp(C("STTARI"),  "=",     C("STTARI2"), None,   None, False),
    Stamp(C("STTARI2"), "str",   C("STTARI3"), None,   decl.astr,    False),

    Stamp(C("STTARI3"), ",",     C("DECLA2"),  None,   decl.acomma, False),
    Stamp(C("STTARI3"), "+",     C("STTARI2"), None,   decl.aadd,   False),
    Stamp(C("STTARI3"), "*",     C("STTARI4"), None,   decl.amul,   False),
    Stamp(C("STTARI4"), "num",   C("STTARI3"), None,   decl.anum,   False),

    Stamp(C("STTARI3"), ";",     C("STPOP"),   decl.adown, None, False),
    Stamp(C("STTARI3"), "nl",    C("STPOP"),   decl.adown, None, False),
)

# Main stamps definition

stamps =  (  \

    Stamp(C("STATEINI"), "ident",   C("STARITH"),  None,  arith.arithstart, True),
    Stamp(C("STATEINI"), "extern",  C("EXTERN"),   None,  misc.extern, True),
    Stamp(C("EXTERN"),   "ident",   C("EXTERN2"),  None,  misc.extadd, False),
    Stamp(C("EXTERN"),   "str",     C("EXTERN2"),  None,  misc.extadd, False),
    Stamp(C("EXTERN2"),  ",",       C("EXTERN"),   None,  misc.extcomma, False),
    Stamp(C("EXTERN2"),  ";",       C("STPOP"),    misc.exdn,  None, False),
    Stamp(C("EXTERN2"),  "nl",      C("STPOP"),    misc.exdn,  None, False),

    # Include sub systems
    *Ddecl,
    *Darith,
    *Dfcall,
    *Dfuncx,
    *Drassn,

    # This will ignore comments
    Stamp(C("STATEANY"), "comm2",   C("STIGN"),   None,  misc.comment, False),
    Stamp(C("STATEANY"), "comm2d",  C("STIGN"),   None,  misc.dcomment, False),
    Stamp(C("STATEANY"), "comm3",   C("STIGN"),   None,  misc.comment, False),
    Stamp(C("STATEANY"), "comm3d",  C("STIGN"),   None,  misc.dcomment2, False),
    Stamp(C("STATEANY"), "comm4",   C("STIGN"),   None,  misc.comment, False),
    Stamp(C("STATEANY"), "comm4d",  C("STIGN"),   None,  misc.dcomment3, False),

    # This will ignore white spaces
    Stamp(C("STATEANY"), "tab",     C("STIGN"),   None,  misc.tab, False),
    Stamp(C("STATEANY"), "sp",      C("STIGN"),   None,  misc.space, False),
    Stamp(C("STATEANY"), "nl",      C("STIGN"),   None,  misc.nl, False),
    )

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
