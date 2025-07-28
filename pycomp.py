#!/usr/bin/env python3

#from __future__ import absolute_import
#from __future__ import print_function

import sys, os, re, time

# Our modules

import  complib.linparse as linparse
from    complib.lindef import stamps as stamps

import  complib.stack as stack
import  complib.lexer as lexer
import  complib.lexdef as lexdef

from complib.utils import *

import inspect
if inspect.isbuiltin(time.process_time):
    time.clock = time.process_time


# ------------------------------------------------------------------------
# Accumulate output: (mostly for testing)
_cummulate = ""

def emit(strx):
    global _cummulate;
    _cummulate += " '" + strx + "' "

def show_emit():
    global _cummulate;
    print (_cummulate)

# ------------------------------------------------------------------------
# Parser functions that are called on parser events. Note the 'e' prefix
# for the 'end' function -> bold() -> ebold()  (end bold)
# The trivial functions are extracted to pungfunc.py

# ------------------------------------------------------------------------

def parsefile(strx):

    global buf, lpg

    got_clock =  time.clock()

    if lpg.verbose > 1:
        print ("Showing file:", strx)
    try:
        fh = open(strx)
    except:
        strerr = "Cannot open file: '" + strx + "'"
        print (strerr)
        #mainview.add_text(strerr)
        return
    try:
        buf = fh.read();
    except:
        strerr2 =  "Cannot read file '" + strx + "'"
        print (strerr2)
        #mainview.add_text(strerr2)
        fh.close()
        return
    fh.close()

    if lpg.show_timing:
        print  ("loader:", time.clock() - got_clock)

    if lpg.pgdebug > 5: print (buf)
    lstack.push(strx)
    lx = lexer.Lexer(lexdef.xtokens, lpg)
    res = []

    # This is a convenience matter
    if buf[len(buf)-1] != "\n":
        buf += "\n"
    lx.feed(buf, res)
    if lpg.show_timing:
        print  ("lexer:", time.clock() - got_clock)

    if lpg.pgdebug > 5:
        prarr(res, "lex res: ")

    if lpg.show_lexer:  # To show what the lexer did
        for aa in res:
            if lpg.verbose:
                print(aa.dump(), end = " ")
            else:
                print(aa, end = " ")
        print()
    if lpg.lex_only:
        exit(0)

    if lx.state != lexdef.ST.INI_STATE.value:
        sss = lexdef.state2str(lx.state)
        print("Warning on lexer state: unterminated state", sss,
                        "line:", lx.linenum + 1, "col:", lx.lastpos - lx.lastline + 1)
    par = linparse.LinParse(stamps, lpg)
    par.feed(res, buf)

    prarr(par.arrx, "result:", lpg.verbose)

    if lpg.show_timing: print  ("parser:", time.clock() - got_clock)
    # Output results
    if lpg.emit:
        show_emit()

# ------------------------------------------------------------------------

def help():
    myname = os.path.basename(sys.argv[0])
    print ("Utility for compiling a pycomp file.")
    print ("Usage: " + myname + " [options] filename [ filename ] ... ")
    print ("Options:    -d level  - Parser debug level (1-10) default: 0")
    print ("            -l level  - Lexer debug level (1-10) default: 0")
    print ("            -o file   - Outfile name")
    print ("            -e        - Emit parse string")
    print ("            -V        - Print version")
    print ("            -v        - Verbose (add -v for more details)")
    print ("            -s        - Show parser states"    )
    print ("            -t        - Show timing of compile")
    print ("            -L        - Lex only")
    print ("            -x        - Show lexer output")
    print ("            -p        - Show parser messages")
    print ("            -h        - Help (this screen)")

# ------------------------------------------------------------------------

if __name__ == "__main__":

    import getopt

    #sys.setrecursionlimit(25)

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "thvVfpesxLl:d:o:")
    except getopt.GetoptError as err:
        print ("Invalid option(s) on command line:", err)
        sys.exit(1)
    #print ("opts", opts, "args", args)
    for aa in opts:
        if   aa[0] == "-d": lpg.pgdebug = xint(aa[1], 1)
        elif aa[0] == "-l": lpg.lxdebug = xint(aa[1], 1)
        elif aa[0] == "-o": lpg.outfile = aa[1]
        elif aa[0] == "-v": lpg.verbose += 1
        elif aa[0] == "-x": lpg.show_lexer = True
        elif aa[0] == "-t": lpg.show_timing = True
        elif aa[0] == "-e": lpg.emit = True
        elif aa[0] == "-p": lpg.show_parse  = True
        elif aa[0] == "-s": lpg.show_state  = True
        elif aa[0] == "-L": lpg.lex_only  = True

        elif aa[0] == "-h": help();  exit(1)
        elif aa[0] == "-V": print("Version 0.9"); exit(0)

    try:     strx = args[0]
    except:  help(); exit(1)

    lstack = stack.pStack()

    fullpath = os.path.abspath(strx);
    lpg.docroot = os.path.dirname(fullpath)
    parsefile(strx)

# EOF
