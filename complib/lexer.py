#!/usr/bin/env python

import re, sys

from . import lexdef, stack

from complib.utils import *

class Lex():

    def __init__(self, stampx = [], mstr = "", startx = 0, endx = 0):
        self.state = lexdef.INI_STATE
        self.stamp = stampx
        self.mstr = mstr        # Main payload
        self.start = startx
        self.end = endx
        self.flag = 0           # state information
        self.val = 0.0
        self.ival = 0

    def copy(self, other):
        other.state = self.state
        other.stamp = self.stamp
        other.mstr = self.mstr
        other.start = self.start
        other.end = self.end
        other.flag = self.flag
        other.val = self.val
        other.ival = self.ival

    def __repr__(self):
        return  "[ '" + str(self.stamp[1]) + "' = '" +  \
                        cesc(self.mstr) + "' " + str(self.flag) + " ]"
    def __str__(self):
        return(self.__repr__())

    def dump(self):
        return  "[ '" + str(self.stamp[1]) + "' = '" +  \
                        cesc(self.mstr) + "'" + \
                        " flag=" + str(self.flag) + \
                        " pos=" + str(self.start) + ":" + str(self.end) +  \
                        " val=" + str(self.val) + \
                        " ival=" + str(self.ival) + \
                        " ]"

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

        self.lastpos = 0;
        self.state =  lexdef.INI_STATE
        self.statstack = stack.Stack()
        self.startstack = stack.Stack()
        self.straccum = ""
        self.escaccum = ""
        self.strterm = ""
        self.linenum = 0
        self.lastline = 0
        self.start_tt = None

    def _lexiter(self, pos, strx):

        '''  Call this for every token '''

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

    def _set_state(self, tt, state):
        self.strterm = tt.stamp[1]
        self.straccum = ""
        self.startstack.push(tt)
        self.statstack.push(self.state)
        self.state = state

    def _down_state(self, tt, typex):

        ttt = self.startstack.pop()
        tt.mstr = self.straccum
        tt.start = ttt.start
        # Update list
        sss = list(tt.stamp)
        sss[1] = typex
        ## Back to read only list
        tt.stamp = tuple(sss)
        self.straccum = ""
        self.state = self.statstack.pop()

    def feed(self, data, res):

        ''' Data comes in here, emit results at res '''

        pos = 0; lenx = len(data)
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
            if self.pvg.lxdebug > 2:
                print("token:", tt, "state =", self.state)

            self.lastpos = pos

            # Global actions
            if  tt.stamp[1] == "nl":
                self.linenum += 1
                if self.pvg.lxdebug > 1:
                    print("Newline at ", tt.start)
                self.lastline = tt.end
            #print("state =", tt, self.state)

            if self.state == lexdef.INI_STATE:
                # Change state if needed
                if tt.stamp[1] == "quote":
                    if self.pvg.lxdebug > 0:
                        print("Change to str state with", tt)
                    self._set_state(tt, lexdef.STR_STATE)

                elif tt.stamp[1] == "squote":
                    if self.pvg.lxdebug > 0:
                        print("Change to str2 state with", tt)
                    self._set_state(tt, lexdef.STR_STATE2)

                elif tt.stamp[1] == "comm3":
                    if self.pvg.lxdebug > 0:
                        print("Change to comm3 state with", tt,
                                    "state =", lexdef.COMM_STATE)
                    self._set_state(tt, lexdef.COMM_STATE)
                else:
                    #print("no state")
                    res.append(tt)

            # Handle back offs
            elif tt.stamp[1] == "dquote": # and self.state == lexdef.STR_STATE:
                self.straccum += '"';
                if self.pvg.lxdebug > 0:
                    print("Change str state down:", self.straccum, tt)
                self._down_state(tt, "strx")
                res.append(tt)    # Emit

            elif tt.stamp[1] == "dsquote": # self.state == lexdef.STR_STATE2:
                self.straccum += "'";
                if self.pvg.lxdebug > 0:
                    print("Change str state2 down:", self.straccum, tt)
                self._down_state(tt, "strx")
                res.append(tt)    # Emit

            elif tt.stamp[1] == "ecomm3": # self.state == lexdef.COMM_STATE:
                self.straccum += "'";
                if self.pvg.lxdebug > 0:
                    print("Change comm state down:",
                                self.straccum, tt, lexdef.COMM_STATE)
                self._down_state(tt, "comm3")
                res.append(tt)    # Emit

                #elif tt.stamp[1] == ""bs";
                #    #print("Change bs state down:", _p(self.escaccum))
                #    self.straccum += self.escaccum
                #    self.escaccum = ""
                #    self.state = self.statstack.pop()

                #if tt.stamp[1] ==  "bsla":
                #    #print("Change bs state up")
                #    self.statstack.push(self.state)
                #    self.state = lexdef.ESC_STATE
            else:
                pass

            # Default to fill accumulators:
            if  self.state == lexdef.STR_STATE:
                #print("accum: ", tt[2])
                self.straccum += tt.mstr

            if  self.state == lexdef.STR_STATE2:
                #print("accum: ", tt[2])
                self.straccum += tt.mstr

            if  self.state == lexdef.COMM_STATE:
                #print("accum: ", tt[2])
                self.straccum += tt.mstr

            if  self.state == lexdef.ESC_STATE:
                self.escaccum += tt[2]

            #print(self.state, tt.stamp, lexdef.rtok[tt.stamp], "\t", tt[2])

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #print("tok", tokens)

# EOF
