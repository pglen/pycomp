#!/usr/bin/env python

''' Definitions for the linear parser '''

from complib.utils import *
from complib.linfunc  import *
import complib.lexdef  as lexdef

def defpvg(xpvg):
    global pvg
    pvg = xpvg
    #print("got pvg", pvg)

lut = Lut()
# The short version of add / lookup, returning the num only
def pl(strx):
    aa = lut.lookup(strx)
    return aa[0]

(GROUPANY,) = range(1)
(STATEANY, STATEINI, SFUNC, SFUNCARG) = range(4)

# These flags determine the handling of a token. The ptional
# is meant to be skipped if not present, the multiple is meant
# to eat up more than one occurances.

N   =   0     # _No flag
P   =   1     # O_P ional
M   =   2     # _Multiple
A   =   4     # _Accumulate

class Stamp:

    def __init__(self, state, token, nstate, call, group = None, flags = None):
        self.state  = state
        self.tokem  = token
        self.nstate = nstate
        self.call   = call
        self.group  = group
        self.flags  = flags

    def dump(self):
        strx  =  str.self.state
        strx +=  str.self.token
        strx +=  str.self.nstate

        return strx

# These are the entries to be matched agains the parse array.
#    state       item        new_state   function   group
#    -----       ---------   ----------  --------   -----

stamps =  (  \
        Stamp(STATEINI, "func",   SFUNC,  func_func),
  )

pvar(stamps)

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #pl("aaaaa") ;    pl("bbbbbb") ;  pl("cvvvvv");
    #pl("dcccccc") ;  pl("eeeeeee")
    #print(lut.dump(), end = " ")

# EOF
