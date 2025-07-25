#!/usr/bin/env python

import re, sys

from . import lexdef, stack

from complib.utils import *

class Lex():

    def __init__(self, stampx = [], mstr = "", startx = 0, endx = 0):
        self.state = lexdef.INI_STATE
        self.stamp = stampx
        self.mstr = mstr
        self.start = startx
        self.end = endx
        # Add fields for state information
        self.flag = 0
        self.val = 0.0
        self.ival = 0

    def copy(self, other):
        other.state = self.state

    def __repr__(self):
        return  "[ '" + str(self.stamp[1]) + "' = '" +  \
                        cesc(self.mstr) + "' " + str(self.flag) + " ]"

# ------------------------------------------------------------------------
# Construct lexer, precompile regex, fill into array

class Lexer():

    def __init__(self, xtokens, pvg):

        # Pre-compile tokens
        self.pvg = pvg
        self.tokens = []
        for idx in range(len(xtokens)):
            try:
                 ccc = re.compile(xtokens[idx][2])
            except:
                print("Error: cannot precomp regex at: ", idx,
                            "'", xtokens[idx][2], "'", sys.exc_info())
                raise
            self.tokens.append((xtokens[idx], ccc))

        if self.pvg.lxdebug > 3:
            for aa in self.tokens:
                print("token:", aa)

        # Remember args
        self.state =  lexdef.INI_STATE
        self.statstack = stack.Stack()
        self.startstack = stack.Stack()
        self.straccum = ""
        self.escaccum = ""
        self.strterm = ""
        self.linenum = 0
        self.lastline = 0
        self.start_tt = None

    # Call this for every token

    def _lexiter(self, pos, strx):
        #print (strx[pos:])
        for ttt, vv in self.tokens:
            if ttt[0] != self.state:
                 continue
            mmm = vv.match(strx, pos)
            if mmm:
                #print (mmm.end(), mmm.start(),
                #        "'" + strx[mmm.start():mmm.end()] + "'", end = " ")
                mstr = mmm.string[mmm.start():mmm.end()]
                tt = Lex(ttt, mstr, mmm.start(), mmm.end())
                return tt
        return None;

    def feed(self, data, res):
        lastpos = 0; pos = 0; lenx = len(data)
        while True:
            if pos >= lenx:
                break;
            #raise  ValueError
            tt = self._lexiter(pos, data)
            if tt == None:
                break
            if not tt.end:
                pos += 1  # Step to next char in no match
                continue

            # Update pos, and skip to token end
            beg = pos; pos = tt.end
            if self.pvg.lxdebug > 0:
                print("tt", tt)

            # Global actions
            if  tt.stamp[1] == "nl":
                self.linenum += 1
                if self.pvg.lxdebug > 0:
                    print("Newline at ", tt.mstr, tt.start)
                self.lastline = tt.end
            #print("state =", tt, self.state)

            # Handle back offs
            if tt.stamp[3] == lexdef.STATE_DOWN:
                if self.state == lexdef.STR_STATE:
                    self.straccum += '"';
                    if self.pvg.lxdebug > 2:
                        print("Change str state down:", self.straccum, tt)
                    ttt = self.startstack.pop()
                    tt.mstr = self.straccum
                    tt.start = ttt.start
                    # Update list
                    sss = list(tt.stamp)
                    sss[1] = "strx"
                    ## Back to read only list
                    tt.stamp = tuple(sss)
                    # Emit
                    res.append(tt)
                    #print("accum", self.straccum)
                    self.straccum = ""
                    self.state = self.statstack.pop()

                elif self.state == lexdef.STR_STATE2:
                    self.straccum += "'";
                    if self.pvg.lxdebug > 2:
                        print("Change str state ' down:", self.straccum, tt)
                    ttt = self.startstack.pop()
                    tt.mstr = self.straccum
                    tt.start = ttt.start
                    # Update list
                    sss = list(tt.stamp)
                    sss[1] = "strx"
                    ## Back to read only list
                    tt.stamp = tuple(sss)
                    # Emit
                    res.append(tt)
                    #print("accum2", self.straccum)
                    self.straccum = ""
                    self.state = self.statstack.pop()
                else:
                    pass

            #if tt.stamp[1] ==  "bsla":
            #    #print("Change bs state up")
            #    self.statstack.push(self.state)
            #    self.state = lexdef.ESC_STATE

            if tt.stamp[3] == lexdef.STATE_ESCD:
                #print("Change bs state down:", _p(self.escaccum))
                self.straccum += self.escaccum
                self.escaccum = ""
                self.state = self.statstack.pop()

            if self.state == lexdef.INI_STATE:
                # Change state if needed
                if tt.stamp[1] == "quote":
                    if self.pvg.lxdebug > 0:
                        print("Change str state with", tt)
                    self.strterm = tt.stamp[1]
                    self.straccum = ""
                    self.startstack.push(tt)
                    self.statstack.push(self.state)
                    self.state = lexdef.STR_STATE

                if tt.stamp[1] == "squote":
                    if self.pvg.lxdebug > 0:
                        print("Change str ' state with", tt)
                    self.strterm = tt.stamp[1]
                    self.straccum = ""
                    self.startstack.push(tt)
                    self.statstack.push(self.state)
                    self.state = lexdef.STR_STATE2

                res.append(tt)
            else:
                pass
                #print("no state")

            # Fill accumulators:
            if  self.state == lexdef.STR_STATE:
                #print("accum: ", tt[2])
                self.straccum += tt.mstr

            if  self.state == lexdef.STR_STATE2:
                #print("accum: ", tt[2])
                self.straccum += tt.mstr

            if  self.state == lexdef.ESC_STATE:
                self.escaccum += tt[2]

            #print(self.state, tt.stamp, lexdef.rtok[tt.stamp], "\t", tt[2])

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #print("tok", tokens)

# EOF
