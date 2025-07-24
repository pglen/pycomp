#!/usr/bin/env python

import re, sys

from complib.utils  import *

from complib.linfunc import *
from complib.lindef import *

# ------------------------------------------------------------------------
# Construct lexer, precompile regex, fill into array

class LinParse():

    def __init__(self, stamps, pvg = None):
        #print("linparse init")
        self.pvg = pvg
        defpvg(pvg)
        funcpvg(pvg)
        self.stamps = stamps
        # Check integrity
        for ss in range(len(self.stamps)):
            pass

    def skiplen(self, stampz):
        ret = 0 ; uprog = 0; umax = len(stampz)
        while 1:
            if uprog >= umax:
                break
            if stampz[uprog][1] & A:
                pass
            #elif stampz[uprog][1] & M:
            #    pass
            else:
                ret += 1
            uprog += 1
        return ret

    def feed(self, arrx, buf):
        self.buf = buf
        self.arrx = arrx
        if self.pvg.verbose > 1:
            print("stamps len =", len(self.stamps), "arrx len =", len(self.arrx))
        if self.pvg.verbose:
            for aa in arrx:
                print(" [", aa.stamp[1], pp(aa.mstr), aa.flag, " ]", end = " ")
                #print(" [", aa, "] ", end = " ")
            print()
        self._feed(0, len(arrx))

    def itemx(self, currstamp, tprog, endd, call):

        '''  Compare items. Return end of scan point '''

        match = 0
        if  self.pvg.pgdebug > 5:
            print("itemx", "tprog =", tprog)

        miss = istamp = iprog = 0
        skiplen = self.skiplen(currstamp)
        while True:
            if istamp >= len(currstamp):
                if self.pvg.pgdebug: print("break on end of stamp")
                break
            while True:
                if tprog + iprog >= endd:
                    break
                if not self.arrx[tprog + iprog].flag:
                    break
                #print("skip",  self.arrx[tprog + iprog])
                iprog += 1

            if tprog + iprog >= endd:
                if  self.pvg.pgdebug > 5:
                    print("break on end of buffer", "tprog =", tprog, "iprog =", iprog)
                    pass
                break
            if currstamp[istamp][1] & P:
                if currstamp[istamp][0] == self.arrx[tprog + iprog].stamp[1]:
                    pass
                else:
                    istamp += 1
            if currstamp[istamp][1] & M:
                # Walk optional multi
                while 1:
                    if currstamp[istamp][0] != self.arrx[tprog + iprog].stamp[1]:
                        break
                    #print("mark", "idx =", self.arrx[tprog + iprog],
                    #                tprog + iprog)
                    self.arrx[tprog + iprog].flag = 1
                    iprog += 1
                istamp += 1
            if currstamp[istamp][1] & A:
                istamp += 2    # End of this expression
                ebound = currstamp[istamp][0]
                #print("accum skip till:", "'"+ebound+"'", end = " => ")
                while 1:
                    #print(self.arrx[tprog + iprog][0][1], end = " ")
                    if ebound == self.arrx[tprog + iprog].stamp[1]:
                        break
                    iprog += 1
                #print()
                #iprog += 1
                if  self.pvg.pgdebug > 6:
                    prarr(self.arrx[tprog : iprog+1], "stamp A opt:")
            #print("before: istamp =", istamp, "iprog =", iprog, "tprog =", tprog)
            if  self.pvg.pgdebug > 5:
                print("[ cstamp:", "'"+currstamp[istamp][0]+"'", "item:",
                              "'"+self.arrx[tprog + iprog][0][1]+"'",
                                "]", end = " ")
            if currstamp[istamp][0] != self.arrx[tprog + iprog].stamp[1]:
                miss = True
                if  self.pvg.pgdebug > 5:
                    print("miss", )
                #iprog += 1    # step forward
                break
            # Complete?
            istamp += 1;
            iprog += 1    # step forward
            if istamp >= skiplen:
                if not miss:
                    #if self.pvg.pgdebug > 3:
                    #    print("stamp match:", "tprog =", tprog,
                    #             "istamp=", istamp, "currstamp =", currstamp);
                    call(self, tprog, iprog )
                    self.restart = True
                    match = True
                break
        #time.sleep(0.1) # this was runaway protection
        return match, iprog

    def stampx(self, idx, start, endd):
        tprog = start
        stamp = self.stamps[idx][0];
        call  = self.stamps[idx][1];
        #print("search stamp =", stamp, "tprog =", tprog)
        while True:
            # Walk all text see if we have a match
            if tprog >= endd:
                #print("stampx: End of data")
                break;
            if self.pvg.pgdebug > 4:
                print("\n stamps:\t",  tprog, end=" " )
                for bb in range(len(stamp)):
                    print(stamp[bb][0], end = " ")
                print("\n", "arrx:", idx, "\t", tprog, end=" ")
                for bb in range(len(stamp)+6):
                    if tprog + bb < len(self.arrx):
                        print(self.arrx[tprog + bb][0][1], end = " ")
            match, xprog = self.itemx(stamp, tprog, endd, call)
            #print("tprog =", tprog, "match =", match, "xprog =", xprog)
            if match:
                break
            if not xprog:
                xprog = 1               # assure forward motion
            tprog += xprog
        return  match

    def _feed(self, start, endd):
        if self.pvg.pgdebug > 5:
            print("_feed: ", start, endd)
        if self.pvg.pgdebug > 3:
            prarr(self.arrx[start : endd], "recu")
        self.restart = False;
        idx = 0
        # Walk all stamps, see if we have a match
        while True:
            if idx >= len(self.stamps):
                if not self.restart:
                    idx = 0
                    break
                idx = 0
                self.restart = False
                if self.pvg.pgdebug: print("restarted at", start)
            #for tprog in range(len(arrx)):
            ret = self.stampx(idx, start, endd)
            if ret:
               idx = 0
            else:
                idx += 1
# EOF
