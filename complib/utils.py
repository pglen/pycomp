#!/usr/bin/env python

import sys, os, re, time, stat

_gl_cnt = 0
def unique():             # create a unique temporary number
    global _gl_cnt; _gl_cnt += 1
    return _gl_cnt

#_gl_cnt2 = 0
#def unique2():             # create a unique temporary number
#    global _gl_cnt2; _gl_cnt2 += 1
#    return _gl_cnt2

# Connect parser token to lexer item. This way the definitions are synced
# without the need for double definition
# Look up, create if not found

class Lut:

    def __init__(self):
        self.tokdef = []

    def lookup(self, strx):
        ret = None
        for aa in self.tokdef:
            if strx == aa[1]:
                #print "found", aa
                ret = aa
                break
        if ret == None:
            #print ("Token '" + strx + "' not found, adding ... ", end = " " )
            self.tokdef.append((unique(), strx))
            for aa in  self.tokdef:
                if strx == aa[1]:
                    #print(aa)
                    ret = aa
                    break
            if ret == None:
                print ("Token '" + strx + "' not found, please correct it.")
        return aa

    def rlookup(self, idn):
        ret =  "none"
        for aa in  self.tokdef:
            #print("idx =", idn, "aa =", aa)
            if idn == aa[0]:
                ret = aa[1]
                break
        return ret

    def dump(self, pad = 15, perline = 5):
        res = ""
        cnt = 0
        for aa in  self.tokdef:
            strx = str(aa[0]) + " = " + "'" + aa[1] + "'"
            xlen = pad - len(strx)
            res += "%s%s" % (strx, " " * xlen)
            cnt += 1
            if cnt % perline == 0:
                res += "\n"
        #res += "\n"
        return res

class Tree:
    def __init__(self, data = None):
        self.left = None
        self.right = None
        self.children = []
        self.data = data

def time_ms(start_time):
    ttt = time.process_time() - start_time
    return "%.2f ms" % (ttt * 1000)

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
        #elif(chh == '\e'):
        #    retx += '\\e'
        elif(chh == '\\'):
            retx += '\\\\'
        else:
            retx += chh
        pos += 1
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

#try:
#    cccc = strx[pos+1]
#    print("second backslash", cccc)
#    if cccc == '\\':
#        retx += "\\"
#        pos += 1
#        continue
#except:
#    pass

# ------------------------------------------------------------------------
# Give the user the usual options for true / false - 1 / 0 - y / n

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
