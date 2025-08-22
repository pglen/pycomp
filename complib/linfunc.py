#!/usr/bin/env python

''' functions for the lin parser '''

#import operator

try:
    from complib.utils import *
except:
    #print(__file__, ":import local")
    from utils import *

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

# Functions to call on stamp match

def func_dummy(self2, tprog, iprog):
    if pvg.opt_debug > 5:
        print("match dummy", "tprog =", tprog, "iprog=", iprog)

def func_comment(self2, tprog, iprog):
    if pvg.opt_debug > 5:
        print("func_comment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )

def func_dcomment(self2, tprog, iprog):
    if pvg.opt_debug > 5:
        print("func_comment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
    if pvg.opt_rdocstr:
        print(self2.arrx[tprog].mstr, end = "")

def func_str(self2, idx, tprog, iprog):
    print("func_str() idx =", idx, "tprog =", tprog, "iprog=", iprog, "slen =", len(stamps[idx][0]))
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+iprog], "func_str pre: ")
    sys.exit(0)

def func_func(self2, tprog, iprog):
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+iprog], "func_func pre: ", True)
    #sys.exit(0)
    self2.arrx[tprog].flag = 1
    #self2._feed(tprog + 1, tprog+iprog - 1)

def func_brace(self2, tprog, iprog):

    #if pvg.opt_debug > 5:
    #    print("match brack tprog =", tprog, "iprog=", iprog)

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+iprog], "func brace pre: ")

    # Done with parentheses
    self2.arrx[tprog].flag = 1
    self2.arrx[tprog + iprog - 1].flag = 1

    if pvg.opt_debug > 5:
        prarr(self2.arrx, "pre func brace feed:", True)

    #self2._feed(tprog + 1, tprog+iprog - 1)

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+iprog+1], "post func brace feed:")

    if pvg.opt_debug > 6:
        prarr(self2.arrx, "func brace post:", True)

    # Force rescan
    return True

def func_paren(self2, tprog, iprog):

    #if pvg.opt_debug > 5:
    #    print("match paren tprog =", tprog, "iprog=", iprog)

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+iprog], "func paren pre: ")

    # Done with parentheses
    self2.arrx[tprog].flag = 1
    self2.arrx[tprog + iprog - 1].flag = 1

    if pvg.opt_debug > 5:
        prarr(self2.arrx, "func pre par feed:", True)

    #self2._feed(tprog + 1, tprog+iprog - 1)

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+iprog+1], "func post par feed:")

    if pvg.opt_debug > 6:
        prarr(self2.arrx, "func paren post:", True)

    # Force rescan
    return True

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
        ttt.mstr = str(int(ttt.mstr) + int(ttt2.mstr))
    elif opstr == "*":
        ttt.mstr = str(int(ttt.mstr) * int(ttt2.mstr))
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
    if pvg.opt_debug > 5:
        print("match func  mul tprog =", tprog, "iprog=", iprog)
    if pvg.opt_debug > 3:
        prarr(self2.arrx[tprog:tprog+iprog], "mul pre: ")
    _func_arith(self2, "*", tprog, iprog)
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+iprog], "mul post: ")

def func_add(self2, tprog, iprog):
    if pvg.opt_debug > 6:
        print("match func add tprog =", tprog, "iprog=", iprog)
    if pvg.opt_debug > 6:
        prarr(self2.arrx[tprog:tprog+iprog], "add pre: ")
    _func_arith(self2, "+", tprog, iprog)
    if pvg.opt_debug > 6:
        prarr(self2.arrx[tprog:tprog+iprog], "add post: ")

# EOF
