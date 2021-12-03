#!/usr/bin/env python

import sys, os, re

# Our modules
from . import stack, lexer

from complib.utils import *

'''
The parser needs several variables to operate.
  Quick summary of variables:
     Token definitions, Lexer tokens, Parser functions,
      Parser states, Parse state table.
See pangparser.py for documentation and examples.
'''

_gl_cnt = 0
def uniq_next():             # create a unique temporary number
    global _gl_cnt; _gl_cnt+= 10
    return _gl_cnt


# This variable controls the display of the default action.
# The default action is executed when there is no rule for the
# expression. Mostly useful for debugging the grammar.

#_show_default_action = False
_show_default_action = True


# May be redefined, included here for required initial states:

STA_ANY         = [-2, "anystate"]
STA_REDUCE      = [-1, "reduce"]
STA_IGNORE      = [punique(), "ignore"]
STA_INIT        = [punique(), "init"]

# ------------------------------------------------------------------------
# This parser creates no error conditions. Bad for languages, good
# for text parsing. Warnings can be generated by enabling the
# 'show_default' action.
# The parser is not fully recursive, so states need to be nested by
# hand. The flat parser is an advantage for text processing.

class Parse():

    def __init__(self, data, xstack, pvg = None):

        self.fstack = stack.Stack()
        self.fsm = INIT; self.contflag = 0
        self.pvg = pvg
        self.pardict = {}

        # Create parse dictionary:
        for pt in parsetable:
            if pt[0] != None:
                if pt[0][1] not in self.pardict:
                    self.pardict[pt[0][1]] = dict()     # Add if new
                dd = self.pardict[pt[0][1]]
                if pt[2]:
                    #print ("pt2", pt[2])
                    dd[ pt[2]] = pt[:]
                else:
                    self.add_class(dd, pt)
            else:
                for aa in pt[1]:
                    if aa[1] not in self.pardict:
                        self.pardict[aa[1]] = dict()  # Add if new
                    dd  = self.pardict[aa[1]]
                    if pt[2]:
                        #print ("pt2", pt[2])
                        dd[ pt[2] ] = pt[:]
                    else:
                        self.add_class(dd, pt)

        '''for sss in self.pardict.iterkeys():
            print ("Key:", sss)
            for cc in self.pardict[sss].iterkeys():
                print ("   Subkey:", cc)
                print (self.pardict[sss][cc][2:])'''

        while True:
            tt = xstack.get2()  # Gen Next token
            if not tt:
                break
            self.parse_item2(data, tt)

    def add_class(self, dd, pt):
        for aa in pt[3]:
            dd[ aa ] = pt[:]

    # This is the new routine, dictionary driven
    # About ten times as fast

    def parse_item2(self, data, tt):

        if self.pvg.pgdebug > 1:
            print ("parse_item", data, tt[0], tt[1].start(), tt[1].end())

        mmm = tt[1];
        self.strx = data[mmm.start():mmm.end()]
        #print ("parser:", tt[0], "=", "'" + self.strx + "'"        )
        if self.pvg.show_state:
            print ("state:", self.fsm, "val:", "'" + self.strx + "' token:", tt[0], tt )
        try:
            curr = self.pardict[self.fsm[1]]
        except:
            print ("no state on", tt[0], self.strx        )
        try:
            item = curr[tt[0][0]]
        except:
            if self.pvg.show_parse:
                # show context
                bbb = mmm.start() - 5;  eee = mmm.end()+ 5
                cont = data[bbb:mmm.start()] + "'" +  self.strx + "'" + \
                        data[mmm.end():eee]

                print ("no key on", tt[0], cont)
            return

        #print ("item:", item)

        if item[4] != None:
            item[4](self, tt, item)

        if item[5] == REDUCE:
            # This is an actionless reduce ... rare
            self.reduce(tt)

        elif item[5] == IGNORE:
            pass
        else:
            #print (" Setting new state", pt[3], self.strx)
            self.fstack.push([self.fsm, self.contflag, tt, self.strx])
            self.fsm = item[5]
            self.contflag = item[6]

    def popstate(self):
        self.fsm, self.contflag, self.ttt, self.stry = self.fstack.pop()

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
# EOF








