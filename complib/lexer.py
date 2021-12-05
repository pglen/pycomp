#!/usr/bin/env python

import re, sys

from . import lexdef, stack


# ------------------------------------------------------------------------
#

class _LexIter():

    def __init__(self, self2):
        self.self2 = self2;

    def lexiter(self, state, pos, strx):
        #print (strx[pos:])
        for ss, bb, cc, dd, ee in self.self2.tokens:

            #print (bb, cc)
            if ss != self.self2.state:
                continue

            mmm = dd.match(strx, pos)
            if mmm:
                #print (mmm.end() - mmm.start(), strx[mmm.start():mmm.end()])
                tt = bb, mmm, strx[mmm.start():mmm.end()], dd, ee
                return tt

        return None;

# ------------------------------------------------------------------------

class Lexer():

    def __init__(self, tokens):

        # Pre-compile tokens
        for cnt in range(len(tokens)):
            try:
                tokens[cnt][3] = re.compile(tokens[cnt][2])
            except:
                print("Cannot precomp regex at", cnt, sys.exc_info())
                #raise
                break
            cnt += 1

        #for aa in tokens:
        #    print( aa)

        # Remember args
        self.tokens  = tokens
        self.state =  lexdef.INI_STATE
        self.lexiter = _LexIter(self)
        self.statstack = stack.Stack()
        self.straccum = ""
        self.escaccum = ""

    def feed(self, data, stack):
        lastpos = 0; pos = 0; lenx = len(data)
        while True:
            if pos >= lenx:
                break;
            tt = self.lexiter.lexiter(self, pos, data)
            if tt == None:
                break

            if tt[1]:
                # skip to token end
                pos = tt[1].end()
                #print  (tt[1], "'" + data[tt[1].start():tt[1].end()] + "' - ",)
                #print   ("'" + data[tt[1].start():tt[1].end()] + "' - ",)

                # Fill accumulators:
                if  self.state == lexdef.STR_STATE:
                    self.straccum += tt[2]

                if  self.state == lexdef.ESC_STATE:
                    self.escaccum += tt[2]

                # Change state if needed
                if tt[4] == lexdef.STATE_CHG:
                    if tt[0] ==  lexdef.tokdef["quote"]:
                        #print("Change str state up", tt[0])
                        self.straccum += "\"";
                        self.statstack.push(self.state)
                        self.state = lexdef.STR_STATE

                    elif tt[0] ==  lexdef.tokdef["bs"]:
                        #print("Change bs state up")
                        self.statstack.push(self.state)
                        self.state = lexdef.ESC_STATE

                if tt[4] == lexdef.STATE_DOWN:
                    #print("Change str state down:", _p(self.straccum))
                    sss = list(tt); sss[0] = lexdef.tokdef['strx'];
                    sss[2] = self.straccum
                    stack.push(sss)
                    self.straccum = "\""
                    self.state = self.statstack.pop()

                elif tt[4] == lexdef.STATE_ESCD:
                    #print("Change bs state down:", _p(self.escaccum))
                    self.straccum += self.escaccum
                    self.escaccum = ""
                    self.state = self.statstack.pop()
                    #stack.push(tt)
                else:
                    #print(self.state, tt[0], lexdef.rtokdef[tt[0]], "\t", tt[2])
                    if self.state == lexdef.INI_STATE:
                        stack.push(tt)
            else:
                pos += 1  # step to next char

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF

