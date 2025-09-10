#!/usr/bin/env python

''' Tool for the linear parser '''

from complib.utils  import *
from complib.ptree import *

import complib.stack as stack
import complib.lexdef  as lexdef
import complib.lindef as lindef

from complib.linfunc import *

for cnt, aa in enumerate(lindef.stamps):

    #print("stamp:", cnt, aa)
    if  lindef.ST.val("STATEANY") in aa.state:
        #print("stateany skip", aa)
        #continue
        pass
    for cnt2, aa2 in enumerate(lindef.stamps):
        if aa == aa2:
            #print("stateidentical skip", aa)
            continue
        if aa2.nstate in aa.state :
            for cnt3, aa3 in enumerate(lindef.stamps):
                if  aa2 == aa3:
                    #print("stateidentical2 skip", aa)
                    continue
                #print("aa2", aa2.state, "aa3", aa3.state)
                for bb in aa2.state:
                    if bb in aa3.state :
                        print("st:", cnt, aa2.dump(), "to st2:", cnt2, aa3.dump())
# EOF