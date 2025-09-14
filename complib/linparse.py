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
        #    print("st", stamps[ss].tokens)

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
                    print("feed(): End of data")
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
                error(self, "Parse")
        #print("end scan")
        if self.state !=  ST.val("STATEINI"):
            print("Warn: unexpected parse state:", pp(ST.get(self.state)), "on exit.")

    def stamps_iter(self, startx, endd):

        ''' Iterate all stamps at startx offset '''

        #if self.pvg.opt_debug > 4:
        #    print("stamps_iter()", "startx =", startx, "endd =", endd)

        matchx = 0 ; xprog = 0; stidx = 0
        self.startx = startx
        while True:
            # Walk all stamps
            if  stidx >= len(stamps):
                if self.pvg.opt_debug > 6:
                    print("stamps_iter: End of stamps")
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
        #print("state", type(stamps[sidx].state), stamps[sidx].state)
        if ST.val("STATEANY") not in stamps[sidx].state:
            if  self.state not in stamps[sidx].state:
                if self.pvg.opt_debug > 9:
                    sss = ""
                    for aa in stamps[sidx].state:
                        sss += ST.get(aa)
                    print("Out of state:", "state: [",  sss, "]",
                            ST.get(self.state),
                                "token:", stamps[sidx].tokens,
                                    "tprog", tprog)
                return match, iprog
        #breakpoint()
        #print("stamp", stamps[idx])

        if self.pvg.opt_debug > 6:
            print("    stamp:", pp(currstamp.tokens), "token:", pp(currtoken.stamp.xstr))

        # ----------------------------------------------------------------
        # Compare current position to ONE stamp

        if currtoken.stamp.xstr in currstamp.tokens:
            match = True
            if self.pvg.opt_debug > 6:
                if currstamp.nstate != ST.val("STIGN"):
                    print(" sState;", ST.get(self.state))

            if self.pvg.opt_debug > 2:
                if  currtoken.stamp.xstr != "sp":    # no sp display
                    xprintf( \
                            #"state:",  ST.get(self.state),
                            #"stamp:", pp(currstamp.token),
                            #padx(pp(currtoken.stamp.xstr), 7),
                            #padx(pp(currtoken.mstr, 6), 5),
                            "tok:", pp(currtoken.mstr),
                            "tprog =", tprog,
                            )
                            #end = " ")
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
                    #if self.pvg.opt_debug > 4:
                    #    for aa in self.statestack:
                    #        print("statestack:", aa)
                    if self.pvg.opt_debug > 4:
                        print("pop state", ST.get(self.state), end = " ")
                    self.state = self.statestack.pop()
                    if self.pvg.opt_debug > 4:
                        print("pop to:", ST.get(self.state), end = " \n")

                    # Re-feed this token to the stack:
                    if  self.statestack.getlen() > 0:
                        #print("re-feed", ST.get(self.state))
                        self.stamps_iter(tprog, endd )

                elif currstamp.nstate == ST.val("STPOP2"):
                    if self.pvg.opt_debug > 4:
                        print("pop state2", ST.get(self.state), end = " ")
                    self.state = self.statestack.pop()
                    self.state = self.statestack.pop()
                    if self.pvg.opt_debug > 4:
                        print("pop to:", ST.get(self.state), end = " ")
                else:
                    if  currstamp.push:
                        if self.pvg.opt_debug > 4:
                            print("push:", ST.get(self.state), end = " ")
                        self.statestack.push(self.state)
                        #if self.pvg.opt_debug > 4:
                        #    for aa in self.statestack:
                        #        print("statestack:", aa)
                    self.state = currstamp.nstate
                    if self.pvg.opt_debug > 4:
                        print("state to:", ST.get(self.state), end = "\n")

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
