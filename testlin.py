#!/usr/bin/env python

''' Definitions for the linear parser '''

#!/usr/bin/env python

''' Definitions for the linear parser '''

from complib.utils  import *
from complib.ptree import *

import complib.stack as stack
import complib.lexdef  as lexdef
import complib.lindef as lindef

from complib.linfunc import *

for cnt, aa in enumerate(lindef.stamps):
    #print("stamp:", aa.dump())
    if aa.state == lindef.ST.val("STATEANY"):
        continue
    for cnt2, aa2 in enumerate(lindef.stamps):
        if aa == aa2:
            continue
        if aa.state == aa2.nstate :
            for cnt3, aa3 in enumerate(lindef.stamps):
                if aa3 == aa2:
                    continue
                if aa3.state == aa2.state :
                    print("stamp:", aa2.dump(), "to stamp2:", aa3.dump())
# EOF
