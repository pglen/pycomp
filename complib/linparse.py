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
        self.state = ST.val("STATEINI")
        self.context = 0
        #stamps = stamps

        # Check integrity
        #for ss in range(len(stamps)):
        #    pass
        # Print stamps:
        #for ss in range(len(stamps)):
        #    print(stamps[ss][1])

    def feed(self, arrx, buf):

        ''' Feed the buffer to '''

        self.buf = buf; self.arrx = arrx

        if self.pvg.opt_verbose.cnt > 2:
            print("stamps len =", len(stamps), "arrx len =", len(self.arrx))

        if self.pvg.opt_debug > 6:
            print("arrx:")
            for aa in arrx:
                if self.pvg.opt_verbose.cnt:
                    print(" [", aa, "] ", end = " ")
                else:
                    print(" [", aa.stamp[1], pp(aa.mstr), aa.flag, " ]", end = " ")
            print("\nend arrx.")

        startx = 0 ; endd = len(self.arrx)
        # Walk all locations, see if we have a match
        while True:
            if startx >= endd:
                if self.pvg.opt_debug > 6:
                    print("stamp_iter: End of data")
                break
            match, prog = self.stamps_iter(startx, endd)
            # None of the tokens match:
            if not match:
                break
            else:
                startx += prog

        if startx >= endd:
            pass
        else:
            if not match:
                posx = self.arrx[startx]
                print("Parse error:", "line:", posx.linenum + 1,
                                "col:", posx.start - posx.linestart + 1 )
                pos = 0
                # Till end of this line
                for aa in range(posx.linestart, len(self.buf)):
                    if self.buf[aa] == "\n":
                        pos = aa
                        break

                #print("aa", self.buf[posx.linestart:pos])
                print(self.buf[posx.linestart:pos])
                print("-" *  (posx.end - posx.linestart), end = "" )
                print("^")
                #print("-" *  (pos - posx.end))





        #print("end scan")

    def stamps_iter(self, startx, endd):

        ''' Iterate all stamps at startx offset '''

        if self.pvg.opt_debug > 3:
            print("stamp_iter()", "startx =", startx, "endd =", endd)

        matchx = 0 ; xprog = 0; stidx = 0
        while True:
            # Walk all stamps
            if  stidx >= len(stamps):
                if self.pvg.opt_debug > 6:
                    print("stamp_iter: End of stamps")
                break

            matchx, xprog = self.itemx(stidx, startx, endd)
            if matchx:
                break
            stidx += 1

        # No matter what, step forward
        if xprog == 0:
            xprog = 1

        return  matchx, xprog

    def itemx(self, sidx, tprog, endd):

        '''  Compare token at sidx to buf at tprog. Call actions
            if found.  Obey optional and multi items.
            Return end of scan point.
        '''
        match = False ; iprog = 1   # Always advance

        if  stamps[sidx].state != self.state:
            if self.pvg.opt_debug > 0:
                print("Out of state:", self.state, "idx = ", idx)
            return match, iprog
        #breakpoint()
        #print("stamp", stamps[idx])
        currstamp = stamps[sidx].token
        currtoken = self.arrx[tprog].stamp[1]

        if self.pvg.opt_debug > 5:
            print("    stamp:", pp(currstamp), "token:", pp(currtoken))

        # ----------------------------------------------------------------
        # Compare current position to ONE stamp

        if currstamp == currtoken:
            if self.pvg.opt_debug > 2:
                print("  Match at:",  tprog, "stamp:", pp(currstamp), "token:", pp(currtoken))
            match = True
            iprog = len(self.arrx[tprog].mstr)
            stamps[sidx].call(self, tprog, 0)
            if self.pvg.opt_emit:
                emit("match:", currtoken)
        else:
            #print("misMatch")
            pass

        if self.pvg.opt_animate:
            time.sleep(0.01) # this case was for runaway display

        #if  self.pvg.opt_debug > 2:
        #    print("itemx return:", match, iprog)

        return match, iprog

# EOF
