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

# There are the entries to be matched agains the parse array.
#    state      (parse items,flags) ...    new_state     function
#    -----      --------------------       ---------     ----------

stamps =  (
    (0,  FUNCD,  func_func),
    (0,  BRACEX, func_brace),
    (0,  PARENX, func_paren),
    (0,  MULX,   func_mul),
    (0,  ADDX,   func_add),

    #(SL.INI.value,  (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("num",N)), func_dummy),
    #(SL.INI.value,  (("ident",N),("=",N),  ("strx",N)), func_dummy),
    #(SL.INI.value,  (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("strx",N)), func_str),
  )

#print(stamps)

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #pl("aaaaa") ;    pl("bbbbbb") ;  pl("cvvvvv");
    #pl("dcccccc") ;  pl("eeeeeee")
    #print(lut.dump(), end = " ")

# EOF
