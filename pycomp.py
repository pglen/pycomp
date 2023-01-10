#!/usr/bin/env python3

#from __future__ import absolute_import
from __future__ import print_function

import sys, os, re, time
import signal, pickle

#import pygtk, gobject, gtk, pango

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import GdkPixbuf

# Our modules

import  complib.parser as parser
import  complib.stack as stack
import  complib.lexer as lexer
import  complib.lexdef as lexdef

from complib.parsedef import *
from complib.utils import *

import inspect
if inspect.isbuiltin(time.process_time):
    time.clock = time.process_time

# Some globals read: (Pang View Globals):

class pvg():

    buf = None; xstack = None; verbose = False
    pgdebug = False; show_lexer = False; full_screen = False
    lstack = None;  fullpath = None; docroot = None
    got_clock = 0; show_timing = False; second = ""
    xfull_screen = False; flag = False; show_parse = False
    emit = False; show_state = False; pane_pos = -1
    currline = 0;


# Just to make sure no one is left out: (for debug only)

#if len(parser.tokens) != len(parser.tokdef):
#    print ("Number of token definitions and tokens do not match.")
#    sys.exit(1)

# Our display object
#mainview = pangdisp.PangoView(pvg)

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

from    complib.utils import *

#cb.Text("d", "dd", "ddd")

# Check parse table: (obsolete: now it is self checking)
'''
for aa in parser.parsetable:
    if aa[2]:
        found = 0
        for bb in parser.tokdef:
            if aa[2] == bb[1]:
                found = True
        if not found :
            print ("Parse table contains unkown definition '" + aa[2] + "'")
            sys.exit(1)

'''


def main():
    # Not using main window
    #Gtk.main()
    return 0

# ------------------------------------------------------------------------

def bslink():

    if lstack.stacklen() == 1:
        return

    lstack.pop()
    strx = lstack.last()

    #print ("backspace linking to:", strx)

    if strx == None or strx == "":
        return

#    mainview.showcur(True)
    showfile(strx)

def link(strx):

    if strx == None or strx == "":
        return

    if not isfile(strx):
        #mainview.showcur(False)
        message_dialog("Missing or broken link",
            "Cannot find file '%s'" % strx );
        return
    #print ("linking to:", strx)
    showfile(strx)

# ------------------------------------------------------------------------

def     message_dialog(title, strx):

    #dialog = Gtk.MessageDialog(mainview,
    dialog = Gtk.MessageDialog(None,
            Gtk.DIALOG_MODAL | Gtk.DIALOG_DESTROY_WITH_PARENT,
            Gtk.MESSAGE_INFO, Gtk.BUTTONS_OK, strx)
    dialog.set_title(title);
    dialog.run()
    dialog.destroy()

# ------------------------------------------------------------------------

def showfile(strx):

    global buf, xstack, mainview, pvg, ts

    got_clock =  time.clock()

    if pvg.verbose:
        print ("Showing file:", strx)
    try:
        fh = open(strx)
    except:
        strerr = "File:  '" + strx + "'  must be an existing and readble file. "
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

    #mainview.clear(pvg.flag)
    ts.clear()

    lx = lexer.Lexer(lexdef.tokens)
    xstack = stack.Stack()
    lx.feed(buf, xstack)

    if pvg.show_timing:
        print  ("lexer:", time.clock() - got_clock)

    if pvg.show_lexer:  # To show what the lexer did
        #xstack.dump()
        cnt = 0; xlen = len(xstack._store)
        while cnt < xlen:
            tt = xstack._store[cnt];
            print(tt[5], ":", tt[6], " -- ", tt[0],  lexdef.rtok[tt[0]], pp(tt[2]))
            cnt += 1

    if lx.state == lexdef.STR_STATE:
        print("Warning on lexer state: unterminated string")

    par = parser.Parse(pvg)
    par.feed(buf, xstack)

    #cb.flush()
    #mainview.showcur(False)

    if pvg.show_timing:
        print  ("parser:", time.clock() - got_clock)

    # Output results
    if pvg.emit:
        show_emit()

# ------------------------------------------------------------------------

def help():
    myname = os.path.basename(sys.argv[0])
    print()
    print (myname + ":", "Version 0.1 - Utility for compiling a pcomp file.")
    print ()
    print ("Usage: " + myname + " [options] filename")
    print ()
    print ("Options are:")
    print ("            -d level  - Debug level (1-10)")
    print ("            -o file   - Outfile name")
    print ("            -e        - Emit parse string")
    print ("            -V        - Version")
    print ("            -v        - Verbose")
    print ("            -s        - Show parser states"    )
    print ("            -t        - Show timing")
    print ("            -x        - Show lexer output")
    print ("            -p        - Show parser messages")
    print ("            -h        - Help")
    print ()

# ------------------------------------------------------------------------

if __name__ == "__main__":

    import getopt

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:o:hvVfpesx")
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

        if aa[0] == "-c":
            pvg.second = aa[1]
            #print (pvg.second)

        if aa[0] == "-a":
            try:
                pvg.pane_pos = int(aa[1])
            except:
                print ("Pane position must be a number")

            print (pvg.pane_pos)

        if aa[0] == "-o": pvg.outfile = ""

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": pvg.verbose = True
        if aa[0] == "-V": print("Version 0.9"); exit(0)
        if aa[0] == "-x": pvg.show_lexer = True
        if aa[0] == "-t": pvg.show_timing = True
        if aa[0] == "-e": pvg.emit = True
        if aa[0] == "-p": pvg.show_parse  = True
        if aa[0] == "-s": pvg.show_state  = True
    try:
        strx = args[0]
    except:
        help(); exit(1)

    lstack = stack.Stack()
    fullpath = os.path.abspath(strx);
    pvg.docroot = os.path.dirname(fullpath)

    if pvg.xfull_screen:
        pass
        #mainview.fullscreen()
    elif pvg.full_screen:
        pass
        #mainview.set_fullscreen()

    #mainview.callback = link
    #mainview.bscallback = bslink

    if pvg.second != "":
        pass
        '''
        if pvg.pane_pos >= 0:
            #mainview.set_pane_position(pvg.pane_pos)
        else:
            #mainview.set_pane_position(250)
        pvg.flag = True
        showfile(pvg.second)
        '''

    pvg.flag = False
    showfile(strx)

    main()

# EOF
