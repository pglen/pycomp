#!/usr/bin/env python

import re, sys

from . import lexdef, stack

from complib.utils import *

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

        if self.pvg.opt_ldebug > 6:
            for aa in self.tokens:
                print("org token:", aa)

        self.lastbeg = 0;  self.lastpos = 0;
        self.state =  lexdef.INI_STATE
        self.statstack = stack.pStack()
        self.startstack = stack.pStack()
        self.linestart = 0
        self.linenum = 0
        self.lastline = 0
        self.start_tt = None
        self.backslash = 0
        self.accum = {}

    def _lexiter(self, pos, strx):

        '''  Call this for every token '''

        #print (strx[pos:])
        ret = None; mmm = None
        for ttt, vv in self.tokens:
            if ttt[0] != self.state:
                 continue
            #print("lex search:", "pos", pos, "ttt", ttt, "vvv", vv)
            mmm = vv.match(strx, pos)
            #print("mmm", mmm)
            if mmm:
                if self.pvg.opt_ldebug > 4:
                    print("match pos:", mmm.end(), mmm.start(),
                        "tok:", "'" + strx[mmm.start():mmm.end()] + "'", end = " ")
                mstr = mmm.string[mmm.start():mmm.end()]
                tt = lexdef.Lex(ttt, mstr, mmm.start(), mmm.end())
                tt.linenum = self.linenum
                tt.linestart = self.linestart
                ret = tt
                break
            else:
                if self.pvg.opt_ldebug > 8:
                    print("nomatch pos:", pos, "ttt:", ttt, "vv:", vv)
                pass
        return ret;

    def _push_state(self, tt, state):
        self.startstack.push(tt)
        self.statstack.push(self.state)
        self.state = state
        self.accum[self.state] = ""

    def _pop_state(self, tt, typex):

        ''' Done with a section, pop state '''

        if self.pvg.opt_ldebug > 2:
            print("Down from", typex, " state, accum:",
                        cesc(self.accum[self.state]), "tt =", tt)
        ttt = self.startstack.pop()
        tt.mstr = self.accum[self.state]
        tt.start = ttt.start
        # Update stamp to reflect collected data
        sss = list(tt.stamp)
        sss[1] = typex
        tt.stamp = tuple(sss)   # Back to tuple (for read only)
        self.state = self.statstack.pop()

    def feed(self, data):

        ''' Data comes in here, emit results at res '''

        res = []; pos = 0; lenx = len(data)
        while True:
            if pos >= lenx:
                break;
            #raise  ValueError
            tt = self._lexiter(pos, data)
            if not tt:
                break
            if not tt.end:
                pos += 1  # Step to next char in no match
                continue
            # Update pos, and skip to token end
            self.lastbeg = pos
            beg = pos; pos = tt.end
            self.lastpos = pos
            if self.pvg.opt_ldebug > 2:
                print("token at pos:", pos, tt, "state =", self.state)

            # Global actions
            if  tt.stamp[1] == "nl":
                self.linestart = pos
                self.linenum += 1
                if self.pvg.opt_ldebug > 2:
                    print("Newline at pos:", tt.start)
                self.lastline = tt.end
            #print("state =", tt, self.state)

            # Statful actions
            if self.state == lexdef.INI_STATE:
                # Change state if needed
                if tt.stamp[1] == "quote":
                    if self.pvg.opt_ldebug > 2:
                        print("Changed to str state with", tt)
                    self._push_state(tt, lexdef.STR_STATE)

                elif tt.stamp[1] == "squote":
                    if self.pvg.opt_ldebug > 2:
                        print("Changed to str2 state with", tt)
                    self._push_state(tt, lexdef.STR2_STATE)

                elif tt.stamp[1] == "comm3":
                    if self.pvg.opt_ldebug > 2:
                        print("Changed to comm3 state with", tt,
                                    "state =", lexdef.COMM_STATE)
                    self._push_state(tt, lexdef.COMM_STATE)
                else:
                    #print("no state")
                    res.append(tt)

            elif self.state == lexdef.UNI_STATE:
                try:
                    ccc = chr(int(tt.mstr, 16))
                except:
                    #print("back off", tt.mstr)
                    ccc = "\\u" + tt.mstr

                if self.pvg.opt_ldebug > 2:
                    print("uni_state:", tt.mstr)
                self.accum[self.state] = ccc

                # Copy up:
                self.accum[self.statstack.pop2()] += self.accum[self.state]
                self._pop_state(tt, "uni")
                self.accum[self.statstack.pop2()] += self.accum[self.state]
                self._pop_state(tt, "esc")

            elif self.state == lexdef.HEX_STATE:
                try:
                    ccc = chr(int(tt.mstr, 16))
                except:
                    #print("back off", tt.mstr)
                    ccc = "\\x" + tt.mstr

                if self.pvg.opt_ldebug > 1:
                    print("hex_state:", tt.mstr)
                self.accum[self.state] = ccc

                # Copy up:
                self.accum[self.statstack.pop2()] += self.accum[self.state]
                self._pop_state(tt, "hex")
                self.accum[self.statstack.pop2()] += self.accum[self.state]
                self._pop_state(tt, "esc")
                continue

            # Handle escapes:
            elif self.state == lexdef.ESC_STATE:
                wasesc = True
                if   tt.mstr == "r":  self.accum[self.state] += "\r"
                elif tt.mstr == "n":  self.accum[self.state] += "\n"
                elif tt.mstr == "a":  self.accum[self.state] += "\a"
                elif tt.mstr == "t":  self.accum[self.state] += "\t"
                elif tt.mstr == "b":  self.accum[self.state] += "\b"
                elif tt.mstr == "v":  self.accum[self.state] += "\v"
                elif tt.mstr == "f":  self.accum[self.state] += "\f"
                elif tt.mstr == "e":  self.accum[self.state] += "\e"
                elif tt.mstr == "\?": self.accum[self.state] += "\?"
                elif tt.mstr == "\"": self.accum[self.state] += "\\"
                elif tt.mstr == "\'": self.accum[self.state] += "\'"
                elif tt.mstr == "\\": self.accum[self.state] += "\""
                elif tt.mstr == "x":
                    self._push_state(tt, lexdef.HEX_STATE)
                    if self.pvg.opt_ldebug > 2:
                        print("Changed to HEX state with:", tt.stamp[1], tt.mstr)
                    wasesc = False
                elif tt.mstr == "u":
                    self._push_state(tt, lexdef.UNI_STATE)
                    if self.pvg.opt_ldebug > 2:
                        print("Changed to UNI state with:", tt.stamp[1], tt.mstr)
                    wasesc = False
                if wasesc:
                    # Unrecognized, or non continuation escape, exit state
                    self.accum[self.statstack.pop2()] += self.accum[self.state]
                    self._pop_state(tt, "esc")
                    continue

            elif tt.stamp[1] == "sbsla":
                #self.accum[self.state] += "";
                self._push_state(tt, lexdef.ESC_STATE)
                if self.pvg.opt_ldebug > 2:
                    print("Changed to ESC state with:", tt.stamp[1])
                self.backslash = 0
                #res.append(tt)    # Emit

            # Handle back offs
            elif tt.stamp[1] == "dquote": # and self.state == lexdef.STR_STATE:
                self.accum[self.state] += '"';
                self._pop_state(tt, "strx")
                res.append(tt)    # Emit

            elif tt.stamp[1] == "dquote2": # self.state == lexdef.STR2_STATE:
                self.accum[self.state] += "'";
                self._pop_state(tt, "strx")
                res.append(tt)    # Emit

            elif tt.stamp[1] == "ecomm3": # self.state == lexdef.COMM_STATE:
                self.accum[self.state] += "*/";
                if self.pvg.opt_ldebug > 0:
                    print("Change comm state down:",
                                self.accum[self.state], tt, lexdef.COMM_STATE)
                self._pop_state(tt, "comm3")
                res.append(tt)    # Emit
            else:
                pass

            # Default to fill accumulators:
            if  self.state == lexdef.STR_STATE:
                self.accum[self.state] += tt.mstr

            if  self.state == lexdef.STR2_STATE:
                self.accum[self.state] += tt.mstr

            if  self.state == lexdef.COMM_STATE:
                self.accum[self.state] += tt.mstr

            #print(self.state, tt.stamp, lexdef.rtok[tt.stamp], "\t", tt[2])

        return res

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    #print("tok", tokens)

def test_letters():

    org = "abcdef"
    res2 = "[[ 'ident' = 'abcdef' 0 ]]"
    lx = Lexer(lexdef.xtokens, lpg)
    res = []
    lx.feed(org, res)
    #print(str(res))
    #assert 0
    del lx
    assert str(res) == res2

def test_keywords():

    org = "func loop enter leave return "
    res2 =  "[[ 'func' = 'func ' 0 ], [ 'loop' = 'loop ' 0 ], " \
            "[ 'enter' = 'enter ' 0 ], [ 'leave' = 'leave ' 0 ], " \
            "[ 'return' = 'return ' 0 ]]"
    lx = Lexer(lexdef.xtokens, lpg)
    res = []
    lx.feed(org, res)
    del lx
    #print(str(res))
    #assert 0
    assert str(res) == res2

def test_operators():
    org = "== != !== += >= <= -> <- && || ^^"
    res2 = "[[ 'deq' = '==' 0 ], [ 'sp' = ' ' 0 ], [ 'ndeq' = '!=' 0 ], " \
    "[ 'sp' = ' ' 0 ], [ 'ndeq' = '!=' 0 ], [ '=' = '=' 0 ], [ 'sp' = ' ' 0 ], "\
    "[ 'peq' = '+=' 0 ], [ 'sp' = ' ' 0 ], [ '>' = '>' 0 ], [ '=' = '=' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ 'gett' = '<=' 0 ], [ 'sp' = ' ' 0 ], [ 'dref' = '->' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ 'aref' = '<-' 0 ], [ 'sp' = ' ' 0 ], [ 'and' = '&&' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ 'or' = '||' 0 ], [ 'sp' = ' ' 0 ], [ 'xor' = '^^' 0 ]]"
    lx = Lexer(lexdef.xtokens, lpg)
    res = []
    lx.feed(org, res)
    del lx
    #print(str(res))
    #assert 0
    assert str(res) == res2

def test_oper():

    org = " ! ~ _ ( ) = / : . << >> ++ -- ^ % "

    res2 = \
    "[[ 'sp' = ' ' 0 ], [ 'excl' = '!' 0 ], [ 'sp' = ' ' 0 ], "\
    "[ 'tilde' = '~' 0 ], [ 'sp' = ' ' 0 ], [ 'ident' = '_' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ '(' = '(' 0 ], [ 'sp' = ' ' 0 ], [ ')' = ')' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ '=' = '=' 0 ], [ 'sp' = ' ' 0 ], [ '/' = '/' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ 'colon' = ':' 0 ], [ 'sp' = ' ' 0 ], [ 'dot' = '.' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ '<' = '<' 0 ], [ '<' = '<' 0 ], [ 'sp' = ' ' 0 ], "\
    "[ '>' = '>' 0 ], [ '>' = '>' 0 ], [ 'sp' = ' ' 0 ], [ '+' = '+' 0 ], "\
    "[ '+' = '+' 0 ], [ 'sp' = ' ' 0 ], [ '-' = '-' 0 ], [ '-' = '-' 0 ], "\
    "[ 'sp' = ' ' 0 ], [ 'caret' = '^' 0 ], [ 'sp' = ' ' 0 ], [ 'cent' = '%' 0 ], "\
    "[ 'sp' = ' ' 0 ]]"

    lx = Lexer(lexdef.xtokens, lpg)
    res = []
    lx.feed(org, res)
    del lx
    #print(str(res))
    #assert 0
    assert str(res) == res2

# EOF
