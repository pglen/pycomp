#!/usr/bin/env python

import re, sys

from . import lexdef, stack

class Lex():

    def __init__(self, stampx, mstr, startx, endx):
        self.state = 0
        self.stamp = stampx
        self.mstr = mstr
        self.start = startx
        self.end = endx
        self.flag = 0
        self.val = 0.0
        self.ival = 0

    def __repr__(self):
        return  "[ '" + str(self.stamp[1]) + "' = '" +  \
                        self.mstr + "' " + str(self.flag) + " ]"

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

        if self.pvg.verbose > 2:
            for aa in self.tokens:
                print("token:", aa)

        # Remember args
        self.state =  lexdef.INI_STATE
        self.statstack = stack.Stack()
        self.straccum = ""
        self.escaccum = ""
        self.linenum = 0
        self.lastline = 0
        self.start_tt = None

    # Call this for every token

    def _lexiter(self, pos, strx):
        #print (strx[pos:])
        for ttt, vv in self.tokens:
            #print (ttt, vv)
            if ttt[0] != self.state:
                 continue
            mmm = vv.match(strx, pos)
            if mmm:
                #print (mmm.end() - mmm.start(), strx[mmm.start():mmm.end()])
                mstr = mmm.string[mmm.start():mmm.end()]
                # Add empty at end for state information
                tt = Lex(ttt, mstr, mmm.start(), mmm.end())
                return tt
        return None;

    def feed(self, data, res):
        lastpos = 0; pos = 0; lenx = len(data)
        while True:
            if pos >= lenx:
                break;
            tt = self._lexiter(pos, data)
            #print(tt)
            if tt == None:
                break
            if tt.end:
                # skip to token end
                beg = pos; pos = tt.end
                #print("tt", tt)
                #if  tt[1] == "sp":
                #    continue
                if  tt.mstr == "nl":
                    self.linenum += 1
                    print("Newline at ", tt.mstr, pos)
                    self.lastline = beg

                #tt.append(self.linenum)
                #tt.append(beg - self.lastline)
                #print(tt)

                # Change state if needed
                if tt.stamp[3] != lexdef.STATE_NOCH:
                    #if tt.stamp[1] ==  "quote":
                    if tt.stamp[3] == lexdef.STR_STATE:
                        #print("Change str state with", tt[2])
                        self.straccum = ""
                        self.start_tt = tt
                        self.statstack.push(self.state)
                        self.state = lexdef.STR_STATE

                    elif tt.stamp[1] ==  "bsl":
                        #print("Change bs state up")
                        self.statstack.push(self.state)
                        self.state = lexdef.ESC_STATE

                if tt.stamp[3] == lexdef.STATE_DOWN:
                    if self.state == lexdef.STR_STATE:
                        #print("Change str state down:", self.straccum)
                        self.straccum += '"';

                        # This converts the read only list
                        ttt = list(tt)
                        ttt.stamp = list(ttt.stamp)
                        ttt.stamp[1] = 'strx';
                        ttt[1] = self.straccum
                        ttt[2] = self.start_tt[2]
                        #print("ttt", ttt)
                        # BAck to read only list
                        ttt.stamp = tuple(ttt.stamp)
                        ttt = tuple(ttt)
                        #stack.push(ttt)
                        res.append(ttt)

                    #print("accum", self.straccum)
                    self.straccum = ""
                    self.state = self.statstack.pop()

                elif tt.stamp[3] == lexdef.STATE_ESCD:
                    #print("Change bs state down:", _p(self.escaccum))
                    self.straccum += self.escaccum
                    self.escaccum = ""
                    self.state = self.statstack.pop()
                else:
                    if self.state == lexdef.INI_STATE:
                        #stack.push(tt)
                        res.append(tt)

                # Fill accumulators:
                if  self.state == lexdef.STR_STATE:
                    #print("accum: ", tt[2])
                    self.straccum += tt[1]

                if  self.state == lexdef.ESC_STATE:
                    self.escaccum += tt[2]

                #print(self.state, tt.stamp, lexdef.rtok[tt.stamp], "\t", tt[2])
            else:
                pos += 1  # step to next char

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #print("tok", tokens)

# EOF

