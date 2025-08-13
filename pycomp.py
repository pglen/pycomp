#!/usr/bin/env python3

import sys, os, re, time

# Our modules

import  complib.args as args
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

    start_time =  time.process_time()

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
        print("loader:", time.process_time() - start_time)

    if lpg.opt_debug > 5: print (buf)
    #lstack.push(strx)
    lx = lexer.Lexer(lexdef.xtokens, lpg)
    res = []

    # This is a convenience matter
    if buf[len(buf)-1] != "\n":
        buf += "\n"
    lx.feed(buf, res)
    if lpg.opt_timing_show:
        print  ("lexer:", time.process_time() - start_time)

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

    if lpg.opt_timing_show: print  ("parser:", time.process_time() - start_time)
    # Output results
    if lpg.opt_emit:
        show_emit()

# ------------------------------------------------------------------------

if __name__ == "__main__":

    global lpg

    #sys.setrecursionlimit(25)

    #    ("Undefine", "", "Un-define variable."),

    opts =  (     ("Define", "", "Define variable."),
                  ("emit", False, "Emit Parse string."),
                  ("Target", "x86_64", "Select target. Currently x86_64 only."),
            )

    lpg = args.Lpg(opts, sys.argv)
    #print(lpg.helpdict)

    if lpg.opt_help:
        lpg.help()
        sys.exit(0)

    #print( lpg.opt_debug, type(lpg.opt_debug))
    if lpg.opt_debug > 1:
        lpg.printme()

    # Check for reasonable flags:
    if lpg.opt_verbose and lpg.opt_quiet:
        print("Warning: both verbose and quiet is set")

    if lpg.opt_Target != "x86_64":
        print("Only x86_64 is supported (for now)")
        sys.exit(0)

    sys.exit(0)

    if lpg.opt_verbose > 1:
        print("Calc options:", lpg.options, lpg.opt_verbose)

    if lpg.opt_verbose > 3:
        lpg.printme()

    if lpg.opt_verbose > 2:
        print("opts:", opts)
        print("args", args)

    if not args:
        args.help();
        exit(0);

    cnt = 0
    strx = "None"
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
