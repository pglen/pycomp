#!/usr/bin/env python

''' Definitions for the linear parser '''

from complib.utils import *

from complib.linfunc  import *

N   =   0     # _No_ flag
P   =   1     # Op_P_ional
M   =   2     # _M_ultiple
A   =   4     # _A_ccumulate

def defpvg(xpvg):
    global pvg
    pvg = xpvg

SP = ("sp", M)

from enum import Enum

class SL(Enum):
    INI = 0; FUNC=2; ARGS=2; DECL=3

class CO(Enum):
    INI = 0; FUNC=2; ARGS=2; DECL=3

class Stmp():

    ''' Our parser stamp '''
    def __init__(self):
        self.state = SL.INI
        self.scan = ()
        self.callf = None

    def call(self):
        ret = None
        if self.callf:
             ret = self.callf()
        return ret

# Short hand for major items

BRACEX  = ("{",M), ("sp",M), ("num",A), ("sp",M), ("}",N)
PARENX  = ("(",N), ("sp",M), ("num",A), ("sp",M), (")",N)

# Short hand for language components

FUNCD   = ("func",N), ("sp",M), *PARENX, ("sp",M), *BRACEX, ("sp",M)
MULX     = ("num",N),  ("sp",M),  ("*",N),  ("sp",M),  ("num",N)
ADDX     = ("num",N),  ("sp",P|M),("+",N),  ("sp",P|M),("num",N)

# There are the entries to be matched agains the parse array.
#    state      (parse items,flags) ...         function
#    -----      --------------------            ----------

stamps =  (
    (SL.INI.value,  FUNCD,  func_func),
    (SL.INI.value,  PARENX, func_paren),
    (SL.INI.value,  MULX,    func_mul),
    (SL.INI.value,  ADDX,    func_add),

    #(SL.INI.value,  (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("num",N)), func_dummy),
    #(SL.INI.value,  (("ident",N),("=",N),  ("strx",N)), func_dummy),
    #(SL.INI.value,  (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("strx",N)), func_str),
  )

#print(stamps)

# EOF
