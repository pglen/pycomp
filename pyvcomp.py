#!/usr/bin/env python3

import sys, os, re, time

# Our modules

import  complib.args as args
import  complib.linparse as linparse
import  complib.stack as stack
import  complib.lexer as lexer
import  complib.lexdef as lexdef
import  complib.lindef as lindef
#import  complib.ptree as ptree

from complib.ptree import *
from complib.utils import *

Version = "Version: 1.0.0; "
Build   = "Build date: Aug 13 2025"

# Name is prepened opt_ and name's first letter is the option letter

opts =  (\
    #   name        initval     Help string
    #   ----        -------     ----------------
    ("Define",      [],         "Define variable. (multiple defines accepted)"),
    ("outfile",     "",         "Name of output file."),
    ("xlexer_show", False,      "Show lexer output"),
    ("comp_only",   False,      "Compile only."),
    ("emit",        False,      "Emit parse string."),
    ("Target",      "x86_64",   "Select target. Def: x86_64 (no other targets)"),
    ("state_show",  False,      "Show parser states."),
    ("timing_show", False,      "Show timings for program execution."),
    ("pre_only",    False,      "Pre-process only."),
    ("just_lex",    False,      "Only execute lexer."),
    ("emit",        False,      "Emit parse string."),
    ("animate",     False,      "Animate (slow) output."),
    ("rdocstr",     False,          "Show document strings"),
    ("ldebug",      0,          "Lexer debug level. Def=0 0=>none 9=>noisy."),
    ("workdir",     "./tmp",    "Directory for temp files. Def=./tmp"),
    )

def parsefile(strx):

    ''' Parse file '''

    global buf, lpg

    if lpg.opt_verbose.cnt > 1:
        print ("Processing file:", strx)

    start_time =  time.process_time()

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
        print("load  time:", time_ms(start_time) )

    if lpg.opt_debug > 5: print (buf)

    if lpg.opt_timing_show:
        start_time =  time.process_time()
    lx = lexer.Lexer(lexdef.xtokens, lpg)

    # This is a convenience matter
    if buf:
        if buf[len(buf)-1] != "\n":
            buf += "\n"

    res = lx.feed(buf)
    if lpg.opt_timing_show:
        print  ("lexer time:", time_ms(start_time) )

    if lpg.opt_debug > 5:
        prarr(res, "lex res: ")

    if lpg.opt_xlexer_show:  # To show what the lexer did
        for aa in res:
            if lpg.opt_verbose.cnt:
                print(aa.dump())
            else:
                print(aa, end = " ")
        print()

    if lpg.opt_just_lex:  # Only do lexer
        return

    if lx.state != lexdef.INI_STATE:
        sss = lexdef.state2str(lx.state)
        print("Warning on lexer state: unterminated state", sss,
                        "line:", lx.linenum + 1, "col:", lx.lastpos - lx.lastline + 1)
    start_time =  time.process_time()
    par = linparse.LinParse(lindef.stamps, lpg)
    par.feed(res, buf)
    if lpg.opt_timing_show: print  ("parse time:", time_ms(start_time))

    #prarr(res, "Result of '%s': " % strx, lpg.opt_verbose.cnt)
    #emit("hello")

    # Output results
    if lpg.opt_emit:
        show_emit()

    print(treeroot)

def setheads(lpg):
    prestr =    "PCOMP parallel compiler.\n" \
                "Usage: " + lpg.myname + \
                " [options] filename [filename(s)] ... [options]\n" \
                "Available options:"

    poststr  =  "Argument values are identical for the short " \
                "form and long form options.\n"  \
                "Def: stands for default value. " \
                "Options after file names are also interpreted."

    lpg.setpre(prestr)
    lpg.setpost(poststr)

# ------------------------------------------------------------------------

if __name__ == "__main__":

    #global lpg

    #sys.setrecursionlimit(25)

    lpg = args.Lpg(opts, sys.argv)
    setheads(lpg)

    if lpg.opt_Version:
        print(lpg.myname, Version, Build)
        sys.exit(0)
    if lpg.opt_help:
        lpg.help()
        sys.exit(0)
    if lpg.opt_Help2:
        lpg.Help()
        sys.exit(0)
    if lpg.opt_Target != "x86_64":
        print("Error: only x86_64 is supported (for now)")
        sys.exit(0)
    if lpg.opt_verbose.cnt > 2:
        lpg.printme()
    if not lpg.args:
        print("Missing file name(s). Use: -h option for help")
        sys.exit(0);

    cnt = 0 ; strx = "None"
    while True:
        try:
            if cnt >= len(lpg.args):
                break
            strx = lpg.args[cnt]
        except:
            #print("Error compiling:", strx, sys.exc_info())
            pass
        fullpath = os.path.abspath(strx);
        docroot = os.path.dirname(fullpath)
        #print("docroot", docroot)
        parsefile(strx)
        cnt += 1

# EOF
