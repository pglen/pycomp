#!/usr/bin/env python3

#from __future__ import absolute_import
#from __future__ import print_function

import sys, os, re, time
import signal, pickle

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

# Some globals read: (Pang View Globals):

class pvg():

    buf = None; xstack = None; verbose = 0
    pgdebug = False; show_lexer = False;
    lstack = None;  fullpath = None; docroot = None
    got_clock = 0; show_timing = False; second = ""
    flag = False; show_parse = False
    emit = False; show_state = False; pane_pos = -1
    currline = 0;

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

    global buf, pvg

    got_clock =  time.clock()

    #if pvg.verbose > 2:
    #    print ("Showing file:", strx)

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

    if pvg.show_timing:
        print  ("loader:", time.clock() - got_clock)

    if pvg.pgdebug > 5: print (buf)
    lstack.push(strx)
    lx = lexer.Lexer(lexdef.xtokens, pvg)
    res = []
    lx.feed(buf, res)
    if pvg.pgdebug > 5:
        prarr(res, "lex res: ")

    if pvg.show_timing:
        print  ("lexer:", time.clock() - got_clock)
    if pvg.show_lexer:  # To show what the lexer did
        for aa in res:
            print(aa, end = " ")
        print()

    if lx.state != lexdef.INI_STATE:
        print("Warning on lexer state: unterminated string")
    par = linparse.LinParse(stamps, pvg)
    par.feed(res, buf)
    if pvg.show_timing: print  ("parser:", time.clock() - got_clock)
    # Output results
    if pvg.emit:
        show_emit()

# ------------------------------------------------------------------------

def help():
    myname = os.path.basename(sys.argv[0])
    print ("Utility for compiling a pycomp file.")
    print ("Usage: " + myname + " [options] filename")
    print ("Options:    -d level  - Debug level (1-10)")
    print ("            -o file   - Outfile name")
    print ("            -e        - Emit parse string")
    print ("            -V        - Version")
    print ("            -v        - Verbose")
    print ("            -s        - Show parser states"    )
    print ("            -t        - Show timing")
    print ("            -x        - Show lexer output")
    print ("            -p        - Show parser messages")
    print ("            -h        - Help (this screen)")

# ------------------------------------------------------------------------

if __name__ == "__main__":

    import getopt

    sys.setrecursionlimit(25)

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "thvVfpesxd:o:")
    except getopt.GetoptError as err:
        print ("Invalid option(s) on command line:", err)
        sys.exit(1)

    #print ("opts", opts, "args", args)

    for aa in opts:
        if aa[0] == "-d":
            try:
                pvg.pgdebug = int(aa[1])
            except:
                pvg.pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-V": print("Version 0.9"); exit(0)
        if aa[0] == "-v": pvg.verbose += 1
        if aa[0] == "-x": pvg.show_lexer = True
        if aa[0] == "-t": pvg.show_timing = True
        if aa[0] == "-e": pvg.emit = True
        if aa[0] == "-p": pvg.show_parse  = True
        if aa[0] == "-s": pvg.show_state  = True
        if aa[0] == "-s": pvg.show_state  = True
        if aa[0] == "-o": pvg.outfile = aa[0]
    try:
        strx = args[0]
    except:
        help(); exit(1)
    lstack = stack.Stack()
    fullpath = os.path.abspath(strx);
    pvg.docroot = os.path.dirname(fullpath)
    parsefile(strx)

# EOF
