#!/usr/bin/env python

''' functions for the linear parser '''

import operator

from complib.utils import *

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

# Functions to call on stamp match

def func_dummy(self2, idx, tprog, iprog):
    if pvg.pgdebug > 0:
        print("match dummy idx =", idx, "tprog =", tprog, "iprog=", iprog, "slen =", len(stamps[idx][0]))

def func_str(self2, idx, tprog, iprog):
    print("match str idx =", idx, "tprog =", tprog, "iprog=", iprog, "slen =", len(stamps[idx][0]))
    if pvg.pgdebug > 2:
        prarr(self2.arrx[tprog:tprog+iprog], "arrx str pre: ")
    sys.exit(0)

def func_paren(self2, tprog, iprog):

    if pvg.pgdebug > 5:
        print("match paren tprog =", tprog, "iprog=", iprog)
    if pvg.pgdebug > 2:
        prarr(self2.arrx[tprog:tprog+iprog], "arrx paren pre: ")

    #self2.arrx[tprog].flag = 1
    #self2.arrx[tprog+iprog-1].flag = 1

    if pvg.pgdebug > 5:
        prarr(self2.arrx[tprog:tprog+iprog+1], "arrx pre par feed:")

    self2._feed(tprog + 1, tprog+iprog - 1)

    if pvg.pgdebug > 5:
        prarr(self2.arrx[tprog:tprog+iprog+1], "arrx post par feed:")

    # Done with parentheses
    self2.arrx[tprog].flag = 1
    self2.arrx[tprog + iprog - 1].flag = 1

    if pvg.pgdebug > 2:
        prarr(self2.arrx[tprog:tprog+iprog+1], "arrx paren post:")

def _func_arith(self2, opstr, tprog, iprog):

    uprog = 0;

    # Skip till number
    while 1:
        if uprog >= iprog: return
        if self2.arrx[tprog + uprog].flag: uprog += 1 ; continue
        if "num" == self2.arrx[tprog + uprog].stamp[1]:
            break
        uprog += 1
    #print("num[", uprog, self2.arrx[tprog + uprog][2])
    startx = uprog
    ttt =  self2.arrx[tprog + uprog]

    # Skip till operator
    while 1:
        if uprog >= iprog: return
        if self2.arrx[tprog + uprog].flag: uprog += 1 ; continue
        if opstr == self2.arrx[tprog + uprog].stamp[1]:
            break
        uprog += 1
    op =  self2.arrx[tprog + uprog]
    #print("op[",  uprog, self2.arrx[tprog + uprog].stamp[1])
    # Skip till number
    while 1:
        if uprog >= iprog: return
        if self2.arrx[tprog + uprog].flag: uprog += 1 ; continue
        if "num" == self2.arrx[tprog + uprog].stamp[1]:
            break
        uprog += 1
    #print("num2[",  uprog, self2.arrx[tprog + uprog][2])
    ttt2 =  self2.arrx[tprog + uprog]

    #print("ttt =", ttt)
    #print("ttt2 =", ttt2)

    if opstr == "+":
        ttt.mstr = int(ttt.mstr) + int(ttt2.mstr)
    elif opstr == "*":
        ttt.mstr = int(ttt.mstr) * int(ttt2.mstr)
    else:
        print("Invalid op:", opstr);

    self2.arrx[tprog + startx] = ttt
    op.flag = 1
    ttt2.flag = 1

    #for ss in range(tprog+1, tprog+iprog):
    #    if self2.arrx[ss].flag:  continue
    #    #prarr(self2.arrx[ss:ss+1], "delx")
    #    #self2.arrx[ss].flag = 1

def func_mul(self2, tprog, iprog):
    if pvg.pgdebug > 5:
        print("match mul tprog =", tprog, "iprog=", iprog)
    if pvg.pgdebug > 2:
        prarr(self2.arrx[tprog:tprog+iprog], "arrx mul pre: ")
    _func_arith(self2, "*", tprog, iprog)
    if pvg.pgdebug > 2:
        prarr(self2.arrx[tprog:tprog+iprog], "arrx mul post: ")

def func_add(self2, tprog, iprog):
    if pvg.pgdebug > 5:
        print("match add tprog =", tprog, "iprog=", iprog)
    if pvg.pgdebug > 2:
        prarr(self2.arrx[tprog:tprog+iprog], "arrx add pre: ")
    _func_arith(self2, "+", tprog, iprog)
    if pvg.pgdebug > 2:
        prarr(self2.arrx[tprog:tprog+iprog], "arrx add post: ")

# EOF
