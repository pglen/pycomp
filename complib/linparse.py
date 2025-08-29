#!/usr/bin/env python

import complib.stack as stack

from complib.utils  import *
from complib.lindef import *
from complib.ptree import *
from complib.linfunc import *

row = 0

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
        self.statestack = stack.pStack(True)
        self.statestack.push(ST.val("STATEINI"))

        # Print stamps:
        #for ss in range(len(stamps)):
        #    print("st", stamps[ss].token)

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
                    print(" [", aa.stamp.xstr, pp(aa.mstr), aa.flag, " ]", end = " ")
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
                pos = 0
                # Till end of this line
                for aa in range(posx.linestart, len(self.buf)):
                    if self.buf[aa] == "\n":
                        pos = aa
                        break
                #print("aa", self.buf[posx.linestart:pos])
                print(self.buf[posx.linestart:pos])
                print("-" *  (posx.end - posx.linestart - 1), end = "" )
                print("^")
                print("Parse \033[31;1merror:\033[0m", "line:", posx.linenum + 1,
                                "col:", posx.start - posx.linestart )
                #print("-" *  (pos - posx.end))

        #print("end scan")

    def stamps_iter(self, startx, endd):

        ''' Iterate all stamps at startx offset '''

        if self.pvg.opt_debug > 5:
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
        currstamp = stamps[sidx]
        currtoken = self.arrx[tprog]

        match = False ; iprog = 1   # Always advance

        if stamps[sidx].state != ST.val("STATEANY"):
            if  stamps[sidx].state != self.state:
                if self.pvg.opt_debug > 7:
                    print("Out of state:", ST.get(stamps[sidx].state), "state:",
                            ST.get(self.state),
                                "token:", stamps[sidx].token,
                                    "tprog", tprog)
                return match, iprog

        #breakpoint()
        #print("stamp", stamps[idx])

        if self.pvg.opt_debug > 5:
            print("    stamp:", pp(currstamp.token), "token:", pp(currtoken.stamp.xstr))

        # ----------------------------------------------------------------
        # Compare current position to ONE stamp

        if currstamp.token == currtoken.stamp.xstr:
            match = True
            if self.pvg.opt_debug > 6:
                if currstamp.nstate != ST.val("STIGN"):
                    print(" sState;", ST.get(self.state))

            if self.pvg.opt_debug > 2:
                if  currtoken.stamp.xstr != "sp":    # no sp display
                    xprintf(#"tprog =", tprog,
                            #"state:",  ST.get(self.state),
                            #"stamp:", pp(currstamp.token),
                            "tok:", #padx(pp(currtoken.stamp.xstr), 7),
                            #" =",
                            padx(pp(currtoken.mstr, 6), 5),
                            end = " ")
                    global row
                    rrr =  6
                    if row % rrr == rrr - 1:
                        print()
                    row += 1
            #iprog = len(self.arrx[tprog].mstr)
            if currstamp.call:
                currstamp.call(self, tprog)

            # Switch state as instructed
            if currstamp.nstate != ST.val("STATEANY") and \
                    currstamp.nstate != ST.val("STIGN"):
                if currstamp.nstate == ST.val("STPOP"):
                    self.state = self.statestack.pop()
                    if self.pvg.opt_debug > 4:
                        print("pop state", ST.get(self.state))
                elif currstamp.nstate == ST.val("STPOP2"):
                    self.state = self.statestack.pop()
                    self.state = self.statestack.pop()
                    if self.pvg.opt_debug > 4:
                        print("pop state2", ST.get(self.state))
                else:
                    if  currstamp.push:
                        self.statestack.push(self.state)
                    self.state = currstamp.nstate

            if self.pvg.opt_debug > 4:
                if currstamp.nstate != ST.val("STIGN"):
                    print(" eState;", ST.get(self.state))

            global lastnode
            if currstamp.nstate != ST.val("STIGN"):
                lastnode = lastnode.add(TreeNode(currtoken.stamp.xstr))
                #if self.pvg.opt_emit:
                #    emit("match:", currtoken.stamp.xstr)
        else:
            #print("misMatch")
            pass

        if self.pvg.opt_animate:
            time.sleep(0.01) # this case was for runaway display

        if  self.pvg.opt_debug > 7:
            print("itemx return:", match, iprog)

        return match, iprog

# EOF
