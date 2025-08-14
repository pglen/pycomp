#!/usr/bin/env python

#import re, sys

from complib.utils  import *
from complib.linfunc import *
from complib.lindef import *

# ------------------------------------------------------------------------
# Construct lexer, precompile regex, fill into array

class LinParse():

    def __init__(self, stamps, pvg = None):
        print("linparse init", pvg)
        self.pvg = pvg
        defpvg(pvg)
        funcpvg(pvg)
        self.stamps = stamps
        self.state = 0
        self.context = 0
        # Check integrity
        #for ss in range(len(self.stamps)):
        #    pass
        # Print stamps:
        #for ss in range(len(self.stamps)):
        #    print(self.stamps[ss][1])

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

        if self.pvg.opt_verbose.cnt > 2:
            print("stamps len =", len(self.stamps), "arrx len =", len(self.arrx))

        #if self.pvg.debug:
        #    for aa in arrx:
        #        print(" [", aa.stamp[1], pp(aa.mstr), aa.flag, " ]", end = " ")
        #        #print(" [", aa, "] ", end = " ")
        #    print()

        self._feed(0, len(self.arrx))

        #return self.arrx

    def itemx(self, idx, tprog, endd, call):

        '''  Compare items. Return end of scan point '''

        currstamp = self.stamps[idx][1];

        if self.pvg.opt_debug > 6:
            print("  itemx", "tprog =", tprog, "endd =", endd)

        match = miss = istamp = iprog = 0
        skiplen = self.skiplen(currstamp)
        while True:
            if istamp >= len(currstamp):
                if self.pvg.opt_debug: print("break on end of stamp")
                break
            # Skip already calculated values and skip markers
            while True:
                if tprog + iprog >= endd:
                    break
                if self.arrx[tprog + iprog].flag == 0:
                    break
                if self.pvg.opt_debug > 6:
                    print("skip",  tprog, iprog, self.arrx[tprog + iprog])
                iprog += 1
            if tprog + iprog >= endd:
                if  self.pvg.opt_debug > 5:
                    print("break on end of buffer", "tprog =", tprog, "iprog =", iprog)
                break
            #print("scan:", "'", self.arrx[tprog + iprog].mstr, "'", end = " ")
            if currstamp[istamp][1] & P:
                if currstamp[istamp][0] != self.arrx[tprog + iprog].stamp[1]:
                    istamp += 1
            if currstamp[istamp][1] & M:
                # Walk optional multi
                while True:
                    if tprog + iprog >= endd:
                        break
                    if self.arrx[tprog + iprog].flag == 1:
                        iprog += 1
                        continue
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
                    if tprog + iprog >= endd:
                        break
                    #print(self.arrx[tprog + iprog][0][1], end = " ")
                    if ebound == self.arrx[tprog + iprog].stamp[1]:
                        break
                    #self.arrx[tprog + iprog].flag = 1
                    iprog += 1
                #print()
                #iprog += 1
                if  self.pvg.opt_debug > 6:
                    prarr(self.arrx[tprog : iprog+1], "stamp A opt:")
            #print("before: istamp =", istamp, "iprog =", iprog, "tprog =", tprog)
            if tprog + iprog >= endd:
                if  self.pvg.opt_debug > 5:
                    print("break on end of buffer", "tprog =", tprog, "iprog =", iprog)
                break

            if  self.pvg.opt_debug > 5:
                sss = self.arrx[tprog + iprog].mstr
                print(" cmp: idx=%d tprog=%d iprog=%d istamp=%d"  % \
                                    (idx, tprog, iprog, istamp),
                                "stamp='"+currstamp[istamp][0]+"'",
                                    "item='"+self.arrx[tprog + iprog].stamp[1]+"'",
                                        "mstr='"+sss+"'")

            if currstamp[istamp][0] != self.arrx[tprog + iprog].stamp[1]:
                miss = True
                if  self.pvg.opt_debug > 7:
                    print("    miss:", "'" + self.arrx[tprog + iprog].mstr + "'")
                break
            # Complete?
            istamp += 1;
            iprog += 1    # step forward
            if istamp >= skiplen:
                if not miss:
                    if self.pvg.opt_debug > 5:
                        #print("stamp match:", "tprog =", tprog, "iprog =", iprog)
                        #print( " curr =", currstamp);
                        prarr(self.arrx[tprog:tprog+iprog], " match idx=%d arrx = " % idx)
                    call(self, tprog, iprog )
                    if self.pvg.opt_debug > 6:
                        #prarr(self.arrx[tprog:tprog+iprog], " post arrx = ", True)
                        prarr(self.arrx, " post arrx = ", True)
                    match = True
                    break
        #time.sleep(0.1) # this was runaway protection
        return match, iprog

    def stampx(self, idx, start, endd):
        tprog = start
        if  self.stamps[idx][0] != self.state:
            if self.pvg.opt_debug > 0:
                print("Out of state:", self.state, "idx = ", idx)
            return False
        stamp = self.stamps[idx][1];
        call  = self.stamps[idx][2];
        if self.pvg.opt_debug > 6:
            print("stampx idx =", idx, "start =", start, "endd =", endd)
        matchx = 0
        while True:
            # Walk all text see if we have a match
            if tprog >= endd:
                #print("stampx: End of data")
                break;
            if self.pvg.opt_debug > 6:
                print("\n stamps:\t",  tprog, end=" " )
                for bb in range(len(stamp)):
                    print(stamp[bb][0], end = " ")
                print("\n", "arrx:", idx, "\t", tprog, end=" ")
                for bb in range(len(stamp)+6):
                    if tprog + bb < len(self.arrx):
                        print(self.arrx[tprog + bb].stamp[1], end = " ")
            matchx, xprog = self.itemx(idx, tprog, endd, call)
            #print("tprog =", tprog, "match =", match, "xprog =", xprog)
            if matchx:
                break
            if not xprog:
                xprog = 1               # assure forward motion
            tprog += xprog
        return  matchx

    def _feed(self, start, endd):
        if self.pvg.opt_debug > 5:
            print("_feed: ", start, endd)
        if self.pvg.opt_debug > 6:
            prarr(self.arrx[start : endd], "recu")
        sprog = start
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
                sprog = 0
                if self.pvg.opt_debug:
                    print("restarted at", start)

            #print("stampx", idx, sprog, endd)

            redo = self.stampx(idx, sprog, endd)
            if redo:
                idx = 0
                sprog = 0
                if self.pvg.opt_debug > 6:
                    print("redo, sprog =", sprog)
            else:
                idx += 1
# EOF
