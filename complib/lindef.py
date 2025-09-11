#!/usr/bin/env python

''' Definitions for the linear parser

# We initialize parser variables in the context of the parser module.
#
# Parse table consists of:
#       a.) Parser states
#       b.) Token definition
#       c.) New parser state
#       d.) Parser function
#
# To create a custom parser, just add new tokens / states here
#
# The parser will look up if current state is in the list of parser states.
# If there is a match, the token is compared. If there is a match, the new
# parser state is set, and the specified parser function is executed.
#
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

    def __init__(self, state, token, nstate, pushx, call, group = None, flags = None):

        # Extend to array if a number passed
        if type(state) == type(0):
            self.state = (state,)
            #print("type cast", self.state)
        else:
            self.state  = state

        self.token  = token

        self.nstate = nstate
        self.push   = pushx
        self.call   = call
        self.group  = group
        self.flags  = flags

    def dump(self):

        states =  ""
        for aa in self.state:
            states += ST.get(aa) + " "
        strx  =  "[ " + states + " "
        strx +=  pp(str(self.token)) + " "
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

funcx = ( \
    # Function Declaration
    Stamp(ST.val("STATEANY"),  "func",   ST.val("STFUNC"),    False,  None),
    Stamp(ST.val("STFUNC"),    "ident",  ST.val("STFUNC2"),   False,  func_func_start),
    Stamp(ST.val("STFUNC2"),   "(",      ST.val("SFUNARG"),   False,  None),
    Stamp(ST.val("SFUNARG"),   "decl",   ST.val("SFUNARG2"),  True,   func_func_arg_start),
    Stamp(ST.val("SFUNARG2"),  ":",      ST.val("SFUNARG3"),  False,  None),
    Stamp(ST.val("SFUNARG3"),  "ident",  ST.val("SFUNARG4"),  False,  None),
    Stamp(ST.val("SFUNARG4"),  ",",      ST.val("SFUNARG3"),   False,  None),
    Stamp(ST.val("SFUNARG4"),  "=",      ST.val("SFUNARG4"),  False,  None),
    Stamp(ST.val("SFUNARG4"),  "ident",  ST.val("SFUNARG3"),  False,  None),
    Stamp(ST.val("SFUNARG4"),  "num",    ST.val("SFUNARG3"),  False,  None),
    Stamp(ST.val("SFUNARG3"),  "nl",     ST.val("STPOP"),     False,  None),
    Stamp(ST.val("SFUNARG3"),  "comm2",  ST.val("STPOP"),     False,  None),

    Stamp(ST.val("SFUNARG"),  ")",      ST.val("STFUNC3"),    False,  func_func_args),
    Stamp(ST.val("SFUNARG3"), ")",      ST.val("STFUNC3"),    False,  func_func_args),
    Stamp(ST.val("STFUNC3"),  "{",      ST.val("SFUNBODY"),   False,  None),
    Stamp(ST.val("SFUNBODY"), "return", ST.val("SFUNCRET"),   False,  None),
    Stamp(ST.val("SFUNCRET"), "ident",  ST.val("SFUNBODY"),   False,  None),
    Stamp(ST.val("SFUNBODY"), "}",      ST.val("STATEINI"),   False,  func_func_end),
    )

rassn  = (
    # Right side assignment
    Stamp(ST.val("STARITH"),  "=>",     ST.val("STRASSN3"),  False,  None),
    Stamp(ST.val("STRASSN3"), "num",    ST.val("STRASSN4"),  False,  func_rassn),
    Stamp(ST.val("STRASSN3"), "num2",   ST.val("STRASSN4"),  False,  func_rassn),
    Stamp(ST.val("STRASSN3"), "ident",  ST.val("STRASSN4"),  False,  func_rassn),
    Stamp(ST.val("STRASSN4"),  ";",     ST.val("STPOP"),     False,  func_rassn_stop),
    Stamp(ST.val("STRASSN4"),  "nl",    ST.val("STPOP"),     False,  func_rassn_stop),
    )

fcall  = (
    # Function call
    Stamp(ST.val("STATEINI"),  "ident",  ST.val("CFUNC2"),  True,  None),
    Stamp(ST.val("SFUNARG"),   "ident",  ST.val("CFUNC2"),  True,  None),
    Stamp(ST.val("SFUNBODY"),  "ident",  ST.val("CFUNC2"),  True,  None),
    Stamp(ST.val("STARITH"),   "(",      ST.val("CFUNC3"),  False, func_func_call),
    Stamp(ST.val("CFUNC2"),    "(",      ST.val("CFUNC3"),  False, func_func_call),
    Stamp(ST.val("CFUNC3"),    "num",    ST.val("CFUNC4"),  False, func_func_decl_val),
    Stamp(ST.val("CFUNC3"),    "ident",  ST.val("CFUNC4"),  False, func_func_decl_val),
    Stamp(ST.val("CFUNC3"),    "str",    ST.val("CFUNC4"),  False, func_func_decl_val),
    Stamp(ST.val("CFUNC3"),    ")",      ST.val("STPOP"),   False, func_func_end),
    Stamp(ST.val("CFUNC4"),    ",",      ST.val("CFUNC3"),  False, None),
    Stamp(ST.val("CFUNC4"),    ")",      ST.val("STPOP"),   False,  func_func_end),
    )

    #Stamp(ST.val("DECL4"), "=",         ST.val("STARITH"),  False,  None),
    #Stamp(ST.val("DECL5"), "ident",     ST.val("DECL6"),    False,  func_decl_val),
    #Stamp(ST.val("DECL5"), "num",       ST.val("DECL6"),    False,  func_decl_val),
    #Stamp(ST.val("DECL5"), "num2",      ST.val("DECL6"),    False,  func_decl_val),
    #Stamp(ST.val("DECL5"), "str",       ST.val("DECL6"),    False,  func_decl_val),

    #Stamp(ST.val("DECL6"), ",",         ST.val("DECL3"),    False,  func_decl_comma),
    #Stamp(ST.val("DECL6"), ";",         ST.val("STPOP"),    False,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "nl",        ST.val("STPOP"),    False,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm2",     ST.val("STPOP"),    False,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm4",     ST.val("STPOP"),    False,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm2d",    ST.val("STPOP"),    False,  func_decl_stop),
    #Stamp(ST.val("DECL6"), "comm4d",    ST.val("STPOP"),    False,  func_decl_stop),

    #Stamp(ST.val("STARITH"),  "=",      ST.val("STASSN"),   False,  func_assn_start),
    #Stamp(ST.val("STASSN"),   "ident",  ST.val("STARITH"),  False,  func_assn),
    #Stamp(ST.val("STASSN"),   "num",    ST.val("STARITH"),  False,  func_assn),
    #Stamp(ST.val("STASSN"),   "str",    ST.val("STARITH"),  False,  func_assn),
    #Stamp(ST.val("STARITH"),  ";",      ST.val("STPOP"),   False,   func_assn_stop),
    #Stamp(ST.val("STARITH"),  "nl",     ST.val("STPOP"),   False,   func_assn_stop),

arith = (
    # Arithmetics (+ - * / sqr assn)
    Stamp(ST.val("STARITH"), "=",       ST.val("SFASSN"),   False,  func_arithop),
    Stamp(ST.val("SFASSN"), "ident",    ST.val("STARITH"),  False,  func_assnexpr),
    Stamp(ST.val("SFASSN"), "num",      ST.val("STARITH"),  False,  func_assnexpr),

    Stamp(ST.val("STARITH"), "=>",      ST.val("SFPUT"),    False,  func_arithop),
    Stamp(ST.val("SFPUT"), "ident",     ST.val("STARITH"),  False,  func_mulexpr),
    Stamp(ST.val("SFPUT"), "num",       ST.val("STARITH"),  False,  func_mulexpr),

    Stamp(ST.val("STARITH"), "expo",    ST.val("SFSQR"),    False,  func_arithop),
    Stamp(ST.val("SFSQR"),   "ident",   ST.val("STARITH"),  False,  func_expexpr),
    Stamp(ST.val("SFSQR"),   "num",     ST.val("STARITH"),  False,  func_expexpr),

    Stamp(ST.val("STARITH"), "*",       ST.val("SFMUL"),    False,  func_arithop),
    Stamp(ST.val("SFMUL"), "ident",     ST.val("STARITH"),  False,  func_mulexpr),
    Stamp(ST.val("SFMUL"), "num",       ST.val("STARITH"),  False,  func_mulexpr),

    Stamp(ST.val("STARITH"), "/",       ST.val("SFDIV"),    False,  func_arithop),
    Stamp(ST.val("SFDIV"), "ident",     ST.val("STARITH"),  False,  func_divexpr),
    Stamp(ST.val("SFDIV"), "num",       ST.val("STARITH"),  False,  func_divexpr),

    Stamp(ST.val("STARITH"), "+",       ST.val("SFADD"),    False,  func_arithop),
    Stamp(ST.val("SFADD"),   "ident",   ST.val("STARITH"),  False,  func_addexpr),
    Stamp(ST.val("SFADD"),   "num",     ST.val("STARITH"),  False,  func_addexpr),

    Stamp(ST.val("STARITH"), "-",       ST.val("SFSUB"),     False,  func_arithop),
    Stamp(ST.val("SFSUB"), "ident",     ST.val("STARITH"),   False,  func_subexpr),
    Stamp(ST.val("SFSUB"), "num",       ST.val("STARITH"),   False,  func_subexpr),

    Stamp(ST.val("STARITH"), "<<",      ST.val("SFSHIFT"),  False,    func_arithop),
    Stamp(ST.val("SFSHIFT"), "ident",   ST.val("STARITH"),  False,    func_expr),
    Stamp(ST.val("SFSHIFT"), "num",     ST.val("STARITH"),  False,    func_expr),

    Stamp(ST.val("STARITH"),  ">>",     ST.val("SFRSHIFT"), False,    func_arithop),
    Stamp(ST.val("SFRSHIFT"), "ident",  ST.val("STARITH"),  False,    func_expr),
    Stamp(ST.val("SFRSHIFT"), "num",    ST.val("STARITH"),  False,    func_expr),

    Stamp(ST.val("STARITH"), ";",       ST.val("STPOP"),    False,  func_arith_stop),
    Stamp(ST.val("STARITH"), "nl",      ST.val("STPOP"),    False,  func_arith_stop),
    )

decl = (
    # Declarations
    Stamp(STBASE,  "decl",   ST.val("DECL2"),   True,   func_decl_start),
    Stamp(STBASE,  "arr",    ST.val("DECL2"),   True,   func_decl_start),
    Stamp(STBASE,  "float",  ST.val("DECL2"),   True,   func_decl_start),
    Stamp(STBASE,  "dbl",    ST.val("DECL2"),   True,   func_decl_start),
    Stamp(STBASE,  "dbl2",   ST.val("DECL2"),   True,   func_decl_start),

    Stamp(ST.val("DECL2"), ":",         ST.val("DECL3"),      False,  None),
    Stamp(ST.val("DECL3"), "ident",     ST.val("STARITH"),    False,  func_decl_ident),

    #Stamp(ST.val("STARITH"), ",",       ST.val("STPOP"),     False,  func_decl_comma),
    #Stamp(ST.val("DECL4"), ";",         ST.val("STPOP2"),    False,  func_decl_stop),
    #Stamp(ST.val("DECL4"), "nl",        ST.val("STPOP2"),    False,  func_decl_stop),
    )

# These are the entries to be matched agains the parse array.
#    states     token       new_state       push_marker     function
#    ------     -----       ----------      -----------     --------

stamps =  (  \

    # Assignments / Start of arithmetic
    #Stamp(ST.val("STATEINI"), "num",    ST.val("STARITH"),  True,  func_arithstart),
    Stamp(ST.val("STATEINI"), "ident",  ST.val("STARITH"),  True,  func_arithstart),

    *decl,
    *arith,
    *funcx,
    *rassn,

    # This will ignore comments
    Stamp(ST.val("STATEANY"), "comm2",   ST.val("STIGN"),   False,  func_comment),
    Stamp(ST.val("STATEANY"), "comm2d",  ST.val("STIGN"),   False,  func_dcomment), # //
    Stamp(ST.val("STATEANY"), "comm3",   ST.val("STIGN"),   False,  func_comment),  # /* */
    Stamp(ST.val("STATEANY"), "comm3d",  ST.val("STIGN"),   False,  func_dcomment2),
    Stamp(ST.val("STATEANY"), "comm4",   ST.val("STIGN"),   False,  func_comment),  # ##
    Stamp(ST.val("STATEANY"), "comm4d",  ST.val("STIGN"),   False,  func_dcomment3),

    # This will ignore white spaces
    Stamp(ST.val("STATEANY"), "tab",     ST.val("STIGN"),   False,  func_tab),
    Stamp(ST.val("STATEANY"), "sp",      ST.val("STIGN"),   False,  func_space),
    Stamp(ST.val("STATEANY"), "nl",      ST.val("STIGN"),   False,  func_nl),
    )

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
