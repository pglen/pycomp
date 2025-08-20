#!/usr/bin/env python

from complib.utils  import *
from complib.linfunc import *
from complib.lindef import *

# ------------------------------------------------------------------------
# Construct lexer, precompile regex, fill into array

class LinParse():

    def __init__(self, stamps, pvg = None):
        #print("linparse init", pvg)
        self.pvg = pvg
        defpvg(pvg)
        funcpvg(pvg)
        self.stamps = stamps
        self.state = STATEINI
        self.context = 0

        # Check integrity
        #for ss in range(len(self.stamps)):
        #    pass
        # Print stamps:
        #for ss in range(len(self.stamps)):
        #    print(self.stamps[ss][1])

    def skiplen(self, stampz):

        '''  '''

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

        ''' Feed the buffer to '''

        self.buf = buf; self.arrx = arrx
        if self.pvg.opt_verbose.cnt > 2:
            print("stamps len =", len(self.stamps), "arrx len =", len(self.arrx))

        if self.pvg.opt_debug > 6:
            print("arrx:")
            for aa in arrx:
                if self.pvg.opt_verbose.cnt:
                    print(" [", aa, "] ", end = " ")
                else:
                    print(" [", aa.stamp[1], pp(aa.mstr), aa.flag, " ]", end = " ")
            print("\nend arrx.")

        self._feed(0, len(self.arrx))

        #return self.arrx

    def itemx(self, idx, tprog, endd, call):

        '''  Compare items. Call actions if found.  Obey optional and
            multi items. Return end of scan point.
        '''
        #print("stamp", self.stamps[idx])
        currstamp = self.stamps[idx]
        if self.pvg.opt_debug > 6:
            print(pvar(currstamp), pvar(tprog))
            #print(pvar(self.arrx))
            pass
        #breakpoint()
        match = istamp = iprog = 0

        # ----------------------------------------------------------------
        # Loop over ONE stamp
        while True:
            if istamp >= len(currstamp):
                if self.pvg.opt_debug > 5:
                    print("break on end of stamp")
                break
            if tprog + iprog >= endd:
                if self.pvg.opt_debug > 5:
                    print("break on end of data")
                break

            # Skip already calculated values and skip markers
            #while True:
            #    if tprog + iprog >= endd:
            #        break
            #    #if self.arrx[tprog + iprog].flag == 0:
            #    #    break
            #    if self.pvg.opt_debug > 7:
            #        print("skip pre:",  tprog, iprog, self.arrx[tprog + iprog])
            #    iprog += 1
            #if tprog + iprog >= endd:
            #    if  self.pvg.opt_debug > 5:
            #        print("break on end of buffer",)
            #        #"tprog =", tprog, "iprog =", iprog)
            #    break

            if self.pvg.opt_debug > 5:
                print("cmp:", pp(currstamp[istamp][0]), "vs",
                                pp(self.arrx[tprog + iprog].stamp[1]) )
                #pvar(tprog, ""), pvar(iprog, ""),

            # Compare current stamp, current item
            if currstamp[istamp][0] != self.arrx[tprog + iprog].stamp[1]:
                # Optional item does not terminate search
                #if currstamp[istamp][1] & P:
                #    if currstamp[istamp][0] != self.arrx[tprog + iprog].stamp[1]:
                #        if  self.pvg.opt_debug > 2:
                #            print("  opt stamp:", "'" + currstamp[istamp][0] + "'",
                #                            "item: ",
                #                            "'" + self.arrx[tprog + iprog].stamp[1] + "'")
                #            #print("    skip at:", pvar(tprog), pvar(iprog))
                #        #istamp += 1
                #        iprog += 1
                #    continue
                #else:
                #    miss = True
                #    if  self.pvg.opt_debug > 3:
                #        print("    miss:", pp(self.arrx[tprog + iprog].stamp[1]))
                #    break
                if self.pvg.opt_debug > 3:
                    print("    mismatch:", pp(currstamp[istamp][0]), "vs",
                                    pp(self.arrx[tprog + iprog].stamp[1]))
                match = False
                break
            else:
                match = True
                if self.pvg.opt_debug > 3:
                    print("    match:", pp(currstamp[istamp][0]), end = " ")

            #if  self.pvg.opt_debug > 3:
            #    print("scan:", "'", self.arrx[tprog + iprog].mstr, "'", end = " ")

            if istamp >= len(currstamp):
                if self.pvg.opt_debug > 5: print("break on end of stamp")
                break

            #if currstamp[istamp][1] & M:
            #    # Walk multi
            #    while True:
            #        if tprog + iprog >= endd:
            #            break
            #        #if self.arrx[tprog + iprog].flag == 1:
            #        #    iprog += 1
            #        #    continue
            #        if currstamp[istamp][0] != self.arrx[tprog + iprog].stamp[1]:
            #            break
            #        if  self.pvg.opt_debug > 5:
            #            print("     mark idx:", self.arrx[tprog + iprog],
            #                        tprog + iprog)
            #        #self.arrx[tprog + iprog].flag = 1
            #        iprog += 1
            #    iprog += 1 ; istamp += 1

            if istamp >= len(currstamp):
                if self.pvg.opt_debug > 5: print("break on end of stamp2")
                break

            #if currstamp[istamp][1] & A:
            #    istamp += 2    # End of this expression
            #    ebound = currstamp[istamp][0]
            #    #print("accum skip till:", "'"+ebound+"'", end = " => ")
            #    while 1:
            #        if tprog + iprog >= endd:
            #            break
            #        #print(self.arrx[tprog + iprog][0][1], end = " ")
            #        if ebound == self.arrx[tprog + iprog].stamp[1]:
            #            break
            #        #self.arrx[tprog + iprog].flag = 1
            #        iprog += 1
            #    if  self.pvg.opt_debug > 6:
            #        prarr(self.arrx[tprog : iprog+1], "stamp A opt:")

            if  self.pvg.opt_debug > 5:
                print("curr line:", pvar(istamp),  pvar(iprog), pvar(tprog))

            if tprog + iprog >= endd:
                if  self.pvg.opt_debug > 5:
                    print("break on end of buffer2", "tprog =", tprog, "iprog =", iprog)
                break

            #if  self.pvg.opt_debug > 5:
            #    sss = self.arrx[tprog + iprog].mstr
            #    print(" cmp: idx=%d tprog=%d iprog=%d istamp=%d"  % \
            #                        (idx, tprog, iprog, istamp),
            #                    "stamp='"+currstamp[istamp][0]+"'",
            #                        "item='"+self.arrx[tprog + iprog].stamp[1]+"'",
            #                            "mstr='"+sss+"'")

            istamp += 1 ; iprog += 1    # step forward

            # Complete?
            if istamp >= len(currstamp): #skiplen:
                #if not miss:
                #    if self.pvg.opt_debug > 3:
                #        print("stamp match:", "tprog =", tprog, "iprog =", iprog)
                #        #print( " curr =", currstamp);
                #        prarr(self.arrx[tprog:tprog+iprog], " match idx=%d arrx = " % idx)
                #    call(self, tprog, iprog )
                #    if self.pvg.opt_debug > 6:
                #        #prarr(self.arrx[tprog:tprog+iprog], " post arrx = ", True)
                #        prarr(self.arrx, " post arrx = ", True)
                #    match = True
                #    break
                break

        if self.pvg.opt_animate:
            time.sleep(0.1) # this case was for runaway display

        if  self.pvg.opt_debug > 5:
            print("return", match, iprog)
        return match, iprog

    def stamps_iter(self, idx, startx, endd):

        ''' Iterate all stamps at startx offset '''

        tprog = startx
        if  self.stamps[idx].state != self.state:
            if self.pvg.opt_debug > 0:
                print("Out of state:", self.state, "idx = ", idx)
            return False
        if self.pvg.opt_debug > 5:
            print("stamp_iter idx =", idx, "startx =", startx, "endd =", endd)
        matchx = 0
        while True:
            # Walk all text see if we have a match
            if tprog >= endd:
                if self.pvg.opt_debug > 6:
                    print("stamp_iter: End of data")
                break;
            if self.pvg.opt_debug > 6:
                print("\n stamps:\t",  tprog, end=" " )
                for bb in range(len(stamp)):
                    print(stamp[bb].item, end = " ")

                print("\n", "arrx:", idx, "\t", tprog, end=" ")

                for bb in range(len(stamp)+6):
                    if tprog + bb < len(self.arrx):
                        print(self.arrx[tprog + bb].stamp.item, end = " ")
            matchx, xprog = self.itemx(idx, tprog, endd, self.stamps[0].call)
            if self.pvg.opt_debug > 6:
                print("after itemx tprog =", tprog, "match =", match, "xprog =", xprog)
            if not matchx:
                posx = self.arrx[tprog]
                print("Parse error:", "line:", posx.linenum + 1, "col:", posx.start - posx.linestart + 1 )
                pos = 0
                # Till end of this line
                for aa in range(posx.linestart, len(self.buf)):
                    if self.buf[aa] == "\n":
                        pos = aa
                        break
                #print("aa", self.buf[posx.linestart:pos])
                print(self.buf[posx.linestart:aa])
                print("-" *  (posx.end - posx.linestart), end = "" )
                print("^")
                #print("-" *  (pos - posx.end))
                break

            # No matter what, step forward
            if xprog == 0:
                xprog = 1

            tprog += xprog
            #if matchx:
            #    break
            #return  matchx

    def _feed(self, start, endd):
        if self.pvg.opt_debug > 5:
            print("_feed: ", start, endd)
        if self.pvg.opt_debug > 6:
            prarr(self.arrx[start : endd], "recu")
        sprog = start
        sidx = 0
        # Walk all stamps, see if we have a match
        while True:
            prog = self.stamps_iter(sidx, sprog, endd)



# EOF
