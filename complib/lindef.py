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

    def __init__(self, statex, tokenx, nstatex, dncall, upcall,
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
        if self.call:
            fname = str(self.call.__name__)
        else:
            fname = "No Func"
        strx = "cState: " + states + " "  + pp(str(self.token)) \
                + " nState: " + ST.get(self.nstate) + " " + fname
        return strx

# List of identities for declaration
IDEN = ("ident", "num", "num2", "str", "arr", "float", "dbl",  "dbl2", )

# Changed to auto add new state (note: no dup checking)
ST = linpool.Xenum()

# Compund states for matching multiple states
STBASE =  ST.val("STATEINI"), ST.val("SFUNBODY")

# Parse tables consist of:
#       a.) Parser states
#       b.) Token(s) definition
#       c.) New parser state
#       d.) Parser functions to call
#
# To create a custom rul, just add new tokens / states in
#   the definition section. the D* declarations are xtracted subsections.

# These are the entries to be matched agains the parse array.
#    states     token or list       new_state       down function     up function
#    ------     -------------       ----------      -------------     -----------

Dfuncx = ( \
    # Function Declaration
    Stamp(ST.val("STATEANY"),  "func",   ST.val("STFUNC"),    None,  None),
    Stamp(ST.val("STFUNC"),    "ident",  ST.val("STFUNC2"),   None,  funcs.func_start),
    Stamp(ST.val("STFUNC2"),   "(",      ST.val("SFUNARG"),   None,  None),
    Stamp(ST.val("SFUNARG"),   "decl",   ST.val("SFUNARG2"),  None,  funcs.func_arg_start),
    Stamp(ST.val("SFUNARG2"),  ":",      ST.val("SFUNARG3"),  None,  None),
    Stamp(ST.val("SFUNARG3"),  "ident",  ST.val("SFUNARG4"),  None,  None),
    Stamp(ST.val("SFUNARG4"),  ",",      ST.val("SFUNARG3"),  None,  None),
    Stamp(ST.val("SFUNARG4"),  "=",      ST.val("SFUNARG4"),  None,  None),
    Stamp(ST.val("SFUNARG4"),  "ident",  ST.val("SFUNARG3"),  None,  None),
    Stamp(ST.val("SFUNARG4"),  "num",    ST.val("SFUNARG3"),  None,  None),
    Stamp(ST.val("SFUNARG3"),  "nl",     ST.val("STPOP"),     None,  None),
    Stamp(ST.val("SFUNARG3"),  "comm2",  ST.val("STPOP"),     None,  None),

    Stamp(ST.val("SFUNARG"),  ")",      ST.val("STFUNC3"),    None,  funcs.func_args),
    Stamp(ST.val("SFUNARG3"), ")",      ST.val("STFUNC3"),    None,  funcs.func_args),
    Stamp(ST.val("STFUNC3"),  "{",      ST.val("SFUNBODY"),   None,  None),
    Stamp(ST.val("SFUNBODY"), "return", ST.val("SFUNCRET"),   None,  None),
    Stamp(ST.val("SFUNCRET"), "ident",  ST.val("SFUNBODY"),   None,  None),
    Stamp(ST.val("SFUNBODY"), "}",      ST.val("STATEINI"),   None,  funcs.func_end),
    )

Drassn  = (
    # Right side assignment
    #Stamp(ST.val("STARITH"),  "=>",     ST.val("STRASSN3"),  None,  None),
    #Stamp(ST.val("STRASSN3"), "num",    ST.val("STRASSN4"),  None,  assn.rassn),
    #Stamp(ST.val("STRASSN3"), "num2",   ST.val("STRASSN4"),  None,  assn.rassn),
    #Stamp(ST.val("STRASSN3"), "ident",  ST.val("STRASSN4"),  None,  assn.rassn),
    #Stamp(ST.val("STRASSN4"),  ";",     ST.val("STPOP"),     None,  assn.rassn_stop),
    #Stamp(ST.val("STRASSN4"),  "nl",    ST.val("STPOP"),     None,  assn.rassn_stop),
    )

Dfcall  = (
    # Function call
    #Stamp(ST.val("STARITH"),   "(",      ST.val("SFUNARG"),  None,  None),
    #Stamp(ST.val("SFUNARG"),   "ident",  ST.val("CFUNC2"),  None,  None),
    #Stamp(ST.val("SFUNBODY"),  "ident",  ST.val("CFUNC2"),  None,  None),

    Stamp(ST.val("STARITH"),   "(",      ST.val("CFUNC3"),  None, funcs.call_start),
    #Stamp(ST.val("CFUNC2"),    "(",      ST.val("CFUNC3"),  None, funcs.func_call),
    Stamp(ST.val("CFUNC3"),    "num",    ST.val("CFUNC4"),  None, funcs.call_decl_val),
    Stamp(ST.val("CFUNC3"),    "ident",  ST.val("CFUNC4"),  None, funcs.call_decl_val),
    Stamp(ST.val("CFUNC3"),    "str",    ST.val("CFUNC4"),  None, funcs.call_decl_val),
    Stamp(ST.val("CFUNC3"),    ")",      ST.val("STPOP"),   None, funcs.call_end),
    Stamp(ST.val("CFUNC4"),    ",",      ST.val("CFUNC3"),  None, None),
    Stamp(ST.val("CFUNC4"),    ")",      ST.val("STPOP"),   None,  funcs.call_end),
    )

Dtest = (
    # Assignments / Start of arithmetic
    #Stamp(ST.val("DECL4"), "=",         ST.val("STARITH"),  None,  None),
    #Stamp(ST.val("DECL5"), "ident",     ST.val("DECL6"),    None,  func_decl_val),
    #Stamp(ST.val("DECL5"), "num",       ST.val("DECL6"),    None,  func_decl_val),
    #Stamp(ST.val("DECL5"), "num2",      ST.val("DECL6"),    None,  func_decl_val),
    #Stamp(ST.val("DECL5"), "str",       ST.val("DECL6"),    None,  func_decl_val),

    #Stamp(ST.val("DECL6"), ",",         ST.val("DECL3"),    None,  func_decl_comma),
    #Stamp(ST.val("DECL6"), ";",         ST.val("STPOP"),    None,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "nl",        ST.val("STPOP"),    None,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm2",     ST.val("STPOP"),    None,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm4",     ST.val("STPOP"),    None,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm2d",    ST.val("STPOP"),    None,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm4d",    ST.val("STPOP"),    None,  func_decl_stop),

    #Stamp(ST.val("STARITH"),  "=",      ST.val("STASSN"),   None,  func_assn_start),
    #Stamp(ST.val("STASSN"),   "ident",  ST.val("STARITH"),  None,  func_assn),
    #Stamp(ST.val("STASSN"),   "num",    ST.val("STARITH"),  None,  func_assn),
    #Stamp(ST.val("STASSN"),   "str",    ST.val("STARITH"),  None,  func_assn),
    #Stamp(ST.val("STARITH"),  ";",      ST.val("STPOP"),    None,   func_assn_stop),
    #Stamp(ST.val("STARITH"),  "nl",     ST.val("STPOP"),    None,   func_assn_stop),
)

Darith = (
    # Arithmetics (+ - * / sqr assn)
    Stamp(ST.val("STARITH"), "=",       ST.val("SFASSN"),   None,  arith.arithop),
    Stamp(ST.val("SFASSN"), "ident",    ST.val("STARITH"),  None,  arith.assnexpr),
    Stamp(ST.val("SFASSN"), "num",      ST.val("STARITH"),  None,  arith.assnexpr),
    Stamp(ST.val("SFASSN"), "str",      ST.val("STARITH"),  None,  arith.assnexpr),

    Stamp(ST.val("STARITH"), "=>",      ST.val("SFPUT"),    None,  arith.arithop),
    Stamp(ST.val("SFPUT"), "ident",     ST.val("STARITH"),  None,  arith.mulexpr),
    Stamp(ST.val("SFPUT"), "num",       ST.val("STARITH"),  None,  arith.mulexpr),

    Stamp(ST.val("STARITH"), "expo",    ST.val("SFSQR"),    None,  arith.arithop),
    Stamp(ST.val("SFSQR"),   "ident",   ST.val("STARITH"),  None,  arith.expexpr),
    Stamp(ST.val("SFSQR"),   "num",     ST.val("STARITH"),  None,  arith.expexpr),

    #Stamp(ST.val("STATEANY"),   "(",     ST.val("STIGN"),    None,  misc.func_parent),
    #Stamp(ST.val("STATEANY"),   ")",     ST.val("STIGN"),    None,  misc.func_parent),

    #Stamp(ST.val("SFPAR"), "ident",     ST.val("STARITH"),  None,  None),
    #Stamp(ST.val("SFPAR"), "num",       ST.val("STARITH"),  None,  None),

    #Stamp(ST.val("STARITH"), ")",       ST.val("SFPAR2"),   None,  misc.func_parent),
    #Stamp(ST.val("SFPAR2"), "ident",    ST.val("STARITH"),  None,  arith.mulexpr),
    #Stamp(ST.val("SFPAR2"), "num",      ST.val("STARITH"),  None,  arith.mulexpr),

    Stamp(ST.val("STARITH"), "*",       ST.val("SFMUL"),    None,  arith.arithop),
    Stamp(ST.val("SFMUL"), "ident",     ST.val("STARITH"),  None,  arith.mulexpr),
    Stamp(ST.val("SFMUL"), "num",       ST.val("STARITH"),  None,  arith.mulexpr),

    Stamp(ST.val("STARITH"), "/",       ST.val("SFDIV"),    None,  arith.arithop),
    Stamp(ST.val("SFDIV"), "ident",     ST.val("STARITH"),  None,  arith.divexpr),
    Stamp(ST.val("SFDIV"), "num",       ST.val("STARITH"),  None,  arith.divexpr),

    Stamp(ST.val("STARITH"), "+",       ST.val("SFADD"),    None,  arith.arithop),
    Stamp(ST.val("SFADD"),   "ident",   ST.val("STARITH"),  None,  arith.addexpr),
    Stamp(ST.val("SFADD"),   "num",     ST.val("STARITH"),  None,  arith.addexpr),

    Stamp(ST.val("STARITH"), "-",       ST.val("SFSUB"),     None, arith.arithop),
    Stamp(ST.val("SFSUB"), "ident",     ST.val("STARITH"),   None, arith.subexpr),
    Stamp(ST.val("SFSUB"), "num",       ST.val("STARITH"),   None, arith.subexpr),

    Stamp(ST.val("STARITH"), "<<",      ST.val("SFSHIFT"),  None,  arith.arithop),
    Stamp(ST.val("SFSHIFT"), "ident",   ST.val("STARITH"),  None,  arith.expr),
    Stamp(ST.val("SFSHIFT"), "num",     ST.val("STARITH"),  None,  arith.expr),

    Stamp(ST.val("STARITH"),  ">>",     ST.val("SFRSHIFT"), None,  arith.arithop),
    Stamp(ST.val("SFRSHIFT"), "ident",  ST.val("STARITH"),  None,  arith.expr),
    Stamp(ST.val("SFRSHIFT"), "num",    ST.val("STARITH"),  None,  arith.expr),

    #Stamp(ST.val("STARITH"), ";",       ST.val("STPOP"),    None,  arith.arith_stop),
    #Stamp(ST.val("STARITH"), "nl",      ST.val("STPOP"),    None,  arith.arith_stop),
    )

Ddecl = (
    # Declarations
    Stamp(STBASE,  "decl",   ST.val("DECL2"),   None,   decl.start),
    Stamp(STBASE,  "arr",    ST.val("DECL2"),   None,   decl.start),
    Stamp(STBASE,  "float",  ST.val("DECL2"),   None,   decl.start),
    Stamp(STBASE,  "dbl",    ST.val("DECL2"),   None,   decl.start),
    Stamp(STBASE,  "dbl2",   ST.val("DECL2"),   None,   decl.start),

    Stamp(ST.val("DECL2"), ":",         ST.val("DECL3"),    None,       decl.col),
    Stamp(ST.val("DECL3"), "ident",     ST.val("STARITH"),  None,       decl.ident),
    Stamp(ST.val("STARITH"), ",",       ST.val("DECL3"),    None,       decl.comma),
    Stamp(ST.val("STARITH"), ";",       ST.val("STPOP"),    decl.down,  decl.ident),
    Stamp(ST.val("STARITH"), "nl",      ST.val("STPOP"),    decl.down,  decl.ident),

    #Stamp(ST.val("DECL2"), ";",         ST.val("STPOP"),    decl.down,  decl.stop),
    #Stamp(ST.val("DECL2"), "nl",        ST.val("STPOP"),    None,       decl.stop),
    )

stamps =  (  \

    #Stamp(ST.val("STATEINI"), "num",    ST.val("STARITH"),  None,  arith.arithstart),
    Stamp(ST.val("STATEINI"), "ident",  ST.val("STARITH"),  None,  arith.arithstart),

    # include sub systems
    *Ddecl,
    *Darith,
    *Dfcall,
    *Dfuncx,
    *Drassn,

    # This will ignore comments
    Stamp(ST.val("STATEANY"), "comm2",   ST.val("STIGN"),   None,  func_comment),
    Stamp(ST.val("STATEANY"), "comm2d",  ST.val("STIGN"),   None,  func_dcomment), # //
    Stamp(ST.val("STATEANY"), "comm3",   ST.val("STIGN"),   None,  func_comment),  # /* */
    Stamp(ST.val("STATEANY"), "comm3d",  ST.val("STIGN"),   None,  func_dcomment2),
    Stamp(ST.val("STATEANY"), "comm4",   ST.val("STIGN"),   None,  func_comment),  # ##
    Stamp(ST.val("STATEANY"), "comm4d",  ST.val("STIGN"),   None,  func_dcomment3),

    # This will ignore white spaces
    Stamp(ST.val("STATEANY"), "tab",     ST.val("STIGN"),   None,  func_tab),
    Stamp(ST.val("STATEANY"), "sp",      ST.val("STIGN"),   None,  func_space),
    Stamp(ST.val("STATEANY"), "nl",      ST.val("STIGN"),   None,  func_nl),
    )

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
