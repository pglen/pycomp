#!/usr/bin/env python

import sys, os, re, time, stat
import threading
import curses

pvg = None
curses_flag = False

def upvg(xpvg):
    global pvg
    pvg = xpvg

def start_curses(stdscr):
    curses.initscr()

_gl_cnt = 0
sema = threading.Semaphore()
def unique():             # create a unique temporary number
    global _gl_cnt;
    sema.acquire()
    _gl_cnt += 1
    sema.release()
    return _gl_cnt

def xprintf(*args, end = " "):
    strx = ""
    for aa in args:
        aa = str(aa)
        if strx:  aa = "\t" + aa
        strx +=  aa
    #strx += end
    print(strx, end = "")
    #return strx

def time_ms(start_time):
    ttt = time.process_time() - start_time
    return "%.2f ms" % (ttt * 1000)

def prarr(xarr, pre = "", all = False):

    ''' Pretty Print array '''

    if pre:
        print(pre, end = " ")
    for aa in xarr:
        if all or not aa.flag:
            print( " [" + pp(aa.stamp) + " " + pp(aa.mstr), aa.flag, end = "]")
    print()

def shorten(strx, xlen = 5):
    if len(strx) < xlen:
        return strx
    else:
        return strx[:xlen] + ".."

def pp(strx, shortenx = False, xlen = 5):
    if shortenx:
        strx = shorten(strx, xlen)
    str2 = cesc_lite(strx)
    return "'" + str(str2) + "'"

def prclass(lpgx):
    for aa in dir(lpgx):
        if aa[:2] != "__":
            print("[", aa, "=", getattr(lpgx, aa), end = " ] ")
    print

# ------------------------------------------------------------------------
# Convert octal string to integer

def oct2int(strx):
    retx = 0
    for aa in strx:
        num = ord(aa) - ord("0")
        if num > 7 or num < 0:
            break
        retx <<= 3; retx += num
    #print ("oct:", strx, "int:", retx)
    return retx

# ------------------------------------------------------------------------
# Convert unicode sequence to unicode char

def uni(xtab):

    #print (str.format("{0:b}",  xtab[0]))

    cc = 0
    try:
        if xtab[0] & 0xe0 == 0xc0:  # two numbers
            cc = (xtab[0] & 0x1f) << 6
            cc += (xtab[1] & 0x3f)
        elif xtab[0] & 0xf0 == 0xe0: # three numbers
            cc = (xtab[0] & 0x0f) << 12
            cc += (xtab[1] & 0x3f) << 6
            cc += (xtab[2] & 0x3f)
        elif xtab[0] & 0xf8 == 0xf0: # four numbers
            cc = (xtab[0] & 0x0e)  << 18
            cc += (xtab[1] & 0x3f) << 12
            cc += (xtab[2] & 0x3f) << 6
            cc += (xtab[3] & 0x3f)
        elif xtab[0] & 0xfc == 0xf8: # five numbers
            cc = (xtab[0] & 0x03)  << 24
            cc += (xtab[1] & 0x3f) << 18
            cc += (xtab[2] & 0x3f) << 12
            cc += (xtab[3] & 0x3f) << 6
            cc += (xtab[4] & 0x3f)
        elif xtab[0] & 0xfe == 0xf8: # six numbers
            cc = (xtab[0] & 0x01)  << 30
            cc += (xtab[1] & 0x3f) << 24
            cc += (xtab[2] & 0x3f) << 18
            cc += (xtab[3] & 0x3f) << 12
            cc += (xtab[4] & 0x3f) << 6
            cc += (xtab[5] & 0x3f)

        ccc = unichr(cc)
    except:
        pass

    return ccc

def rcesc(strx):

    ''' Reverse 'C' escape sequences \\n '''

    retx = ""; pos = 0; lenx = len(strx)
    while True:
        if pos >= lenx:
            break
        chh = strx[pos]
        if(chh == '\\'):
            if pos >= lenx:
                retx += chh
                break
            chh2 = strx[pos+1]
            if chh2 == "n":
                retx += '\n'
                pos += 1
            elif chh2 == "r":
                retx += '\r'
                pos += 1
            elif chh2 == "a":
                retx += '\a'
                pos += 1
            elif chh2 == "t":
                retx += '\t'
                pos += 1
            else:
                retx += chh + chh2;
        else:
            retx += chh
        pos += 1
    return retx

def asmesc(strx):

    ''' escape to 'ASM' escape sequences '''

    lenx = len(strx); sep = strx[0]
    retx = ""; pos = 0;  cumm = "";

    def subst(retxx, cummm, sepp, chh):
        ''' internal function for esc sequences '''
        if cummm:
            retxx += sepp + cummm + sepp + ", "; cummm = ""
        retxx += str(ord(chh))  + ", "
        return retxx, cummm

    while True:
        if pos >= lenx:
            break
        chh = strx[pos]
        if(chh == '\\'):
            pos += 1                # leap of faith
            if pos >= lenx:         # end ?
                retx += chh
                break
            chh2 = strx[pos]
            if chh2 == "t":
                retx, cumm  = subst(retx, cumm, sep, "\t")
            elif chh2 == "n":
                retx, cumm  = subst(retx, cumm, sep, "\n")
            elif chh2 == "r":
                retx, cumm  = subst(retx, cumm, sep, "\r")
            elif chh2 == "a":
                retx, cumm  = subst(retx, cumm, sep, "\a")
            elif chh2 == "b":
                retx, cumm  = subst(retx, cumm, sep, "\b")
            elif chh2 == '"':
                retx, cumm  = subst(retx, cumm, sep, "\"")
            #elif chh2 == '\\':
            #    retx, cumm  = subst(retx, cumm, sep, "\\")
            else:
                # back off, put chars out
                pos -= 1
                if chh2 == "\\":
                    cumm += chh
                else:
                    cumm += chh + chh2;
        else:
            if chh != sep:
                cumm += chh
        pos += 1
    # Output last
    if cumm:
        retx += sep + cumm + sep + ", "
    retx += "0"
    if pvg and pvg.opt_debug > 7:
        print("asmesc:", strx, "->", retx)
    if pvg and pvg.opt_debug > 8:
        for aa in retx:
            print(retx)

    return retx

def cesc_lite(strx):

    ''' A simpler version for printing to terminal '''

    retx = u""; pos = 0;

    try:
        lenx = len(strx)
    except:
        # Class does not have length
        strx = str(strx)
        lenx = len(strx)

    while True:
        if pos >= lenx:
            break
        chh = strx[pos]
        if(chh == '\n'):
            retx += '\\n'
        elif(chh == '\r'):
            retx += '\\r'
        elif(chh == '\b'):
            retx += '\\b'
        elif(chh == '\a'):
            retx += '\\a'
        elif(chh == '\t'):
            retx += '\\t'
        else:
            retx += chh
        pos += 1

    if pvg and pvg.opt_debug > 8:
        print("cesc:", strx, "=>", retx)

    return retx

def cesc(strx):

    r''' Expand 'C' sequences like: \n \\n
        Thu 21.Aug.2025 added c l a s s is now stringized before processing

    From doc:
        \" \'
    	\r \n \a \t \b \v \f \ e
    	\? \\
    '''

    retx = u""; pos = 0;

    try:
        lenx = len(strx)
    except:
        # Class does not have length
        strx = str(strx)
        lenx = len(strx)

    while True:
        if pos >= lenx:
            break
        chh = strx[pos]
        if(chh == '\n'):
            retx += '\\n'
        elif(chh == '\r'):
            retx += '\\r'
        elif(chh == '\b'):
            retx += '\\b'
        elif(chh == '\a'):
            retx += '\\a'
        elif(chh == '\t'):
            retx += '\\t'
        elif(chh == '\f'):
            retx += '\\f'
        elif(chh == '\v'):
            retx += '\\v'
        elif(chh == '\''):
            retx += '\\\''
        elif(chh == '\"'):
            retx += '\\"'
        #elif(chh == '\e'):
        #    retx += '\\e'
        elif(chh == '\\'):
            retx += '\\'
        else:
            retx += chh
        pos += 1

    if pvg and pvg.opt_debug > 8:
        print("cesc:", strx, "=>", retx)

    return retx

# ------------------------------------------------------------------------
# Unescape unicode into displayable sequence

def unescape(strx):

    xtab = []; xtablen = 0
    #print (" x[" + strx + "]x ")

    #global xtab, xtablen
    retx = u""; pos = 0; lenx = len(strx)

    while True:
        if pos >= lenx:
            break

        chh = strx[pos]

        if(chh == '\\'):
            #print ("backslash", strx[pos:])

            pos2 = pos + 1; strx2 = ""
            while True:
                if pos2 >= lenx:
                    # See if we accumulated anything
                    if strx2 != "":
                        xtab.append(oct2int(strx2))
                    if len(xtab) > 0:
                        #print ("final:", xtab)
                        if xtablen == len(xtab):
                            retx += uni(xtab)
                            xtab = []; xtablen = 0
                    pos2 += 1
                    break
                chh2 = strx[pos2]
                if chh2  >= "0" and chh2 <= "7":
                    strx2 += chh2
                else:
                    #print ("strx2: '"  + strx2 + "'")
                    if strx2 != "":
                        octx = oct2int(strx2)
                        if xtablen == 0:
                            if octx & 0xe0 == 0xc0:
                                #print ("two ",str.format("{0:b}", octx))
                                xtablen = 2
                                xtab.append(octx)
                            elif octx & 0xf0 == 0xe0: # three numbers
                                #print ("three ",str.format("{0:b}", octx))
                                xtablen = 3
                                xtab.append(octx)
                            elif octx & 0xf8 == 0xf0: # four numbers
                                print ("four ",str.format("{0:b}", octx))
                                xtablen = 4
                                xtab.append(octx)
                            elif octx & 0xfc == 0xf8: # five numbers
                                print ("five ",str.format("{0:b}", octx))
                                xtablen = 5
                                xtab.append(octx)
                            elif octx & 0xfe == 0xfc: # six numbers
                                print ("six ",str.format("{0:b}", octx))
                                xtablen = 6
                                xtab.append(octx)
                            else:
                                #print ("other ",str.format("{0:b}", octx))
                                retx += unichr(octx)
                        else:
                            xtab.append(octx)
                            #print ("data ",str.format("{0:b}", octx))
                            if xtablen == len(xtab):
                                retx += uni(xtab)
                                xtab = []; xtablen = 0

                    pos = pos2 - 1
                    break
                pos2 += 1
        else:
            if xtablen == len(xtab) and xtablen != 0:
                retx += uni(xtab)
            xtab=[]; xtablen = 0

            try:
                retx += chh
            except:
                pass
        pos += 1

    #print ("y[" + retx + "]y")
    return retx

# ------------------------------------------------------------------------
# Give the user the usual options for true / false - 1 / 0 - y / n ...

def isTrue(strx, defx = False):
    sss = strx.strip()
    if sss == "1": return True
    if sss == "0": return False
    uuu = sss.upper()
    if uuu == "OK": return True
    if uuu == "TRUE": return True
    if uuu == "FALSE": return False
    if uuu == "YES": return True
    if uuu == "NO": return False
    if uuu == "Y": return True
    if uuu == "N": return False
    return defx

def isfile(fname):
    ''' # Return True if file exists '''
    try:
        ss = os.stat(fname)
    except:
        return False
    if stat.S_ISREG(ss[stat.ST_MODE]):
        return True
    return False

def stringify(lll):
    ttt = ""
    for aa in lll:
        if ttt: aa = " " + aa
        ttt += aa
    return ttt

def hd(varx):
    ''' Hex dump it '''
    strx = ""
    for aa in range(len(varx)):
        strx += "%02x " % (int(aa) & 0xff);
    strx += "\n"
    return strx

def padx(strx, lenx = 4):
    lenz = len(strx)
    if  lenz < lenx:
        strx = strx + " " * (lenx - lenz)
    #print("[[" + strx + "]]")
    return strx;

def count_newlines(xstr):
    cnt = 0
    for aa in xstr:
        if aa == "\n":
            cnt += 1
    return cnt

def error(self2, errstr, newpos = -1, addstr = ""):

    ''' Print compiler error, add more info if  requested '''

    if newpos >= 0:
        print("newpos", newpos)
    eol = 0
    posx = self2.arrx[self2.startx]
    # From current pos till end of this line
    for aa in range(posx.linestart, len(self2.buf)):
        if self2.buf[aa] == "\n":
            eol = aa
            #print("Found pos", posx.linestart, eol)
            break
    print("\n" + self2.buf[posx.linestart:eol], file=sys.stderr, )
    print("-" *  (posx.end - posx.linestart - 2), file=sys.stderr, end = "" )
    print("^", file=sys.stderr, end = "")
    print("-" *  (eol - posx.end), file=sys.stderr,  )
    print(pvg.nowfile + ":", errstr, red("error"), "at line:", posx.linenum + 1,
          "near col:", posx.start - posx.linestart, file=sys.stderr, end = " " )
    print(addstr, file=sys.stderr)
    subexit(self2, 1)

def subexit(self2, errx):
    if pvg.opt_ymtab:
        import complib.linpool as linpool
        print("Symtab:")
        linpool.showpool(self2)

    if(not pvg.opt_ignore):
        sys.exit(1)

# 30: Black     31: Red     32: Green   33: Yellow
# 34: Blue      35: Magenta 36: Cyan    37: White

def red(strx):
    return color(strx, "31")

def blue(strx):
    return color(strx, "34")

def green(strx):
    return color(strx, "32")

def color(strx, col = "31"):

    if not os.isatty(1):
        return strx

    if not os.isatty(2):
        return strx

    if not pvg.opt_nocolor:
        global curses_flag
        if not curses_flag:
            curses_flag = True
            curses.wrapper(start_curses)

    if pvg.opt_nocolor:
        return strx
    if not curses.has_colors():
        return strx
    return "\033[" + str(col) + ";1m" + strx + "\033[0m"

def dumpstack(self2, stackx, eolx = "", label = "", active=False):
    print(stackx.name + ":", label, end = eolx)
    for aa in stackx:
        if active and self2.arrx[aa].flag != 0:
            continue
        print("  " + str(self2.arrx[aa]), end=eolx)
    if eolx == "": print()

class   Xenum():

    ''' Simple autofill enum to use in parser '''

    def __init__(self, *val):
        self.arr = [] ; self.narr = {}
        self.add(*val)

    def add(self, *val):
        for aa in val:
            self.narr[aa] = len(self.arr)
            self.arr.append(aa)

    def dump(self):
        strx = ""
        for cnt, aa in enumerate(self.arr):
            #print(cnt, aa)
            strx += str(cnt) + " = " + str(aa) + "\n"
        return strx

    def get(self, cnt):
        try:
            return self.arr[cnt]
        except:
            return("Invalid")

    def val(self, name):
        try:
            ret = self.narr[name]
        except:
            if 0: #pvg.opt_verbose:
                print("Warn: adding:", name)
            self.add(name)
            ret = self.narr[name]
        return ret

def test_xenum():

    ''' Test Xenum class '''
    eee = Xenum("no", "yes",)
    eee.add( "maybe")
    assert eee.get(0) == "no"
    assert eee.get(1) == "yes"
    assert eee.val("no")  == 0
    assert eee.val("yes") == 1
    # Autogen
    assert eee.val("none") == 3

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    org = "12345678\r\n\a\tabcdef"
    print(org)
    sss = cesc(org)
    print(sss)
    uuu = rcesc(sss)
    print(uuu)

def test_cesc():
    org = "12345678\r\n\a\tabcdef"
    sss = cesc(org)
    ttt = rcesc(sss)
    assert ttt == org

def test_hd():
    org = "12345678\r\n\a\tabcdef"
    sss = hd(org)
    #print(sss)
    assert sss == "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 \n"

def test_true():

    assert True == isTrue("Yes")
    assert True == isTrue(" Yes ")
    assert True == isTrue("YES")
    assert True == isTrue("OK")
    assert True == isTrue("True")
    assert True == isTrue(" True ")
    assert True == isTrue("Y")
    assert True == isTrue(" Y ")
    assert True == isTrue("1")
    assert True == isTrue(" 1 ")

    assert False == isTrue("xrue")
    assert False == isTrue("False")
    assert False == isTrue(" NO ")
    assert False == isTrue("0")
    assert False == isTrue("")

def test_oct2():

    sss = oct2int("111")
    assert sss == 73
    ttt = oct2int("123456")
    assert ttt == 42798
    uuu = oct2int("888")
    assert uuu == 0

def test_unescape():

    ret = unescape("a\"\'\r\nb")
    assert ret ==  "a\"\'\r\nb"

    ret = unescape("\x41\x42")
    assert ret == "AB"

    ret = unescape("\061\062")
    assert ret == "12"

    #print("\x263A")
    #print("\x1f60a")
    #ret = unescape("\x263A")
    #print(ret)
    #ret = unescape("\x1f60a")
    #print(ret)
    #assert ret == "a\\b"
    #ret = unescape("\0")
    #assert ret == ""

# EOF
