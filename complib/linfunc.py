#!/usr/bin/env python

''' functions for the lin parser '''

import complib.stack as stack
import complib.lindef as lindef

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

astack = stack.pStack()             # Arithmetic
dstack = stack.pStack()             # Declaration

def func_decl_start(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_start", "tprog =", tprog)
    dstack.empty()
    dstack.push(tprog)
    #emit(self2.arrx[tprog].mstr)

def func_decl_ident(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_ident", "tprog =", tprog)
    dstack.push(tprog)
    #emit(self2.arrx[tprog].mstr)

def func_decl_val(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_val", "tprog =", tprog)
    dstack.push(tprog)
    #emit(self2.arrx[tprog].mstr)

def func_decl_comma(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_comma", "tprog =", tprog)
    print("\ndstack one:", end = " ")
    for aa in dstack:
        print(self2.arrx[aa], end = " ")
    print()
    dstack.empty()
    #dstack.push(tprog)
    #emit(self2.arrx[tprog].mstr)

def func_decl_stop(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_stop", "tprog =", tprog)
    #print("\ndstack:", end = " ")
    #for aa in dstack:
    #    print(self2.arrx[aa], end = " ")
    #print()
    strx =  "; " + self2.arrx[dstack.get(0)].mstr + " : "
    strx += self2.arrx[dstack.get(1)].mstr + " = "
    strx += self2.arrx[dstack.get(2)].mstr
    emit(strx)

    datatype = pctona(self2.arrx[dstack.get(0)].mstr)

    strx =   self2.arrx[dstack.get(1)].mstr + " : " + datatype + " "
    strx +=  self2.arrx[dstack.get(2)].mstr
    emit(strx)

def pctona(ddd):

    #print("pctona:", ddd)

    retx = "db"
    if ddd == "u8":
        retx = "db"
    elif ddd == "u16":
        retx = "dw"
    elif ddd == "u32":
        retx = "dd"
    return retx

def func_space(self2, tprog):
    if pvg.opt_debug > 5:
        print("func_space", "tprog =", tprog)

def func_nl(self2, tprog):
    if pvg.opt_debug > 5:
        print("func_nl", "tprog =", tprog)

def func_dummy(self2, tprog):
    if pvg.opt_debug > 5:
        print("match dummy", "tprog =", tprog)

def func_comment(self2, tprog):
    if pvg.opt_debug > 5:
        print("func_comment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )

def func_dcomment(self2, tprog):
    if pvg.opt_debug > 5:
        print("func_dcomment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
    if pvg.opt_rdocstr:
        print(self2.arrx[tprog].mstr[3:], end = "")

def func_dcomment2(self2, tprog):
    if pvg.opt_debug > 5:
        print("func_dcomment2()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
    if pvg.opt_rdocstr:
        print(self2.arrx[tprog].mstr[3:-2], end = "")

def func_dcomment3(self2, tprog):
    if pvg.opt_debug > 5:
        print("func_dcomment3()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
    if pvg.opt_rdocstr:
        print(self2.arrx[tprog].mstr[2:], end = "")

def func_str(self2, idx, tprog):
    print("func_str() idx =", idx, "tprog =", tprog, "iprog=", "slen =", len(stamps[idx][0]))
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog], "func_str pre: ")
    sys.exit(0)

def func_func(self2, tprog):
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog], "func_func pre: ")
    #sys.exit(0)
    self2.arrx[tprog].flag = 1
    #self2._feed(tprog + 1, tprog - 1)

def func_arithstart(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_arithstart: ", "tprog =", tprog, self2.arrx[tprog])
    astack.push(tprog)

def func_arithop(self2, tprog):
    if pvg.opt_debug > 5:
        print("func_arithop: ", "tprog =", tprog, self2.arrx[tprog])
    astack.push(tprog)

def func_addexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = astack.peek()
        print("func_addexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )
    astack.push(tprog)

def func_mulexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = astack.peek()
        print("func_mulexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )

    astack.push(tprog)

def exeop(op, arg1, arg2):
    #print("exeop", arg1, arg2)
    if op ==  "sqr":  ret = arg1 ** arg2
    if op ==   "*":   ret = arg1 * arg2
    if op ==   "/":   ret = arg1 / arg2
    if op ==   "+":   ret = arg1 + arg2
    if op ==   "-":   ret = arg1 - arg2
    if op ==   "<<":   ret = arg1 >> arg2
    if op ==   ">>":   ret = arg1 << arg2
    return ret

def reduce(self2, filter):

    while True:
        # Cycle back here if changed the list
        bstack = stack.pStack()
        loopx = 0
        # Make a clean index:
        for bb in range(len(astack)):
            idx = astack.get(bb)
            if self2.arrx[idx].flag == 0:
                bstack.push(idx)
        #print("bstack:", filter)
        #for cc in bstack:
        #    print(self2.arrx[cc])
        while True:
            if loopx >= len(bstack):
                break
            idx = bstack.get(loopx)
            if  self2.arrx[idx].stamp.xstr == filter:
                idx1 = bstack.get(loopx-1)
                idx2 = bstack.get(loopx+1)
                if pvg.opt_debug > 5:
                    print("op", pp(filter), "pr:",
                        self2.arrx[idx1], self2.arrx[idx], self2.arrx[idx2])
                self2.arrx[idx1].ival =  exeop(filter,
                                    self2.arrx[idx1].ival, self2.arrx[idx2].ival)
                # Just to make it look uniform
                self2.arrx[idx1].mstr = str(self2.arrx[idx1].ival)
                #self2.arrx[idx1].flag = 0
                self2.arrx[idx].flag = self2.arrx[idx2].flag = 1
                if pvg.opt_debug > 5:
                    print("op", pp(filter), "po:",
                        self2.arrx[idx1], self2.arrx[idx], self2.arrx[idx2])
                # Restart loop if changed
                break
            loopx += 1
        # End of stack
        if loopx >= len(bstack):
            break

def func_endarith(self2, tprog):
    if pvg.opt_debug > 2:
        print("func_endarith", "tprog =", tprog, "iprog=")
    # Execute operator precedence
    reduce(self2, "sqr")
    reduce(self2, "*")
    reduce(self2, "/")
    reduce(self2, "+")
    reduce(self2, "-")
    reduce(self2, ">>")
    reduce(self2, "<<")

def func_brace(self2, tprog):

    #if pvg.opt_debug > 5:
    #    print("match brack tprog =", tprog, "iprog=")

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog], "func brace pre: ")

    # Done with parentheses
    self2.arrx[tprog].flag = 1
    self2.arrx[tprog  - 1].flag = 1

    if pvg.opt_debug > 5:
        prarr(self2.arrx, "pre func brace feed:", True)

    #self2._feed(tprog + 1, tprog - 1)

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+1], "post func brace feed:")

    if pvg.opt_debug > 6:
        prarr(self2.arrx, "func brace post:", True)

    # Force rescan
    return True

def func_paren(self2, tprog):

    #if pvg.opt_debug > 5:
    #    print("match paren tprog =", tprog, "iprog=")

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog], "func paren pre: ")

    # Done with parentheses
    self2.arrx[tprog].flag = 1
    self2.arrx[tprog  - 1].flag = 1

    if pvg.opt_debug > 5:
        prarr(self2.arrx, "func pre par feed:", True)

    #self2._feed(tprog + 1, tprog - 1)

    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog+1], "func post par feed:")

    if pvg.opt_debug > 6:
        prarr(self2.arrx, "func paren post:", True)

    # Force rescan
    return True

def _func_arith(self2, opstr, tprog):

    uprog = 0;
    # Skip till number
    while 1:
        #if uprog >= iprog: return
        if self2.arrx[tprog + uprog].flag: uprog += 1 ; continue
        if "num" == self2.arrx[tprog + uprog].stamp.xstr:
            break
        uprog += 1
    #print("num[", uprog, self2.arrx[tprog + uprog][2])
    startx = uprog
    ttt =  self2.arrx[tprog + uprog]
    # Skip till operator
    while 1:
        #if uprog >= iprog: return
        if self2.arrx[tprog + uprog].flag: uprog += 1 ; continue
        if opstr == self2.arrx[tprog + uprog].stamp.xstr:
            break
        uprog += 1
    op =  self2.arrx[tprog + uprog]
    #print("op[",  uprog, self2.arrx[tprog + uprog].stamp.xstr)
    # Skip till number
    while 1:
        #if uprog >= iprog: return
        if self2.arrx[tprog + uprog].flag: uprog += 1 ; continue
        if "num" == self2.arrx[tprog + uprog].stamp.xstr:
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

def func_mul(self2, tprog):
    if pvg.opt_debug > 5:
        print("match func  mul tprog =", tprog, "iprog=")
    if pvg.opt_debug > 3:
        prarr(self2.arrx[tprog:tprog], "mul pre: ")
    _func_arith(self2, "*", tprog)
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog], "mul post: ")

def func_add(self2, tprog):
    if pvg.opt_debug > 6:
        print("match func add tprog =", tprog, "iprog=")
    if pvg.opt_debug > 6:
        prarr(self2.arrx[tprog:tprog], "add pre: ")
    _func_arith(self2, "+", tprog)
    if pvg.opt_debug > 6:
        prarr(self2.arrx[tprog:tprog], "add post: ")

# EOF
