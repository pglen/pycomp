#!/usr/bin/env python

import re, sys

from . import lexdef, stack

from complib.utils import *
from complib import lexfunc as lexfunc

class LexI():

    ''' Store one lexed item (used to be a list, but got out of hand)
    '''

    def __init__(self, stampx = [], mstr = "", startx = 0, endx = 0):
        self.state = lexdef.INI_STATE
        self.stamp = stampx     # Originating token
        self.mstr = mstr        # Main payload
        # Init some future vars (just to show what comes)
        self.flag = 0           # State information 0=>available
        self.start = startx     # Positions
        self.end = endx
        self.linenum = 0
        self.linestart = 0
        self.lineoffs = 0
        self.pos = 0
        self.val = 0.0          # if number  (pre calculated)
        self.ival = 0           # if integer (pre calculated)
        self.wantstate = None
        self.typez  = "NoType"

        # Decode and mold
        if self.stamp.xstr == "num":
            self.ival = int(self.mstr)

        if self.stamp.xstr == "hex":
            self.stamp.xstr = "num"
            self.ival = int(self.mstr[2:], 16)

        if self.stamp.xstr == "oct":
            self.stamp.xstr = "num"
            self.ival = int(self.mstr[2:], 8)

        if self.stamp.xstr == "bin":
            self.stamp.xstr = "num"
            self.ival = int(self.mstr[2:], 2)

        #print("inited", str(self))

    def copy(self, other):
        other.state = self.state
        other.stamp = self.stamp
        other.mstr = self.mstr
        other.start = self.start
        other.end = self.end
        other.flag = self.flag
        other.val = self.val
        other.ival = self.ival
        other.wantstate = self.wantstate

    def __str__(self):
        '''   Deliver it in an easy to see format  '''
        strx = "[ " + pp(self.stamp.xstr) + " -> " + pp(self.mstr) + \
                        " ival = " + pp(str(self.ival)) + \
                        " flag = " + pp(str(self.flag)) + \
                        " typez = " + pp(self.typez) + \
                        " ]"
                        #" want = "  + lexdef.state2str(self.wantstate) + \
        return strx

    def dump(self):
        ''' deliver a more detailed set of fields '''
        strx = " [ Lex: " + padx("'" + str(self.stamp) + "' => '" + \
                        cesc(self.mstr) + "'", 20) + \
                        " flag = " + padx("%d" % (self.flag)) + \
                        " st/en = " + padx("%d:%d" % (self.start, self.end), 8) +  \
                        " val = "  + ("%d" % (self.val)) + \
                        " ival = " + ("%d" % (self.ival)) + \
                        " line = " + ("%d" % (self.linenum+1)) + \
                        " offs = " + ("%d" % (self.lineoffs+1)) + \
                        " lsta = " + ("%d" % (self.linestart)) + \
                        " typez = " + ("%s" % (self.typez)) + \
                        " want = "  + state2str(self.wantstate) + \
                        " ] "
        return strx

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

        if self.pvg.opt_lexdebug > 6:
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
        # Initial accum
        self.accum = {}
        self.accum[self.state] = ""
        self.linearr = []

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
                if self.pvg.opt_lexdebug > 4:
                    print("match pos:", mmm.end(), mmm.start(),
                        "tok:", "'" + strx[mmm.start():mmm.end()] + "'", end = " ")
                mstr = mmm.string[mmm.start():mmm.end()]
                #print("ttt", ttt)
                dd = lexdef.StI(ttt)
                tt = LexI(dd, mstr, mmm.start(), mmm.end())
                tt.linenum = self.linenum
                tt.linestart = self.linestart
                tt.lineoffs  = tt.start - self.linestart
                tt.wantstate = ttt[3]
                tt.callit = ttt[4]
                ret = tt
                break
            else:
                if self.pvg.opt_lexdebug > 8:
                    print("nomatch pos:", pos, "ttt:", ttt, "vv:", vv)
                pass
        return ret;

    def _push_state(self, tt, state):

        ''' Start new state  '''

        if self.pvg.opt_lexdebug > 0:
            print("  To:", lexdef.state2str(state), tt)
        self.startstack.push(tt)
        self.statstack.push(self.state)
        # Clean accum as we are going up
        #self.accum[self.state] = ""
        self.state = state
        self.accum[self.state] = ""

    def _pop_state(self, tt, typex = "None"):

        ''' Done with a state, pop state '''

        if self.pvg.opt_lexdebug > 2:
            print("  Dn:", lexdef.state2str(self.state),
                        " acc:", pp(self.accum[self.state]), "tt =", tt)
        ttt = self.startstack.pop()
        tt.start = ttt.start
        tmp = self.accum[self.state] # + tt.mstr
        self.state = self.statstack.pop()
        # Migrate collected data down
        self.accum[self.state] += tmp
        self.mstr = self.accum[self.state]
        if self.pvg.opt_lexdebug > 2:
            print("  Dn2:", lexdef.state2str(self.state),
                        " acc:", pp(self.accum[self.state]), "tt =", tt)

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
            if self.pvg.opt_lexdebug > 3:
                print("Token at:", pos, tt, "state =", lexdef.state2str(self.state))

            # Change state if needed, except on pop state
            if tt.wantstate and tt.wantstate != lexdef.POP_STATE:
                if self.pvg.opt_lexdebug > 3:
                    print("Push state:", lexdef.state2str(tt.wantstate))
                self._push_state(tt, tt.wantstate)

            # If function is specified, execute
            if tt.callit:
                tt.callit(self, tt)

            # Global actions
            if  tt.stamp.xstr == "decl":
                # Lower case declaration
                tt.mstr = tt.mstr.lower()

            if  tt.stamp.xstr == "nl":
                # Count lines
                self.linearr.append(pos)
                self.linestart = pos
                self.linenum += 1
                if self.pvg.opt_lexdebug > 6:
                    print("Newline at pos:", tt.start)
                self.lastline = tt.end

            if tt.stamp.xstr == "comm2" or \
                    tt.stamp.xstr == "comm4":
                self.linestart = pos
                self.linenum += 1

            if self.pvg.opt_lexdebug > 5:
                print("state:", lexdef.state2str(self.state), tt)

            # Stateful actions
            if self.state == lexdef.UNI_STATE:
                try:
                    ccc = chr(int(tt.mstr, 16))
                except:
                    #print("back off", tt.mstr)
                    ccc = "\\u" + tt.mstr

                if self.pvg.opt_lexdebug > 2:
                    print("uni_state:", tt.mstr)
                self.accum[self.state] = ccc
                # Copy up:
                #self.accum[self.statstack.pop2()] += self.accum[self.state]
                self._pop_state(tt, "uni")
                #self.accum[self.statstack.pop2()] += self.accum[self.state]
                self._pop_state(tt, "esc")
            elif self.state == lexdef.HEX_STATE:
                if self.pvg.opt_lexdebug > 2:
                    print("hex state", tt)
                try:
                    ccc = chr(int(tt.mstr, 16))
                except:
                    #print("back off", tt.mstr)
                    ccc = "\\x" + tt.mstr
                if self.pvg.opt_lexdebug > 1:
                    print("hex_state:", tt.mstr)
                self.accum[self.state] = ccc
                # Copy up:
                self._pop_state(tt, "hex")
                self._pop_state(tt, "esc")
                continue

            # Handle escapes:
            elif self.state == lexdef.ESC_STATE:
                if self.pvg.opt_lexdebug > 4:
                    print("in ESC state", tt)
                wasesc = True
                if tt.stamp.xstr == 'anyx':
                    if   tt.mstr == "r":  self.accum[self.state] += "\\r"
                    elif tt.mstr == "n":  self.accum[self.state] += "\\n"
                    elif tt.mstr == "a":  self.accum[self.state] += "\\a"
                    elif tt.mstr == "t":  self.accum[self.state] += "\\t"
                    elif tt.mstr == "b":  self.accum[self.state] += "\\b"
                    elif tt.mstr == "v":  self.accum[self.state] += "\\v"
                    elif tt.mstr == "f":  self.accum[self.state] += "\\f"
                    elif tt.mstr == "e":  self.accum[self.state] += "\\e"
                    elif tt.mstr == "\?": self.accum[self.state] += "\\?"
                    elif tt.mstr == "\"": self.accum[self.state] += "\\\""
                    elif tt.mstr == "\'": self.accum[self.state] += "\\\'"
                    elif tt.mstr == "\\": self.accum[self.state] += "\\\\"
                    elif tt.mstr == "x":
                        self._push_state(tt, lexdef.HEX_STATE)
                        if self.pvg.opt_lexdebug > 2:
                            print("  Changed to HEX state with:", tt) #.stamp.xstr, tt.mstr)
                        wasesc = False
                    elif tt.mstr == "u":
                        self._push_state(tt, lexdef.UNI_STATE)
                        if self.pvg.opt_lexdebug > 2:
                            print("  Changed to UNI state with:", tt) #tt.stamp.xstr, tt.mstr)
                        wasesc = False
                    else:
                        self.accum[self.state] += tt.mstr
                    if wasesc:
                        # Unrecognized, or non continuation escape, exit state
                        #self.accum[self.statstack.pop2()] += self.accum[self.state]
                        self._pop_state(tt, "esc")
                        continue

            # Handle back offs
            if tt.wantstate == lexdef.POP_STATE:
                #print("Pop state: ", lexdef.state2str(self.state))
                self._pop_state(tt, "strx")
                tt.mstr = self.accum[self.state]
                self.accum[self.state] = ""

                if tt.stamp.xstr == "dquote":
                    tt.mstr += '"';
                    tt.stamp.xstr = "str"
                elif tt.stamp.xstr == "dquote2":
                    tt.mstr += "'";
                    tt.stamp.xstr = "str"
                elif tt.stamp.xstr == "ecomm3":
                    tt.mstr += "*/";
                    tt.stamp.xstr = "comm3"
                elif tt.stamp.xstr == "ecomm3d":
                    tt.mstr += "*/";
                    tt.stamp.xstr = "comm3d"
                else:
                    pass
                #continue

            # Default to fill accumulators:
            if  self.state == lexdef.STR_STATE:
                self.accum[self.state] += tt.mstr

            if  self.state == lexdef.STR2_STATE:
                self.accum[self.state] += tt.mstr

            if  self.state == lexdef.COMM_STATE:
                self.accum[self.state] += tt.mstr

            if  self.state == lexdef.COMM_STATED:
                self.accum[self.state] += tt.mstr

            if self.state == lexdef.INI_STATE:
                res.append(tt)

            #print("fin", self.state, "tt", tt, "acc", self.accum[self.state])

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
