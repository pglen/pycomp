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
        strx  =  str.self.state
        strx +=  str.self.token
        strx +=  str.self.nstate
        return strx

    def __str__(self):
        strx = "State: " + str(ST.get(self.state)) + " " + \
            str(self.token) + " nState: " + str(ST.get(self.nstate)) + \
                " " + str(self.call.__name__)
        return strx

GR = xenum("GROUPANY")

# Changed to auto add new state
ST = xenum("STATEANY", "STATEINI", "STPOP", "STPOP2",
                "STATEIGN", "STATEFUNC", "SFUNARG", "SFUNARG2", "SFUNARG3",
                    "SFUNARG4", "SFUNBODY", "SFASSN", "SFASSN2", "SFADD2")

# These are the entries to be matched agains the parse array.
#    state       item        new_state   function   group
#    -----       ---------   ----------  --------   -----

stamps =  (  \
    Stamp(ST.val("STATEINI"), "func",   ST.val("STATEFUNC"), False,  func_func),
    Stamp(ST.val("STATEFUNC"), "(",     ST.val("SFUNARG"),   False, func_dummy),
    Stamp(ST.val("SFUNARG"), "decl",    ST.val("SFUNARG2"), True,  func_dummy),

    # Declarations
    Stamp(ST.val("STATEINI"), "decl",   ST.val("SFUNARG2"), True,   None),
    Stamp(ST.val("STATEINI"), "float",  ST.val("SFUNARG2"), True,   func_dummy),
    Stamp(ST.val("STATEINI"), "dbl",    ST.val("SFUNARG2"), True,   func_dummy),

    Stamp(ST.val("SFUNARG2"), ":",      ST.val("SFUNARG3"), False,  func_dummy),
    Stamp(ST.val("SFUNARG3"), "ident",  ST.val("SFUNARG3"), False,  func_dummy),
    Stamp(ST.val("SFUNARG3"), "=",      ST.val("SFUNARG4"), False,  func_dummy),
    Stamp(ST.val("SFUNARG4"), "ident",  ST.val("SFUNARG3"), False,  func_dummy),
    Stamp(ST.val("SFUNARG4"), "num",    ST.val("SFUNARG3"), False,  func_dummy),
    Stamp(ST.val("SFUNARG3"), ";",      ST.val("STPOP"),    False,  func_dummy),
    Stamp(ST.val("SFUNARG3"), "nl",     ST.val("STPOP"),    False,  func_dummy),
    Stamp(ST.val("SFUNARG3"), "comm2",  ST.val("STPOP"),    False,  func_dummy),

    Stamp(ST.val("SFUNARG"), ")",       ST.val("STATEIGN"), False,  func_dummy),
    Stamp(ST.val("STATEFUNC"), "{",     ST.val("SFUNBODY"), False,  func_dummy),
    Stamp(ST.val("SFUNBODY"), "}",      ST.val("STATEIGN"), False,  func_dummy),

    # Assignments / Start of arithmetic
    Stamp(ST.val("STATEINI"), "num",    ST.val("SFARITH"),  True,   func_arithstart),
    Stamp(ST.val("STATEINI"), "ident",  ST.val("SFARITH"),  True,   func_arithstart),

    Stamp(ST.val("SFARITH"),  "=",      ST.val("SFASSN"),   False,   func_arithop),
    Stamp(ST.val("SFASSN"),   "ident",  ST.val("STPOP"),    False,   None),
    Stamp(ST.val("SFASSN"),   "num",    ST.val("STPOP"),    False,   None),

    # Arithmetics (+ - * / sqr)
    Stamp(ST.val("SFARITH"), "sqr",     ST.val("SFSQR"),    False,  func_arithop),
    Stamp(ST.val("SFSQR"),   "ident",   ST.val("SFARITH"),  False,  None),
    Stamp(ST.val("SFSQR"),   "num",     ST.val("SFARITH"),  False,  None),

    Stamp(ST.val("SFARITH"), "+",       ST.val("SFADD"),    False,  func_arithop),
    Stamp(ST.val("SFADD"),   "ident",   ST.val("SFARITH"),  False,   func_addexpr),
    Stamp(ST.val("SFADD"),   "num",     ST.val("SFARITH"),  False,   func_addexpr),

    Stamp(ST.val("SFARITH"), "-",       ST.val("SFSUB"),    False,   func_arithop),
    Stamp(ST.val("SFSUB"), "ident",     ST.val("STPOP"),    False,   None),
    Stamp(ST.val("SFSUB"), "num",       ST.val("STPOP"),    False,   None),

    Stamp(ST.val("SFARITH"), "*",       ST.val("SFMUL"),    False,   func_arithop),
    Stamp(ST.val("SFMUL"), "ident",     ST.val("SFARITH"), False,   func_mulexpr),
    Stamp(ST.val("SFMUL"), "num",       ST.val("SFARITH"), False,   func_mulexpr),

    Stamp(ST.val("SFARITH"), "/",       ST.val("SFDIV"),    False,   func_arithop),
    Stamp(ST.val("SFDIV"), "ident",     ST.val("SFARITH"), False,   None),
    Stamp(ST.val("SFDIV"), "num",       ST.val("SFARITH"), False,   None),

    Stamp(ST.val("SFARITH"), ";",       ST.val("STPOP"),    False,   func_endarith),
    Stamp(ST.val("SFARITH"), "nl",      ST.val("STPOP"),    False,   func_endarith),

    # This will ignore commants
    Stamp(ST.val("STATEANY"), "comm2",   ST.val("STATEIGN"), False,   func_comment),
    Stamp(ST.val("STATEANY"), "comm3",   ST.val("STATEIGN"), False,   func_comment),
    Stamp(ST.val("STATEANY"), "comm2d",  ST.val("STATEIGN"), False,   func_dcomment),
    Stamp(ST.val("STATEANY"), "comm3d",  ST.val("STATEIGN"), False,   func_dcomment),

    # This will ignore white spaces
    Stamp(ST.val("STATEANY"), "sp",      ST.val("STATEIGN"), False,   func_dummy),
    Stamp(ST.val("STATEANY"), "nl",      ST.val("STATEIGN"), False,   func_dummy),
    )

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
