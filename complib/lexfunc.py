#!/usr/bin/env python3

''' Called while parsing '''

fpvg = None

def funcpvg(xpvg):
    global fpvg
    fpvg = xpvg

def func_start_esc(self2, tt):
    if fpvg.opt_lexdebug > 6:
        print("func_start_esc()", tt)

def func_start_str(self2, tt):
    if fpvg.opt_lexdebug > 6:
        print("func_start_str()", tt)
    #self2.accum[self2.state] = ""

# EOF
