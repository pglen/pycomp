#!/usr/bin/env python

''' Definitions for the linear parser '''

from complib.utils import *
from complib.linfunc  import *
import complib.lexdef  as lexdef

def defpvg(xpvg):
    global pvg
    pvg = xpvg
    #print("got pvg", pvg)

# These flags determine the handling of a token. The ptional
# is meant to be skipped if not present, the multiple is meant
# to eat up more than one occurances. (obsolete)
# N  =_No flag  O = O_P ional  M  = _Multiple A = _Accumulate

FL = xenum("N", "P", "M", "A")

class Stamp:

    def __init__(self, state, token, nstate, pushx, call, group = None, flags = None):
        self.state  = state
        self.token  = token
        self.nstate = nstate
        self.push   = pushx
        self.call   = call
        self.group  = group
        self.flags  = flags

    def dump(self):
        strx  =  "[ " + ST.get(self.state) + " "
        strx +=  pp(str(self.token)) + " "
        strx +=  ST.get(self.nstate) + " ]"
        return strx

    def __str__(self):
        strx = "State: " + ST.get(self.state) + " " + \
            str(self.token) + " nState: " + ST.get(self.nstate) + \
                " " + str(self.call.__name__)
        return strx

GR = xenum("GROUPANY")

# Changed to auto add new state (note: no dup checking)
ST = xenum()
#"STATEANY", "STATEINI", "STPOP", "STPOP2",
#                "STIGN", "STATEFUNC", "SFUNARG", "SFUNARG2", "SFUNARG3",
#                    "SFUNARG4", "SFUNBODY", "SFASSN", "SFASSN2", "SFADD2")

# These are the entries to be matched agains the parse array.
#    state       item        new_state   function   group
#    -----       ---------   ----------  --------   -----

stamps =  (  \
    #Stamp(ST.val("STATEINI"), "func",   ST.val("STATEFUNC"), False, func_func),
    #Stamp(ST.val("STATEFUNC"), "(",     ST.val("SFUNARG"),   False, None),
    #Stamp(ST.val("SFUNARG"), "decl",    ST.val("SFUNARG2"),  True,  None),
    #
    #Stamp(ST.val("SFUNARG2"), ":",      ST.val("SFUNARG3"), False,  None),
    #Stamp(ST.val("SFUNARG3"), "ident",  ST.val("SFUNARG3"), False,  None),
    #Stamp(ST.val("SFUNARG3"), "=",      ST.val("SFUNARG4"), False,  None),
    #Stamp(ST.val("SFUNARG4"), "ident",  ST.val("SFUNARG3"), False,  None),
    #Stamp(ST.val("SFUNARG4"), "num",    ST.val("SFUNARG3"), False,  None),
    #Stamp(ST.val("SFUNARG3"), ";",      ST.val("STPOP"),    False,  None),
    #Stamp(ST.val("SFUNARG3"), "nl",     ST.val("STPOP"),    False,  None),
    #Stamp(ST.val("SFUNARG3"), "comm2",  ST.val("STPOP"),    False,  None),
    #Stamp(ST.val("SFUNARG"), ")",       ST.val("STIGN"),    False,  func_dummy),
    #Stamp(ST.val("STATEFUNC"), "{",     ST.val("SFUNBODY"), False,  func_dummy),
    #Stamp(ST.val("SFUNBODY"), "}",      ST.val("STIGN"),    False,  func_dummy),

    # Assignments / Start of arithmetic
    Stamp(ST.val("STATEINI"), "num",    ST.val("SFARITH"),   True,  func_arithstart),
    Stamp(ST.val("STATEINI"), "ident",  ST.val("SFARITH"),   True,  func_arithstart),

    # Declarations
    Stamp(ST.val("STATEINI"), "decl",   ST.val("DECL2"),    True,   func_decl_start),
    Stamp(ST.val("STATEINI"), "arr",    ST.val("DECL2"),    True,   func_decl_start),
    Stamp(ST.val("STATEINI"), "float",  ST.val("DECL2"),    True,   func_decl_start),
    Stamp(ST.val("STATEINI"), "dbl",    ST.val("DECL2"),    True,   func_decl_start),
    Stamp(ST.val("STATEINI"), "exten",  ST.val("DECL2"),    True,   func_decl_start),

    # Functions
    Stamp(ST.val("SFARITH"),  "(",      ST.val("FUNC3"),    False,  func_func_start),
    Stamp(ST.val("FUNC3"),    "num",    ST.val("FUNC4"),    False,  func_func_decl_val),
    Stamp(ST.val("FUNC3"),    "ident",  ST.val("FUNC4"),    False,  func_func_decl_val),
    Stamp(ST.val("FUNC3"),    "str",    ST.val("FUNC4"),    False,  func_func_decl_val),
    Stamp(ST.val("FUNC4"),    ",",      ST.val("FUNC3"),    False,  None),
    Stamp(ST.val("FUNC4"),    ")",      ST.val("STPOP"),    False,  func_func_end),

    Stamp(ST.val("DECL2"), ":",         ST.val("DECL3"),    False,  None),
    Stamp(ST.val("DECL3"), "ident",     ST.val("DECL4"),    False,  func_decl_ident),
    Stamp(ST.val("DECL4"), "=",         ST.val("DECL5"),    False,  None),
    Stamp(ST.val("DECL5"), "ident",     ST.val("DECL6"),    False,  func_decl_val),
    Stamp(ST.val("DECL5"), "num",       ST.val("DECL6"),    False,  func_decl_val),
    Stamp(ST.val("DECL5"), "num2",      ST.val("DECL6"),    False,  func_decl_val),
    Stamp(ST.val("DECL5"), "str",       ST.val("DECL6"),    False,  func_decl_val),
    Stamp(ST.val("DECL6"), ",",         ST.val("DECL3"),    False,  func_decl_comma),
    Stamp(ST.val("DECL6"), ";",         ST.val("STPOP"),    False,  func_decl_stop),
    Stamp(ST.val("DECL6"), "nl",        ST.val("STPOP"),    False,  func_decl_stop),
    Stamp(ST.val("DECL6"), "comm2",     ST.val("STPOP"),    False,  func_decl_stop),
    Stamp(ST.val("DECL6"), "comm4",     ST.val("STPOP"),    False,  func_decl_stop),
    Stamp(ST.val("DECL6"), "comm2d",    ST.val("STPOP"),    False,  func_decl_stop),
    Stamp(ST.val("DECL6"), "comm4d",    ST.val("STPOP"),    False,  func_decl_stop),

    #Stamp(ST.val("SFARITH"),  "=>",     ST.val("STRASSN3"),  False,  None),
    #Stamp(ST.val("STRASSN3"), "num",    ST.val("STRASSN4"),  False,  func_rassn),
    #Stamp(ST.val("STRASSN3"), "num2",   ST.val("STRASSN4"),  False,  func_rassn),
    #Stamp(ST.val("STRASSN3"), "ident",  ST.val("STRASSN4"),  False,  func_rassn),
    #Stamp(ST.val("STRASSN4"),  ";",     ST.val("STPOP"),     False,  func_rassn_stop),
    #Stamp(ST.val("STRASSN4"),  "nl",    ST.val("STPOP"),     False,  func_rassn_stop),

    Stamp(ST.val("SFARITH"),  "=",      ST.val("STASSN"),    False,  None),
    Stamp(ST.val("STASSN"),   "ident",  ST.val("SFARITH"),   False,  func_assn),
    Stamp(ST.val("STASSN"),   "num",    ST.val("SFARITH"),   False,  func_assn),
    Stamp(ST.val("STASSN"),   "num2",   ST.val("SFARITH"),   False,  func_assn),
    Stamp(ST.val("STASSN"),   "str",    ST.val("SFARITH"),    False,  func_assn),
    #Stamp(ST.val("STASSN2"),  ";",      ST.val("STPOP"),     False,  func_assn_stop),
    #Stamp(ST.val("STASSN2"),  "nl",     ST.val("STPOP"),     False,  func_assn_stop),

    # Arithmetics (+ - * / sqr assn)
    Stamp(ST.val("SFARITH"), "=>",      ST.val("SFPUT"),    False,  func_arithop),
    Stamp(ST.val("SFPUT"), "ident",     ST.val("SFARITH"), False,   func_mulexpr),
    Stamp(ST.val("SFPUT"), "num",       ST.val("SFARITH"), False,   func_mulexpr),

    Stamp(ST.val("SFARITH"), "expo",    ST.val("SFSQR"),    False, func_arithop),
    Stamp(ST.val("SFSQR"),   "ident",   ST.val("SFARITH"),  False, func_expexpr),
    Stamp(ST.val("SFSQR"),   "num",     ST.val("SFARITH"),  False, func_expexpr),

    Stamp(ST.val("SFARITH"), "*",       ST.val("SFMUL"),    False,  func_arithop),
    Stamp(ST.val("SFMUL"), "ident",     ST.val("SFARITH"), False,   func_mulexpr),
    Stamp(ST.val("SFMUL"), "num",       ST.val("SFARITH"), False,   func_mulexpr),

    Stamp(ST.val("SFARITH"), "/",       ST.val("SFDIV"),    False,  func_arithop),
    Stamp(ST.val("SFDIV"), "ident",     ST.val("SFARITH"), False,   None),
    Stamp(ST.val("SFDIV"), "num",       ST.val("SFARITH"), False,   None),

    Stamp(ST.val("SFARITH"), "+",       ST.val("SFADD"),    False,  func_arithop),
    Stamp(ST.val("SFADD"),   "ident",   ST.val("SFARITH"),  False,  func_addexpr),
    Stamp(ST.val("SFADD"),   "num",     ST.val("SFARITH"),  False,  func_addexpr),

    Stamp(ST.val("SFARITH"), "-",       ST.val("SFSUB"),    False,  func_arithop),
    Stamp(ST.val("SFSUB"), "ident",     ST.val("STPOP"),    False,  None),
    Stamp(ST.val("SFSUB"), "num",       ST.val("STPOP"),    False,  None),

    Stamp(ST.val("SFARITH"), ";",       ST.val("STPOP"),    False,  func_arit_stop),
    Stamp(ST.val("SFARITH"), "nl",      ST.val("STPOP"),    False,  func_arit_stop),

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
