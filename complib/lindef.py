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

    def __init__(self, state, token, nstate, call, group = None, flags = None):
        self.state  = state
        self.token  = token
        self.nstate = nstate
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
ST = xenum("STATEANY", "STATEINI", "STATEBACK", "STATEBACK2", "STATEIGN", "STATEFUNC",
                "SFUNCARG", "SFUNCBODY")

# These are the entries to be matched agains the parse array.
#    state       item        new_state   function   group
#    -----       ---------   ----------  --------   -----

stamps =  (  \
        Stamp(ST.val("STATEINI"), "func",    ST.val("STATEFUNC"),   func_func),
        Stamp(ST.val("STATEFUNC"), "(",      ST.val("SFUNCARG"),    func_dummy),
        Stamp(ST.val("SFUNCARG"), ")",       ST.val("STATEBACK"),   func_dummy),
        Stamp(ST.val("STATEFUNC"), "{",      ST.val("SFUNCBODY"),   func_dummy),
        Stamp(ST.val("SFUNCBODY"), "}",      ST.val("STATEBACK2"),  func_dummy),

        # This will ignore commants
        Stamp(ST.val("STATEANY"), "comm2",   ST.val("STATEIGN"),    func_comment),
        Stamp(ST.val("STATEANY"), "comm3",   ST.val("STATEIGN"),    func_comment),
        Stamp(ST.val("STATEANY"), "comm2d",  ST.val("STATEIGN"),    func_dcomment),
        Stamp(ST.val("STATEANY"), "comm3d",  ST.val("STATEIGN"),    func_dcomment),

        # This will ignore white spaces
        Stamp(ST.val("STATEANY"), "sp",      ST.val("STATEIGN"),    func_dummy),
        Stamp(ST.val("STATEANY"), "nl",      ST.val("STATEIGN"),    func_dummy),
  )

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
