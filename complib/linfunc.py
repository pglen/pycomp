#!/usr/bin/env python

''' functions for the lin parser '''

import complib.stack as stack
import complib.lindef as lindef
import complib.linpool as linpool
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

# Stack definitions

pastack    = stack.pStack()             # Arithmetic
argstack  = stack.pStack()             # Function arguments
callstack = stack.pStack()             # Function calls

# ------------------------------------------------------------------------

def func_rassn(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_rassn()", "tprog =", tprog)
    pastack.push(tprog)

def func_rassn_stop(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_assnr_stop()", "tprog =", tprog)
    #pastack.push(tprog)

    if pvg.opt_debug > 2:
        print("\npastack rassn:", end = " ")
        for aa in pastack:
            print(self2.arrx[aa], end = " ")
        print()

    strx =   "  lea  rsi, " + self2.arrx[pastack.get(0)].mstr + "\n"
    strx +=  "  mov rax, " + self2.arrx[pastack.get(1)].mstr + "\n"
    strx +=  "  mov [rsi], rax "
    linex = self2.arrx[pastack.get(1)].linenum + 1
    strx +=   " ; line " + str(linex) + " -- " + self2.arrx[pastack.get(0)].mstr + " => "
    strx +=  self2.arrx[pastack.get(1)].mstr
    strx +=  "\n"

    codegen.emit(strx)
    pastack.empty()

def func_assn_start(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_assn()", "tprog =", tprog, self2.arrx[tprog])
    #pastack.empty()
    pastack.push(tprog)

def func_assn(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_assn()", "tprog =", tprog, self2.arrx[tprog])
    pastack.push(tprog)

def func_assn_stop(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_assn_stop()", "tprog =", tprog)
    pastack.push(tprog)

    if pvg.opt_debug > 2:
        print("\npastack assn:", end = " ")
        for aa in pastack:
            print(self2.arrx[aa], end = " ")
        print()
    tpi = linpool.lookpool(self2, self2.arrx[pastack.get(0)].mstr)
    if not tpi:
        print("Undeclared variable:", pp(self2.arrx[pastack.get(0)].mstr))
        return

    print("tpi:", tpi, self2.arrx[pastack.get(0)],
                        self2.arrx[pastack.get(2)])

    if tpi.typex == "arr":
        strx =   "lea  rsi, " + self2.arrx[pastack.get(0)].mstr + "\n"
        strx +=  "mov rax, [rsi]" #self2.arrx[pastack.get(1)].mstr
        strx +=  self2.arrx[pastack.get(2)].mstr
    elif tpi.typex == "u64":
        strx =   "    lea   rsi, " + self2.arrx[pastack.get(0)].mstr + "\n"
        strx +=  "    mov   rax,  " + self2.arrx[pastack.get(2)].mstr  + "\n"
        strx +=  "    mov   [rsi] , rax \n"
    elif tpi.typex == "u32":
        strx =   "    lea   rsi, " + self2.arrx[pastack.get(0)].mstr + "\n"
        strx +=  "    mov   rax,  0 \n"
        strx +=  "    mov   eax,  " + self2.arrx[pastack.get(2)].mstr  + "\n"
        strx +=  "    mov   [rsi] , eax \n"
    elif tpi.typex == "u16":
        strx =   "    lea   rsi, " + self2.arrx[pastack.get(0)].mstr + "\n"
        strx +=  "    mov   ax,  " + self2.arrx[pastack.get(2)].mstr  + "\n"
        strx +=  "    mov   [rsi] , ax \n"
    elif tpi.typex == "u8":
        strx =   "    lea   rsi, " + self2.arrx[pastack.get(0)].mstr + "\n"
        strx +=  "    mov   al,  " + self2.arrx[pastack.get(2)].mstr  + "\n"
        strx +=  "    mov   [rsi] , al \n"
    else:
        pass
        strx = "; No code for assignment."

    #print("assn:\n", strx)

    #strx +=   "; " + self2.arrx[pastack.get(0)].mstr + " = "
    #strx +=  "\n"

    codegen.emit(strx)
    pastack.empty()

def func_decl_start(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_start()", "tprog =", tprog, self2.arrx[tprog])
    #pastack.empty()
    pastack.push(tprog)
    #codegen.emit(self2.arrx[tprog].mstr)

def func_decl_ident(self2, tprog):
    if pvg.opt_debug > 1:
        print("funct_decl_ident()", "tprog =", tprog)
    pastack.push(tprog)
    #codegen.emit(self2.arrx[tprog].mstr)

def func_decl_val(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_val()", "tprog =", tprog, self2.arrx[tprog])
    pastack.push(tprog)
    #codegen.emit(self2.arrx[tprog].mstr)

def func_decl_comma(self2, tprog):
    if pvg.opt_debug > 1:
        print("decl_comma()", "tprog =", tprog)
    print("\npastack one:", end = " ")
    if pvg.opt_debug > 2:
        for aa in pastack:
            print(self2.arrx[aa], end = " ")
        print()

    datatype = linpool.addtopool(self2, pastack)

    strx =   self2.arrx[pastack.get(1)].mstr + " : " + datatype + " "
    strx +=  self2.arrx[pastack.get(2)].mstr
    #codegen.emitdata(strx)

    strx +=  " ; " + self2.arrx[pastack.get(0)].mstr + " : "
    strx += self2.arrx[pastack.get(1)].mstr + " = "
    strx += self2.arrx[pastack.get(2)].mstr
    codegen.emitdata(strx)

    # Back off of last variable
    pastack.pop(); pastack.pop()

def func_space(self2, tprog):
    if pvg.opt_debug > 5:
        print("space()", "tprog =", tprog)

def func_tab(self2, tprog):
    if pvg.opt_debug > 5:
        print("tab()", "tprog =", tprog)

def func_nl(self2, tprog):
    if pvg.opt_debug > 5:
        print("nl()", "tprog =", tprog)

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

def func_func_call(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_call()", pp(self2.arrx[tprog].mstr))

def func_func_start(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_start()", pp(self2.arrx[tprog].mstr))
        argstack.empty()
        callstack.empty()
        callstack.push(pastack.pop())

def func_func_arg_start(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_arg_start()", pp(self2.arrx[tprog].mstr))

def func_func_args(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_args()", pp(self2.arrx[tprog].mstr))
        argstack.empty()
        callstack.empty()
        callstack.push(pastack.pop())

def func_func_decl_val(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_decl_val()", self2.arrx[tprog])
        argstack.push(tprog)

def func_decl_stop(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_decl_stop()", "tprog =", tprog)

    if pvg.opt_debug > 0:
        print("\npastack: len =", pastack.getlen(), end = " ")
        for aa in pastack:
            print(self2.arrx[aa], end = " ")
        print()

    datatype = linpool.addtopool(self2, pastack)

    strx =   self2.arrx[pastack.get(1)].mstr + " : " + datatype + " "
    #print("datatype =", pp(self2.arrx[pastack.get(0)].mstr), datatype)

    # type dependent expand
    if self2.arrx[pastack.get(0)].mstr == "arr":
        if pastack.getlen() <= 2:
            # patch missing declaration argument with zero /empty
            strx += ""
        else:
            strx +=  asmesc(self2.arrx[pastack.get(2)].mstr)
    elif datatype == "u32" or datatype == "u16" or datatype == "u8":
        if pastack.getlen() <= 2:
            # patch missing declaration argument with zero /empty
            strx += " 0 "
        else:
            strx +=  "[" + self2.arrx[pastack.get(2)].mstr + "[]"
    else:
        # This is where type expnsion takes place
        if pastack.getlen() <= 2:
            strx += " 0 "
        else:
            strx +=  self2.arrx[pastack.get(2)].mstr

    #print("strx", strx)
    # Output comment as well
    linex = self2.arrx[pastack.get(0)].linenum + 1
    strx +=  " ; line: " + str(linex) + " -- "
    strx +=  self2.arrx[pastack.get(0)].mstr + " : "
    strx += self2.arrx[pastack.get(1)].mstr + " = "

    if pastack.getlen() <= 2:
        strx += " 0 "
    else:
        strx += self2.arrx[pastack.get(2)].mstr

    codegen.emitdata(strx)

def func_func_end(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_end()", pp(self2.arrx[tprog].mstr))

        return
        #print("\nargtsack:", end = " ")
        #for aa in argstack:
        #    print(self2.arrx[aa], end = " ")
        #print()
        idx  =   callstack.get(0)
        funcname =  self2.arrx[idx].mstr
        linex = self2.arrx[idx].linenum + 1

        # Exception on printf stack call
        estr = ""
        if funcname == "printf":
            estr += "    and     rsp, 0xfffffffffffffff0\n"
            estr += "    mov     rbp, rsp\n"
        cnt = 0
        for aa in argstack:
            tpi = linpool.lookpool(self2, self2.arrx[aa].mstr)
            #print("linpool.lookpool tpi =>", tpi)
            if not tpi:
                error(self2, "Variable: '%s' not defined" % self2.arrx[aa].mstr)

            if cnt  >= len(codegen.regorder) - 1:
                #error(self2, "Too many arguments to function:") #, funcname )
                #sys.exit(1)
                pass
            # Skip first arg as syscall opcode is in rax
            #print("arg:", self2.arrx[aa].dump())
            # Expand types
            if tpi.typex == "arr":
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                             ", " + self2.arrx[aa].mstr + "\n"
            elif  tpi.typex == "u32" or tpi.typex == "s32" :
                estr += "    mov rax, 0\n"
                estr += "    mov ax, word [" + self2.arrx[aa].mstr + "]\n"
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                             ", [" + self2.arrx[aa].mstr + "]\n"
            elif  tpi.typex == "u16" or tpi.typex == "s16":
                estr += "    mov rax, 0\n"
                estr += "    mov ax, word [" + self2.arrx[aa].mstr + "]\n"
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                                    ", rax\n"
            elif  tpi.typex == "u8" or tpi.typex == "s8":
                estr += "    mov rax, 0\n"
                estr += "    mov al, byte [" + self2.arrx[aa].mstr + "]\n"
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                                     ", rax\n"
            cnt += 1
        estr += "    xor  rax, rax" + "\n"
        #print("estr =\n", estr)

        estr += "    extern " +  funcname + "\n"
        estr += "    call " +  funcname
        estr +=  " ; line: " + str(linex + 1) + " -- " + funcname

        codegen.emit(estr)

def func_arithstart(self2, tprog):
    if pvg.opt_debug > 1:
        print("func_arithstart()", "tprog =", tprog, self2.arrx[tprog])
    pastack.empty()
    pastack.push(tprog)

def func_arithop(self2, tprog):
    if pvg.opt_debug > 5:
        print("arithop: ()", "tprog =", tprog, self2.arrx[tprog])
    pastack.push(tprog)

def func_addexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = pastack.peek()
        print("addexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )
    pastack.push(tprog)

def func_expexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = pastack.peek()
        print("func_expexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )
    pastack.push(tprog)

def func_mulexpr(self2, tprog):
    if pvg.opt_debug > 5:
        tprog2 = pastack.peek()
        print("mulexpr: ",
                "tprog  =", tprog,  self2.arrx[tprog],
                "tprog2 =", tprog2, self2.arrx[tprog2] )

    pastack.push(tprog)

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
        for bb in range(len(pastack)):
            idx = pastack.get(bb)
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
                    error("Syntax Error near", self2.arrx[idx].stamp.xstr)
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
        print("\npastack:", end = " ")
        for aa in pastack:
            print(self2.arrx[aa], end = " ")
        print()
    try:
        strx =   self2.arrx[pastack.get(0)].mstr + " = "
        strx +=  self2.arrx[pastack.get(1)].mstr
    except:
        linex = self2.arrx[pastack.get(0)].linenum + 1
        tok = self2.arrx[pastack.get(0)].mstr
        error(self2, "Syntax error",
                    addstr =  "near: %s" % (pp(tok)))
    codegen.emit(strx)

    #strx =  " ; " + self2.arrx[pastack.get(0)].mstr + " : "
    #strx += self2.arrx[pastack.get(1)].mstr + " = "
    #strx += self2.arrx[pastack.get(2)].mstr + " \n"
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
