#!/usr/bin/env python3

import sys, os, re, time
import getopt

# Our modules

import  complib.linparse as linparse
import  complib.stack as stack
import  complib.lexer as lexer
import  complib.lexdef as lexdef
import  complib.lindef as lindef

from complib.utils import *

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

    got_clock =  time.process_time()

    if lpg.opt_verbose > 1:
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

    if lpg.opt_timing_show:
        print("loader:", time.process_time() - got_clock)

    if lpg.opt_debug > 5: print (buf)
    #lstack.push(strx)
    lx = lexer.Lexer(lexdef.xtokens, lpg)
    res = []

    # This is a convenience matter
    if buf[len(buf)-1] != "\n":
        buf += "\n"
    lx.feed(buf, res)
    if lpg.opt_timing_show:
        print  ("lexer:", time.process_time() - got_clock)

    if lpg.opt_debug > 5:
        prarr(res, "lex res: ")

    if lpg.opt_xshow_lexer:  # To show what the lexer did
        for aa in res:
            if lpg.opt_verbose:
                print(aa.dump(), end = " ")
            else:
                print(aa, end = " ")
        print()
    if lpg.opt_xshow_lexer > 1:  # Only show lexer
        #exit(0)
        return

    if lx.state != lexdef.ST.INI_STATE.value:
        sss = lexdef.state2str(lx.state)
        print("Warning on lexer state: unterminated state", sss,
                        "line:", lx.linenum + 1, "col:", lx.lastpos - lx.lastline + 1)
    par = linparse.LinParse(lindef.stamps, lpg)
    par.feed(res, buf)

    prarr(par.arrx, "result:", lpg.opt_verbose)

    if lpg.opt_timing_show: print  ("parser:", time.process_time() - got_clock)
    # Output results
    if lpg.opt_emit:
        show_emit()

# ------------------------------------------------------------------------

def help():
    myname = os.path.basename(sys.argv[0])
    print ("PCOMP parallel compiler.")
    print ("Usage: " + myname + " [options] filename [ filename ] ... ")
    print ("Options:    -d level  - Parser debug level (1-10) default: 0")
    print ("            -l level  - Lexer debug level (1-10) default: 0")
    print ("            -o file   - Outfile name")
    print ("            -e        - Emit parse string")
    print ("            -V        - Print version")
    print ("            -v        - Verbose (add -v for more details)")
    print ("            -s        - Show parser states"    )
    print ("            -t        - Show timing of compile")
    print ("            -T        - Temp dir for work related files")
    print ("            -L        - Lex only")
    print ("            -x        - Show lexer output")
    print ("            -p        - Show parser messages")
    print ("            -h        - Help (this screen)")

# ------------------------------------------------------------------------

if __name__ == "__main__":

    #sys.setrecursionlimit(25)
    #opts = []; args = []

    lpg.auto_opt()

    try:
        opts, args = getopt.getopt(sys.argv[1:], lpg.options)
    except getopt.GetoptError as err:
        print ("Invalid option(s) on command line:", err)
        sys.exit(1)
    #print ("opts", opts, "args", args)
    for aa in opts:
        if   aa[0] == "-d": lpg.opt_debug = xint(aa[1], 1)
        elif aa[0] == "-l": lpg.opt_lxdebug = xint(aa[1], 1)
        elif aa[0] == "-o": lpg.opt_outfile = aa[1]
        elif aa[0] == "-v": lpg.opt_verbose += 1
        elif aa[0] == "-x": lpg.opt_xshow_lexer = True
        elif aa[0] == "-X": lpg.opt_show_lexer = 2  # True for lexer, 2 for only lexer
        elif aa[0] == "-t": lpg.opt_timing_show = True
        elif aa[0] == "-e": lpg.opt_emit = True
        elif aa[0] == "-q": lpg.opt_quiet = True
        elif aa[0] == "-p": lpg.opt_show_parse  = True
        elif aa[0] == "-s": lpg.opt_show_state  = True
        elif aa[0] == "-L": lpg.opt_lex_only  = True
        elif aa[0] == "-T": lpg.opt_temp  = aa[1]
        elif aa[0] == "-h": help();  exit(1)
        elif aa[0] == "-V": print("Version 0.9"); exit(0)
        else: pass

    if lpg.opt_verbose > 1:
        print("Calc options:", lpg.options, lpg.opt_verbose)

    if not args:
        help();  exit(0);

    if lpg.opt_verbose > 3: print(args)
    if lpg.opt_verbose > 2: lpg.print()

    cnt = 0
    while True:
        try:
            if cnt >= len(args):
                break
            strx = args[cnt]

            if lpg.opt_verbose:
                print("Compiling: %s" % strx)
        except:
            print("Error compiling:", strx)
            pass ; #exit(1)
        #lstack = stack.pStack()
        fullpath = os.path.abspath(strx);
        lpg.docroot = os.path.dirname(fullpath)
        parsefile(strx)
        cnt += 1

# EOF
