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

GR = xenum("GROUPANY")
ST = xenum("STATEANY", "STATEINI", "SFUNC", "SFUNCARG")

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

# These are the entries to be matched agains the parse array.
#    state       item        new_state   function   group
#    -----       ---------   ----------  --------   -----

stamps =  (  \
        Stamp(ST.val("STATEINI"), "func",   ST.val("SFUNC"),        func_func),
        Stamp(ST.val("STATEINI"), "(",      ST.val("STATEANY"),     func_dummy),
        Stamp(ST.val("STATEINI"), ")",      ST.val("STATEANY"),     func_dummy),
        Stamp(ST.val("STATEINI"), "{",      ST.val("STATEANY"),     func_dummy),
        Stamp(ST.val("STATEINI"), "}",      ST.val("STATEANY"),     func_dummy),

        # This will ignore white spaces
        Stamp(ST.val("STATEINI"), "sp",      ST.val("STATEANY"),    func_dummy),
        Stamp(ST.val("STATEINI"), "nl",      ST.val("STATEANY"),    func_dummy),
  )

pvar(stamps)

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #pl("aaaaa") ;    pl("bbbbbb") ;  pl("cvvvvv");
    #pl("dcccccc") ;  pl("eeeeeee")
    #print(lut.dump(), end = " ")

# EOF
