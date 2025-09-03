#!/usr/bin/env python

''' functions for the lin parser '''

import complib.stack as stack
import complib.lindef as lindef
import complib.lexdef as lexdef
import codegen.codegen as codegen

try:
    from complib.utils import *
except:
    #print(__file__, ":import local")
    from utils import *

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

# Functions to call on stamp match

astack    = stack.pStack()             # Arithmetic
dstack    = stack.pStack()             # Declaration
argstack  = stack.pStack()             # function arguments
callstack = stack.pStack()             # Function call

def func_rassn(self2, tprog):
    if pvg.opt_debug > 1:
        print("rassn()", "tprog =", tprog)
    dstack.push(tprog)

def func_rassn_stop(self2, tprog):
    if pvg.opt_debug > 1:
        print("assnr_stop()", "tprog =", tprog)
    astack.push(tprog)
    strx =   "  lea  rsi, " + self2.arrx[astack.get(0)].mstr + "\n"
    strx +=  "  mov rax, [rsi]" #self2.arrx[astack.get(1)].mstr

    strx +=   "; " + self2.arrx[astack.get(0)].mstr + " = "
    strx +=  self2.arrx[astack.get(1)].mstr

    strx +=  "\n"

    codegen.emit(strx)
    astack.empty()

def func_assn(self2, tprog):
    if pvg.opt_debug > 1:
        print("assn()", "tprog =", tprog)
    astack.push(tprog)

def func_assn_stop(self2, tprog):
    if pvg.opt_debug > 1:
        print("assn_stop()", "tprog =", tprog)
    dstack.push(tprog)
    strx =   "lea  rsi, " + self2.arrx[dstack.get(0)].mstr + "\n"
    strx +=  "mov rax, [rsi]" #self2.arrx[dstack.get(1)].mstr

    strx +=   "; " + self2.arrx[dstack.get(0)].mstr + " = "
    strx +=  self2.arrx[dstack.get(1)].mstr

    strx +=  "\n"

    codegen.emit(strx)
    astack.empty()

def func_decl_start(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_start()", "tprog =", tprog)
    dstack.empty()
    dstack.push(tprog)
    #codegen.emit(self2.arrx[tprog].mstr)

def func_decl_ident(self2, tprog):
    if pvg.opt_debug > 1:
        print("funct_decl_ident()", "tprog =", tprog)
    dstack.push(tprog)
    #codegen.emit(self2.arrx[tprog].mstr)

def func_decl_val(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_val()", "tprog =", tprog)
    dstack.push(tprog)
    #codegen.emit(self2.arrx[tprog].mstr)

def func_decl_comma(self2, tprog):
    if pvg.opt_debug > 1:
        print("decl_comma()", "tprog =", tprog)
    print("\ndstack one:", end = " ")
    for aa in dstack:
        print(self2.arrx[aa], end = " ")
    print()

    datatype = pctona(self2.arrx[dstack.get(0)].mstr)

    strx =   self2.arrx[dstack.get(1)].mstr + " : " + datatype + " "
    strx +=  self2.arrx[dstack.get(2)].mstr
    #codegen.emitdata(strx)

    strx +=  " ; " + self2.arrx[dstack.get(0)].mstr + " : "
    strx += self2.arrx[dstack.get(1)].mstr + " = "
    strx += self2.arrx[dstack.get(2)].mstr
    codegen.emitdata(strx)

    # Back off of last variable
    dstack.pop(); dstack.pop()

def func_decl_stop(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_stop()", "tprog =", tprog)

    if pvg.opt_debug > 1:
        print("\ndstack:", end = " ")
        for aa in dstack:
            print(self2.arrx[aa], end = " ")
        print()

    datatype = pctona(self2.arrx[dstack.get(0)].mstr)

    strx =   self2.arrx[dstack.get(1)].mstr + " : " + datatype + " "
    strx +=  self2.arrx[dstack.get(2)].mstr

    # if str type, put trailing zero

    if self2.arrx[dstack.get(2)].stamp.xstr == "str":
        strx +=  ", 0"

    # Output comment as well
    linex = self2.arrx[dstack.get(0)].linenum + 1
    strx +=  " ; line: " + str(linex) + " -- "
    strx +=  self2.arrx[dstack.get(0)].mstr + " : "
    strx += self2.arrx[dstack.get(1)].mstr + " = "
    strx += self2.arrx[dstack.get(2)].mstr
    codegen.emitdata(strx)

def func_space(self2, tprog):
    if pvg.opt_debug > 5:
        print("space()", "tprog =", tprog)

def func_tab(self2, tprog):
    if pvg.opt_debug > 5:
        print("tab()", "tprog =", tprog)

def func_nl(self2, tprog):
    if pvg.opt_debug > 5:
        print("nl()", "tprog =", tprog)

def func_dummy(self2, tprog):
    if pvg.opt_debug > 5:
        print("match dummy()", "tprog =", tprog)

def func_comment(self2, tprog):
    if pvg.opt_debug > 5:
        print("comment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )

def func_dcomment(self2, tprog):
    if pvg.opt_debug > 5:
        print("dcomment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
    if pvg.opt_rdocstr:
        print(self2.arrx[tprog].mstr[3:], end = "")

def func_dcomment2(self2, tprog):
    if pvg.opt_debug > 5:
        print("dcomment2()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
    if pvg.opt_rdocstr:
        print(self2.arrx[tprog].mstr[3:-2], end = "")

def func_dcomment3(self2, tprog):
    if pvg.opt_debug > 5:
        print("dcomment3()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
    if pvg.opt_rdocstr:
        print(self2.arrx[tprog].mstr[2:], end = "")

def func_str(self2, idx, tprog):
    print("func_str() idx =", idx, "tprog =", tprog, "iprog=", "slen =", len(stamps[idx][0]))
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog], "func_str pre: ")
    sys.exit(0)

def func_func_start(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_start()", pp(self2.arrx[tprog].mstr))
        argstack.empty()
        callstack.empty()
        callstack.push(astack.pop())

def func_func_decl_val(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_decl_val()", pp(self2.arrx[tprog].mstr))
        argstack.push(tprog)

def func_func_end(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_end()", pp(self2.arrx[tprog].mstr))
        #print("\nargtsack:", end = " ")
        #for aa in argstack:
        #    print(self2.arrx[aa], end = " ")
        #print()
        idx  =   callstack.get(0)
        funcname =  self2.arrx[idx].mstr
        linex = self2.arrx[idx].linenum + 1

        estr = ""
        for cnt, aa in enumerate(argstack):
            if cnt > 6:
                print("Too many arguments to function:", funcname )
                sys.exit(1)
            # Skip first arg as syscall opcode is in rax
            #estr += "   push   rbp\n"
            estr += "   mov  " + codegen.regorder[cnt+1] + "  " + \
                        ", " + self2.arrx[aa].mstr + "\n"
            #estr += "   pop   rbp\n"

        estr += "   extern " +  funcname + "\n"
        estr += "   and     rsp, 0xfffffffffffffff0\n"
        estr += "   call " +  funcname
        estr +=  " ; line: " + str(linex) + " -- " + funcname

        codegen.emit(estr)

def func_arithstart(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_arithstart()", "tprog =", tprog, self2.arrx[tprog])
    astack.empty()
    astack.push(tprog)

def func_arithop(self2, tprog):
    if pvg.opt_debug > 5:
        print("arithop: ()", "tprog =", tprog, self2.arrx[tprog])
    astack.push(tprog)

def func_addexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = astack.peek()
        print("addexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )
    astack.push(tprog)

def func_expexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = astack.peek()
        print("func_expexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )
    astack.push(tprog)

def func_mulexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = astack.peek()
        print("mulexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )

    astack.push(tprog)

def execop(arg1, op, arg2):
    print("execop:", arg1, op, arg2)
    ret = 0
    if op ==  "sqr":  ret = arg1 ** arg2
    elif op ==   "*":   ret = arg1 * arg2
    elif op ==   "/":   ret = arg1 / arg2
    elif op ==   "+":   ret = arg1 + arg2
    elif op ==   "-":   ret = arg1 - arg2
    elif op ==   "<<":  ret = arg1 >> arg2
    elif op ==   ">>":  ret = arg1 << arg2
    elif op ==   "=":   ret = arg1
    else:  print("Invalid operator")
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

                if not idx1 == None or idx2 == None:
                    print("Syntax Error")
                    return

                if pvg.opt_debug > 5:
                    print("op", pp(filter), "pr:",
                        self2.arrx[idx1], self2.arrx[idx], self2.arrx[idx2])

                self2.arrx[idx1].ival =  execop(self2.arrx[idx1].ival, filter,
                                            self2.arrx[idx2].ival)
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

def func_arit_stop(self2, tprog):
    if pvg.opt_debug > 2:
        print("func_arit_stop()", "tprog =", tprog, self2.arrx[tprog])
    # Execute operator precedence
    reduce(self2, "sqr")
    reduce(self2, "*")
    reduce(self2, "/")
    reduce(self2, "+")
    reduce(self2, "-")
    reduce(self2, ">>")
    reduce(self2, "<<")
    reduce(self2, "=")

    if pvg.opt_debug > 2:
        print("\nastack:", end = " ")
        for aa in astack:
            print(self2.arrx[aa], end = " ")
        print()

    try:
        strx =   self2.arrx[astack.get(0)].mstr + " = "
        strx +=  self2.arrx[astack.get(1)].mstr
    except:
        linex = self2.arrx[astack.get(0)].linenum + 1
        tok = self2.arrx[astack.get(0)].mstr
        print("Syntax error on line:", linex, "near:", pp(tok))
    codegen.emit(strx)

    #strx =  " ; " + self2.arrx[dstack.get(0)].mstr + " : "
    #strx += self2.arrx[dstack.get(1)].mstr + " = "
    #strx += self2.arrx[dstack.get(2)].mstr + " \n"
    #codegen.emit(strx)

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
        print("mul() tprog =", tprog, "iprog=")
    if pvg.opt_debug > 3:
        prarr(self2.arrx[tprog:tprog], "mul pre: ")
    _func_arith(self2, "*", tprog)
    if pvg.opt_debug > 5:
        prarr(self2.arrx[tprog:tprog], "mul post: ")

def func_add(self2, tprog):
    if pvg.opt_debug > 6:
        print("add() tprog =", tprog, "iprog=")
    if pvg.opt_debug > 6:
        prarr(self2.arrx[tprog:tprog], "add pre: ")
    _func_arith(self2, "+", tprog)
    if pvg.opt_debug > 6:
        prarr(self2.arrx[tprog:tprog], "add post: ")

# EOF
