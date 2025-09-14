#!/usr/bin/env python

''' Functions for the lin parser, to call on stamp match '''

import complib.stack as stack
import complib.lindef as lindef
import complib.linpool as linpool
import complib.lexdef as lexdef
import codegen.codegen as codegen

ops_prec = "**", "*", "/", "+", "-", ">>", "<<" #, "="

try:
    from complib.utils import *
except:
    from utils import *

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

# Stack definitions

arithstack = stack.pStack()            # Arithmetic
argstack  = stack.pStack()             # Function arguments
callstack = stack.pStack()             # Function calls

def execop(self2, arg1, op, arg2):
    ret = 0
    if op ==   "**":  ret = arg1 ** arg2
    elif op ==   "*":   ret = arg1 * arg2
    elif op ==   "/":   ret = arg1 // arg2
    elif op ==   "+":   ret = arg1 + arg2
    elif op ==   "-":   ret = arg1 - arg2
    elif op ==   "<<":  ret = arg1 << arg2
    elif op ==   ">>":  ret = arg1 >> arg2
    elif op ==   "=":   ret = arg2
    else:  error(self2, "Invalid operator '%s': " % op )
    print(" execop:", arg1, op, arg2, "; ret = ", ret, )
    return ret

def reduce_const(self2, filter, xstack, pos = 0):

    print("reduce_const():", filter, "pos =", pos)

    if pvg.opt_debug > 6:
        print("\narithstack pre reduce:", pp(filter), end = " ")
        for aa in arithstack:
            print(self2.arrx[aa], end = " ")
        print()

    # Walk the stack
    loopx = pos ;
    statex = 0 ; numidx = -1 ; opidx = -1 ;  wasop = False
    while True:
        if loopx >= len(xstack):
            break
        idx = xstack.get(loopx)
        if self2.arrx[idx].flag != 0:
            loopx += 1
            continue

        print(loopx, pp(self2.arrx[idx].mstr), end = " -- ")
        #print("arithstack: [", self2.arrx[idx].stamp.xstr,
        #                    pp(self2.arrx[idx].mstr), end = "] " )
        if statex == 0:
            if self2.arrx[idx].stamp.xstr == "num":
                if pvg.opt_debug > 5:
                    print(" arg1: ", pp(self2.arrx[idx].mstr), filter)
                numidx = idx
            elif self2.arrx[idx].stamp.xstr == "(":
                self2.arrx[idx].flag = 1
                # Recurse into stack
                print("\n ** recurse:", self2.arrx[idx].mstr)
                for aa in ops_prec:
                    reduce_const(self2, aa, xstack, idx)
                print("\n ** after recurse")
                #break

            elif self2.arrx[idx].stamp.xstr == ")":
                self2.arrx[idx].flag = 1
                print("paren2:", idx, self2.arrx[idx].stamp.xstr)
                break
            else:
                pass

        elif statex == 1:
            if self2.arrx[idx].stamp.xstr == "num":
                if pvg.opt_debug > 5:
                    print(" arg2", pp(self2.arrx[idx].mstr))
                if numidx >= 0:
                    self2.arrx[numidx].ival =  execop(self2, self2.arrx[numidx].ival,
                                filter, self2.arrx[idx].ival)
                    self2.arrx[numidx].mstr = str(self2.arrx[numidx].ival)
                    self2.arrx[idx].flag = 1
                    self2.arrx[opidx].flag = 1
                statex = 0;
                wasop = True
        else:
            pass

        if self2.arrx[idx].mstr == filter:
            if pvg.opt_debug > 2:
                print(" op: filter =", filter, pp(self2.arrx[idx].mstr))
            opidx = idx
            statex = 1
        loopx += 1

    if pvg.opt_debug > 6:
        if wasop:
            print("\nxstack post reduce:", pp(filter), end = " ")
            for aa in xstack:
                print(self2.arrx[aa], end = " ")
            print()

    return loopx

class   Funcs():

    def call_start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call_start()", pp(self2.arrx[tprog].mstr))
            #print("func arithstack: len =", arithstack.getlen(), end = " ")
            #for aa in arithstack:
            #    print(self2.arrx[aa], end = " ")
            #print()
        argstack.empty()
        callstack.empty()
        callstack.push(arithstack.pop())
        #print("call stack", str(callstack))

    def call_decl_val(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call_decl_val()", self2.arrx[tprog])
        argstack.push(tprog)

    def call_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call_end()", pp(self2.arrx[tprog].mstr))
            print("argstack:", end = " ")
            for aa in argstack:
                print(self2.arrx[aa], end = " ")
            print()
            print("calltsack:", end = " ")
            for aa in callstack:
                print(self2.arrx[aa], end = " ")
            print()

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


    def func_start(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_start()", pp(self2.arrx[tprog].mstr))

    def func_arg_start(self2, tprog):
            if pvg.opt_debug > 1:
                print("func_func_arg_start()", pp(self2.arrx[tprog].mstr))

    def func_args(self2, tprog):
            if pvg.opt_debug > 1:
                print("func_func_args()", pp(self2.arrx[tprog].mstr))
            argstack.empty()
            callstack.empty()
            callstack.push(arithstack.pop())

    def func_end(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_end()", pp(self2.arrx[tprog].mstr))

funcs = Funcs()

class Arith():

    def arith_stop(self, self2, tprog):
        if pvg.opt_debug > 2:
            print("func_arith_stop()", "tprog =", tprog, self2.arrx[tprog])

        #if self2.pvg.opt_debug > 4:
        #    for aa in self2.statestack:
        #        print("statestack:", lindef.ST.get(aa))

        #if pvg.opt_debug > 2:
        #    print("arithstack:", end = " ")
        #    for aa in arithstack:
        #        print(self2.arrx[aa], end = " ")
        #    print()

        # Execute as operator precedence
        for aa in ops_prec:
            reduce_const(self2, aa, arithstack)

        #if self2.statestack.getlen() > 1:
        #    sss =  self2.statestack[self2.statestack.getlen() - 1]
        #    #print("Arith parent context:", lindef.ST.get(sss))

        #strx =  " ; " + self2.arrx[arithstack.get(0)].mstr + " : "
        #strx += self2.arrx[arithstack.get(1)].mstr + " = "
        #strx += self2.arrx[arithstack.get(2)].mstr + " \n"
        #codegen.emit(strx)

    def arithstart(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arithstart()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.empty()
        arithstack.push(tprog)

    def arithop(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("arithop()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def addexpr(self, self2, tprog):
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("addexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        arithstack.push(tprog)

    def subexpr(self, self2, tprog):
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("subexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        arithstack.push(tprog)

    def divexpr(self, self2, tprog):
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("divexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        arithstack.push(tprog)

    def expexpr(self, self2, tprog):
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("func_expexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        arithstack.push(tprog)

    def mulexpr(self, self2, tprog):
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("mulexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        arithstack.push(tprog)

    def assnexpr(self, self2, tprog):
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("assnexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        arithstack.push(tprog)

    def expr(self, self2, tprog):

        ''' Just push '''
        arithstack.push(tprog)

arith = Arith()

# ------------------------------------------------------------------------

class Assn():

    def rassn(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_rassn()", "tprog =", tprog)
        arithstack.push(tprog)

    def rassn_stop(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_assnr_stop()", "tprog =", tprog)
        #arithstack.push(tprog)

        if pvg.opt_debug > 2:
            print("\narithstack rassn:", end = " ")
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()

        strx =   "  lea  rsi, " + self2.arrx[arithstack.get(0)].mstr + "\n"
        strx +=  "  mov rax, " + self2.arrx[arithstack.get(1)].mstr + "\n"
        strx +=  "  mov [rsi], rax "
        linex = self2.arrx[arithstack.get(1)].linenum + 1
        strx +=   " ; line " + str(linex) + " -- " + self2.arrx[arithstack.get(0)].mstr + " => "
        strx +=  self2.arrx[arithstack.get(1)].mstr
        strx +=  "\n"

        codegen.emit(strx)
        arithstack.empty()

    def assn_start(self2, tprog):
        if pvg.opt_debug > 1:
            print("assn_start()", "tprog =", tprog, self2.arrx[tprog])
        #arithstack.empty()
        arithstack.push(tprog)

    def func_assn(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_assn()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def assn_stop(self2, tprog):
        if pvg.opt_debug > 1:
            print("assn_stop()", "tprog =", tprog)
        arithstack.push(tprog)

        if pvg.opt_debug > 2:
            print("\narithstack assn:", end = " ")
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()
        tpi = linpool.lookpool(self2, self2.arrx[arithstack.get(0)].mstr)
        if not tpi:
            print("Undeclared variable:", pp(self2.arrx[arithstack.get(0)].mstr))
            return

        print("tpi:", tpi, self2.arrx[arithstack.get(0)],
                            self2.arrx[arithstack.get(2)])

        if tpi.typex == "arr":
            strx =   "lea  rsi, " + self2.arrx[arithstack.get(0)].mstr + "\n"
            strx +=  "mov rax, [rsi]" #self2.arrx[arithstack.get(1)].mstr
            strx +=  self2.arrx[arithstack.get(2)].mstr
        elif tpi.typex == "u64":
            strx =   "    lea   rsi, " + self2.arrx[arithstack.get(0)].mstr + "\n"
            strx +=  "    mov   rax,  " + self2.arrx[arithstack.get(2)].mstr  + "\n"
            strx +=  "    mov   [rsi] , rax \n"
        elif tpi.typex == "u32":
            strx =   "    lea   rsi, " + self2.arrx[arithstack.get(0)].mstr + "\n"
            strx +=  "    mov   rax,  0 \n"
            strx +=  "    mov   eax,  " + self2.arrx[arithstack.get(2)].mstr  + "\n"
            strx +=  "    mov   [rsi] , eax \n"
        elif tpi.typex == "u16":
            strx =   "    lea   rsi, " + self2.arrx[arithstack.get(0)].mstr + "\n"
            strx +=  "    mov   ax,  " + self2.arrx[arithstack.get(2)].mstr  + "\n"
            strx +=  "    mov   [rsi] , ax \n"
        elif tpi.typex == "u8":
            strx =   "    lea   rsi, " + self2.arrx[arithstack.get(0)].mstr + "\n"
            strx +=  "    mov   al,  " + self2.arrx[arithstack.get(2)].mstr  + "\n"
            strx +=  "    mov   [rsi] , al \n"
        else:
            pass
            strx = "; No code for assignment."

        #print("assn:\n", strx)

        #strx +=   "; " + self2.arrx[arithstack.get(0)].mstr + " = "
        #strx +=  "\n"

        codegen.emit(strx)
        arithstack.empty()

assn = Assn()

class Decl():

    def decl_start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl_start()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def decl_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl_end()", "tprog =", tprog, self2.arrx[tprog])
        #arithstack.push(tprog)

    def decl_col(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl_col()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def decl_ident(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl_ident()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)
        #codegen.emit(self2.arrx[tprog].mstr)

    def decl_val(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl_val()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)
        #codegen.emit(self2.arrx[tprog].mstr)

    def decl_comma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl_comma()", "tprog =", tprog)
        print("arithstack comma:", end = " ")
        if pvg.opt_debug > 2:
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()
        return
        datatype = linpool.addtopool(self2, arithstack)
        strx =   self2.arrx[arithstack.get(1)].mstr + " : " + datatype + " "
        strx +=  self2.arrx[arithstack.get(2)].mstr
        #codegen.emitdata(strx)
        strx +=  " ; " + self2.arrx[arithstack.get(0)].mstr + " : "
        strx += self2.arrx[arithstack.get(1)].mstr + " = "
        strx += self2.arrx[arithstack.get(2)].mstr
        codegen.emitdata(strx)

        # Back off of last variable
        arithstack.pop(); arithstack.pop()

    def decl_stop(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl_stop()", "tprog =", tprog, self2.arrx[tprog])

        if pvg.opt_debug > 0:
            print("arithstack: len =", arithstack.getlen(), end = " ")
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()

        return
        datatype = linpool.addtopool(self2, arithstack)

        strx =   self2.arrx[arithstack.get(1)].mstr + " : " + datatype + " "
        #print("datatype =", pp(self2.arrx[arithstack.get(0)].mstr), datatype)

        # type dependent expand
        if self2.arrx[arithstack.get(0)].mstr == "arr":
            if arithstack.getlen() <= 2:
                # patch missing declaration argument with zero /empty
                strx += ""
            else:
                strx +=  asmesc(self2.arrx[arithstack.get(2)].mstr)
        elif datatype == "u32" or datatype == "u16" or datatype == "u8":
            if arithstack.getlen() <= 2:
                # patch missing declaration argument with zero /empty
                strx += " 0 "
            else:
                strx +=  "[" + self2.arrx[arithstack.get(2)].mstr + "[]"
        else:
            # This is where type expnsion takes place
            if arithstack.getlen() <= 2:
                strx += " 0 "
            else:
                strx +=  self2.arrx[arithstack.get(2)].mstr

        #print("strx", strx)
        # Output comment as well
        linex = self2.arrx[arithstack.get(0)].linenum + 1
        strx +=  " ; line: " + str(linex) + " -- "
        strx +=  self2.arrx[arithstack.get(0)].mstr + " : "
        strx += self2.arrx[arithstack.get(1)].mstr + " = "

        if arithstack.getlen() <= 2:
            strx += " 0 "
        else:
            strx += self2.arrx[arithstack.get(2)].mstr

        codegen.emitdata(strx)

decl = Decl()

# ------------------------------------------------------------------------

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

class Misc():

    def func_str(self, self2, idx, tprog):
        print("func_str() idx =", idx, "tprog =", tprog, "iprog=", "slen =", len(stamps[idx][0]))
        if pvg.opt_debug > 5:
            prarr(self2.arrx[tprog:tprog], "func_str pre: ")
        sys.exit(0)


    def func_brace(self, self2, tprog):

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

    def func_parent(self, self2, tprog):

        if pvg.opt_debug > 3:
            print("func_parent()", tprog, self2.arrx[tprog])

        if pvg.opt_debug > 5:
            prarr(self2.arrx, "func pre par feed:", True)

        arithstack.push(tprog)

        #self2._feed(tprog + 1, tprog - 1)
        #if pvg.opt_debug > 5:
        #    prarr(self2.arrx[tprog:tprog+1], "func post par feed:")

        #if pvg.opt_debug > 6:
        #    prarr(self2.arrx, "func paren post:", True)


    def _func_arith(self, self2, opstr, tprog):

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

    def func_mul(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("mul() tprog =", tprog, "iprog=")
        if pvg.opt_debug > 3:
            prarr(self2.arrx[tprog:tprog], "mul pre: ")
        _func_arith(self2, "*", tprog)
        if pvg.opt_debug > 5:
            prarr(self2.arrx[tprog:tprog], "mul post: ")

    def func_add(self, self2, tprog):
        if pvg.opt_debug > 6:
            print("add() tprog =", tprog, "iprog=")
        if pvg.opt_debug > 6:
            prarr(self2.arrx[tprog:tprog], "add pre: ")
        _func_arith(self2, "+", tprog)
        if pvg.opt_debug > 6:
            prarr(self2.arrx[tprog:tprog], "add post: ")

misc = Misc()

# EOF


