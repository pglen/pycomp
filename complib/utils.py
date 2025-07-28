#!/usr/bin/env python

import sys, os, re, time, stat

class lpg():

    ''' Some class globals. Read: (Lexer and Parser Globals) '''

    buf = None; xstack = None; verbose = 0
    lxdebug = 0; pgdebug = 0; show_lexer = False;
    lstack = None;  fullpath = None; docroot = None
    got_clock = 0; show_timing = False; second = ""
    flag = False; show_parse = False
    emit = False; show_state = False; lex_only = False
    currline = 0;

    def print():
        for aa in dir(lpg):
            if aa[:2] != "__":
                print("[", aa, "=", getattr(lpg, aa), end = " ] ")
        print()

# ------------------------------------------------------------------------
# Pretty Print

def prarr(xarr, pre = "", all = False):
    if pre:
        print(pre, end = "")

    for aa in xarr:
        if all or not aa.flag:
            print( " [" + pp(aa.stamp[1]) + " " + pp(aa.mstr), aa.flag, end = "]")
    print()

def pp(strx):
    str2 = cesc(strx)
    return "'" + str(str2) + "'"

def xint(strx, defx = 0):

    ''' Convert to integer without fault.
            Return defx if it is an invalid integer. '''

    ret = defx
    try:
        ret = int(strx)
    except ValueError:      pass
    except: print(sys.exc_info())
    return ret

def prclass(lpgx):
    for aa in dir(lpgx):
        if aa[:2] != "__":
            print("[", aa, "=", getattr(lpgx, aa), end = " ] ")
    print

# ------------------------------------------------------------------------
# Give a new integer value with every iteration

_gl_pcnt = 0
def punique():                       # create a unique temporary number
    global _gl_pcnt;
    _gl_pcnt += 10
    return _gl_pcnt

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

    ''' reverse 'C' escape sequences \\n '''

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

    #print("revesc", strx)
    #for aa in retx:
    #    print(ord(retx))

    return retx

def cesc(strx):

    ''' convert like 'C' like: \n \\n '''

    #print (" x[" + strx + "]x ")

    retx = u""; pos = 0; lenx = len(strx)

    while True:
        if pos >= lenx:
            break
        chh = strx[pos]
        if(chh == '\n'):
            retx += '\\n'
        elif(chh == '\r'):
            retx += '\\r'
        elif(chh == '\a'):
            retx += '\\a'
        elif(chh == '\t'):
            retx += '\\t'
        elif(chh == '\f'):
            retx += '\\f'
        elif(chh == '\v'):
            retx += '\\v'
        elif(chh == '\e'):
            retx += '\\e'
        elif(chh == '\\'):
            retx += '\\\\'
        else:
            retx += chh
        pos += 1
    return retx

# ------------------------------------------------------------------------
# Unescape unicode into displayable sequence

xtab = []; xtablen = 0

def unescape(strx):

    #print (" x[" + strx + "]x ")

    global xtab, xtablen
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
                    pos = pos2 - 1
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
# Give the user the usual options for true / false - 1 / 0 - y / n

def isTrue(strx, defx = False):
    if strx == "1": return True
    if strx == "0": return False
    uuu = strx.upper()
    if uuu == "OK": return True
    if uuu == "TRUE": return True
    if uuu == "FALSE": return False
    if uuu == "YES": return True
    if uuu == "NO": return False
    if uuu == "Y": return True
    if uuu == "N": return False
    return defx

# ------------------------------------------------------------------------

def isfile(fname):
    ''' # Return True if file exists '''
    try:
        ss = os.stat(fname)
    except:
        return False
    if stat.S_ISREG(ss[stat.ST_MODE]):
        return True
    return False

def hd(varx):
    ''' Hex dump it '''
    strx = ""
    for aa in range(len(varx)):
        strx += "%02x " % (int(aa) & 0xff);
    strx += "\n"
    return strx

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

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
    assert True == isTrue("YES")
    assert True == isTrue("OK")
    assert True == isTrue("True")
    assert True == isTrue("Y")
    assert True == isTrue("1")

    assert False == isTrue("xrue")
    assert False == isTrue("False")
    assert False == isTrue("")

def test_xint():

    assert 0 == xint(0);
    assert 1 == xint(1);
    assert 0 == xint("a");
    assert 1 == xint("b", 1);

def test_oct2():

    sss = oct2int("111")
    assert sss == 73
    ttt = oct2int("123456")
    assert ttt == 42798
    uuu = oct2int("888")
    assert uuu == 0

def test_hd():
    pass
    #print(hd("hello"))

# EOF
