#!/usr/bin/env python3

#from __future__ import absolute_import
#from __future__ import print_function

import sys, os, re, time

def yint(strx, defx = 0):

    ''' Convert to integer without fault.
            Return defx if it is an invalid integer. '''

    ret = defx
    try:
        ret = int(strx)
    except ValueError: pass
    except: print(sys.exc_info())
    return ret

def fmt(strx):
    strx = cesc(strx)
    strx = pad(strx, 2)
    return strx

def pad(strx, lenz):
    xlen = len(strx)
    if xlen < lenz:
        strx += " " * (lenz - xlen)
    return strx

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

def toch(pos):

    if pos < 32: return '0'
    strx = "%c" % chr(pos)
    return strx

# ------------------------------------------------------------------------

if __name__ == "__main__":

    start = 0
    import getopt
    opts = []; args = []
    #try:
    #    opts, args = getopt.getopt(sys.argv[1:], "s:")
    #except getopt.GetoptError as err:
    #    print ("Invalid option(s) on command line:", err)
    #    sys.exit(1)
    ##print ("opts", opts, "args", args)
    #for aa in opts:
    #    if   aa[0] == "-s": start = int(aa[1], 16)

    try:
        start = int(sys.argv[1], 16)
    except:
        pass

    print("Unicode codepoints from %x" % start)
    rep = 6
    for aa in range(126):
        pos = start + aa
        print( "%x" % pos, toch(pos), end = "   ")
        if aa % rep == rep - 1:
            print()
# EOF