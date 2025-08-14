#!/usr/bin/env python

''' Definitions for the linear parser '''

try:
    from complib.utils import *
    from complib.linfunc  import *
except:
    #print(__file__, ":import local")
    from linfunc  import *
    from utils import *

N   =   0     # _No_ flag
P   =   1     # Op_P_ional
M   =   2     # _M_ultiple
A   =   4     # _A_ccumulate

def defpvg(xpvg):
    global pvg
    pvg = xpvg
    #print("got pvg", pvg)

SP = ("sp", M)

lut = Lut()
# The short version of add / lookup, returning the num only
def pl(strx):
    aa = lut.lookup(strx)
    return aa[0]

# Short hand for some items
SPC =  ("sp",M)

# Short hand for major items
BRACEX  = ("{",M), SPC, ("num",A), ("sp",M), ("}",N)
PARENX  = ("(",N), SPC, ("num",A), ("sp",M), (")",N)

# Short hand for language components
FUNCD   = ("func",N), ("sp",M), ("ident",N), ("sp",M), *PARENX, ("sp",M), *BRACEX, ("sp",M)
MULX    = ("num",N), ("sp",M), ("*",N), ("sp",M), ("num",N)
ADDX    = ("num",N), ("sp",P|M), ("+",N), ("sp",P|M), ("num",N)

STATE0   = pl("state_0")
STATEANY = pl("state_any")

# These are the entries to be matched agains the parse array.
#    state      (items,flags)       new_state       function
#    -----      ----------------    ---------       ----------
stamps =  (
    (STATE0,    FUNCD,              STATEANY,      func_func),
    (STATE0,    BRACEX,             STATEANY,      func_brace),
    (STATE0,    PARENX,             STATEANY,      func_paren),
    (STATE0,    MULX,               STATEANY,      func_mul),
    (STATE0,    ADDX,               STATEANY,      func_add),

    #(SL.INI.value,  (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("num",N)), func_dummy),
    #(SL.INI.value,  (("ident",N),("=",N),  ("strx",N)), func_dummy),
    #(SL.INI.value,  (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("strx",N)), func_str),
  )

pvar(stamps)

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #pl("aaaaa") ;    pl("bbbbbb") ;  pl("cvvvvv");
    #pl("dcccccc") ;  pl("eeeeeee")
    #print(lut.dump(), end = " ")

# EOF
