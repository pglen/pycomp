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

# There are the entries to be matched agains the parse array.
#       (parse items,flags) ...                              function
#       --------------------------                           ----------

stamps =  (
    ( (("(",N),("sp",M),  ("num",A),    ("sp",M),  (")",M)), func_paren),
    ( (("num",N),  ("sp",M),  ("*",N),  ("sp",M),  ("num",N)), func_mul),
    ( (("num",N),  ("sp",P|M),("+",N),  ("sp",P|M),("num",N)), func_add),
    #( (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("num",N)), func_dummy),
    #( (("ident",N),("=",N),  ("strx",N)), func_dummy),
    #( (("ident",N),("sp",P|M),("=",N),  ("sp",P|M),("strx",N)), func_str),
  )

# EOF
