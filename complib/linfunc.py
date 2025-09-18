#!/usr/bin/env python

''' Functions for the lin parser, to call on stamp match '''

import complib.stack as stack
import complib.lindef as lindef
import complib.linpool as linpool
import complib.lexdef as lexdef
import codegen.codegen as codegen

# End it with empty "" operator for cleanup
#ops_prec = "**", "*", "/", "+", "-", ">>", "<<" #, "="
ops_prec = "*","+", ""
int_types = "u64", "s64", "u32", "s32", "u16", "s16", "u8", "s8",
float_types = "float", "double", "quad"

try:
    from complib.utils import *
except:
    from utils import *

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

# Stack definitions

arithstack = stack.pStack(name='arithstack')     # Arithmetic
argstack  = stack.pStack(name='argstack')        # Function arguments
callstack = stack.pStack(name='callstack')       # Function calls
gllevel = 0

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

    if pvg.opt_debug > 5:
        print(" execop:", arg1, op, arg2, "; ret = ", ret, )

    return ret

def reduce(self2, xstack, filter, pos = 0):

    if pvg.opt_debug > 7:
        print("reduce():", "filter =", pp(filter), "pos =", pos)

    #if pvg.opt_debug > 4:
    #    print("\narithstack pre reduce:", end = " ")
    #    for aa in arithstack:
    #        print(self2.arrx[aa], end = " ")
    #    print()

    # Walk the stack
    loopx = pos ; wasop = False
    statex = 0 ; numidx = -1 ; opidx = -1 ;  num2idx = -1
    while True:
        if loopx >= len(xstack):
            break
        idx = xstack.get(loopx)
        if self2.arrx[idx].flag != 0:
            loopx += 1
            continue

        if pvg.opt_debug > 7:
            print("pos:", loopx, pp(self2.arrx[idx].stamp.xstr),
                        pp(self2.arrx[idx].mstr), end = " -- ")
        if pvg.opt_debug > 7:
            print("arithstack: [", self2.arrx[idx].stamp.xstr,
                            pp(self2.arrx[idx].mstr), end = "] " )

        if self2.arrx[idx].stamp.xstr == "(":
            self2.arrx[idx].flag = 1
            # Recurse into parenthases
            if pvg.opt_debug > 7:
                print("\n ** recurse:", "idx:", idx, pp(self2.arrx[idx].mstr))
            global gllevel
            gllevel += 1
            for aa in ops_prec:
                reduce(self2, xstack, aa, idx)
            if pvg.opt_debug > 7:
                print("\n ** after recurse" )
            gllevel -= 1
            if pvg.opt_debug > 7:
                print("\nxstack post recurse:", end = " ")
                for aa in xstack:
                    if 1: #self2.arrx[aa].flag == 0:
                        print(self2.arrx[aa], end = " ")
                print()
        if self2.arrx[idx].stamp.xstr == ")":
            if pvg.opt_debug > 7:
                print("\nparen2:", idx, pp(self2.arrx[idx].stamp.xstr), loopx)
            #if gllevel == 0:
            if filter == "":
                self2.arrx[idx].flag = 1
            else:
                return
        # Blind assign first number
        if statex == 0:
            if self2.arrx[idx].stamp.xstr == "num":
                numidx = idx
                if pvg.opt_debug > 7:
                    print(" arg1: ", pp(self2.arrx[numidx].mstr))
        elif statex == 1:
            if self2.arrx[idx].stamp.xstr == "num":
                #statex = 0
                num2idx = idx
                if pvg.opt_debug > 7:
                    print(" arg1", pp(self2.arrx[numidx].mstr),
                            " op", pp(self2.arrx[opidx].mstr),
                            " arg2", pp(self2.arrx[num2idx].mstr))
                    if pvg.opt_debug > 7:
                        print("numidx =", numidx, "opidx =", opidx)
                if numidx >= 0 and opidx >= 0:
                    bb =  execop(self2, self2.arrx[numidx].ival,
                            self2.arrx[opidx].mstr,
                            self2.arrx[idx].ival)
                    self2.arrx[numidx].ival = bb
                    self2.arrx[numidx].mstr = str(bb)
                    self2.arrx[idx].flag = 1
                    self2.arrx[opidx].flag = 1
                    wasop = True
                    opidx = -1
                pass
         # If filter match, step state
        if self2.arrx[idx].mstr == filter:
            if pvg.opt_debug > 7:
                print(" op: ", pp(filter), pp(self2.arrx[idx].mstr))
            opidx = idx
            statex = 1
        loopx += 1
    if pvg.opt_debug > 7:
        if wasop:
            print("\nxstack post reduce:", end = " ")
            for aa in xstack:
                print(self2.arrx[aa], end = " ")
            print()
    return

class   FuncCall():

    def start(self, self2, tprog):
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

    def decl_val(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call_decl_val()", self2.arrx[tprog])
        argstack.push(tprog)

    def end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call_end()", pp(self2.arrx[tprog].mstr))
            print("argstack:", end = " ")
            for aa in argstack:
                print(self2.arrx[aa], end = " ")
            print()
            print("callstack:", end = " ")
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

fcall = FuncCall()

class   Funcs():

    def start(self2, tprog):
        if pvg.opt_debug > 1:
            print("func_func_start()", pp(self2.arrx[tprog].mstr))

    def arg_start(self2, tprog):
            if pvg.opt_debug > 1:
                print("func_func_arg_start()", pp(self2.arrx[tprog].mstr))

    def args(self2, tprog):
            if pvg.opt_debug > 1:
                print("func_func_args()", pp(self2.arrx[tprog].mstr))
            argstack.empty()
            callstack.empty()
            callstack.push(arithstack.pop())

    def end(self2, tprog):
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

        if pvg.opt_debug > 2:
            print("arithstack:", end = " ")
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()

        # Execute as operator precedence
        for aa in ops_prec:
            reduce(self2, arithstack, aa)

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

    def start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.start()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.empty()
        arithstack.push(tprog)
        if pvg.opt_debug > 2:
            print("arithstack start:", end = " ")
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()

    def col(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.col()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def ident(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.ident()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def val(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.val()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def comma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.comma()", "tprog =", tprog)
        if pvg.opt_debug > 7:
            print("arithstack comma:", end = " ")
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()
        #if arithstack.getlen() <= 3:
        #    print("Padding ??? for zero fill", len(arithstack))

    def down(self, self2, tprog):

        if pvg.opt_debug > 1:
            print("decl.down()", "tprog =", tprog, self2.arrx[tprog])

        if pvg.opt_debug > 0:
            print("arithstack: len =", arithstack.getlen(), end = " ")
            for aa in arithstack:
                if self2.arrx[aa].flag == 0:
                    print(self2.arrx[aa], end = " ")
            print()

        # Nothing to see here
        if not arithstack.getlen():
            return

        datatype = self2.arrx[arithstack.get(0)].mstr
        asmtype = linpool.addtopool(self2, arithstack)
        if pvg.opt_debug > 3:
            print("datatype =", datatype, asmtype)

        strx =   self2.arrx[arithstack.get(2)].mstr + " : " + asmtype + " "

        # type dependent expand
        if self2.arrx[arithstack.get(0)].mstr == "arr":
            #print("arr type")
            if arithstack.getlen() <= 3:
                # patch missing declaration argument with zero /empty
                strx += "hello"
                pass
            else:
                strx +=  asmesc(self2.arrx[arithstack.get(4)].mstr)

        elif datatype.lower() in int_types:
            #print("int type")
            if arithstack.getlen() <= 4:
                # patch missing declaration argument with zero /empty
                strx += " 0 "
            else:
                strx +=  self2.arrx[arithstack.get(4)].mstr
        elif datatype.lower() in float_types:
            #print("float type")
            if arithstack.getlen() <= 3:
                # patch missing declaration argument with zero /empty
                strx += " 0 "
            else:
                strx +=  self2.arrx[arithstack.get(4)].mstr
        else:
            print("other type", datatype)
            # This is where type expnsion takes place
            if arithstack.getlen() <= 2:
                strx += " 0 "
            else:
                strx +=  self2.arrx[arithstack.get(4)].mstr

        #print("data decl:", pp(strx))

        # Output comment as well
        linex = self2.arrx[arithstack.get(0)].linenum + 1
        strx +=  " ; line: " + str(linex) + " -- "
        for aa in range(arithstack.getlen()):
            strx +=  self2.arrx[arithstack.get(aa)].mstr + " "
        strx += "\n"

        #if arithstack.getlen() <= 2:
        #    strx += " 0 "
        #else:
        #    strx += self2.arrx[arithstack.get(2)].mstr

        codegen.emitdata(strx)
        #arithstack.empty()

decl = Decl()

# ------------------------------------------------------------------------

class Misc():

    def space(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("misc.space()", "tprog =", tprog)

    def tab(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("misc.tab()", "tprog =", tprog)

    def nl(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("misc.nl()", "tprog =", tprog)

    def comment(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("misc.comment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )

    def dcomment(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("misc.dcomment()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
        if pvg.opt_rdocstr:
            print(self2.arrx[tprog].mstr[3:], end = "")

    def dcomment2(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("misc.dcomment2()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
        if pvg.opt_rdocstr:
            print(self2.arrx[tprog].mstr[3:-2], end = "")

    def dcomment3(self, self2, tprog):
        if pvg.opt_debug > 5:
            print("misc.dcomment3()", "tprog =", tprog, pp(self2.arrx[tprog].mstr) )
        if pvg.opt_rdocstr:
            print(self2.arrx[tprog].mstr[2:], end = "")

    def str(self, self2, idx, tprog):
        print("misc.str() idx =", idx, "tprog =", tprog, "iprog=", "slen =", len(stamps[idx][0]))
        if pvg.opt_debug > 5:
            prarr(self2.arrx[tprog:tprog], "func_str pre: ")
        sys.exit(0)

    def brace(self, self2, tprog):

        if pvg.opt_debug > 5:
            print("misc.brace", "tprog =", tprog, "iprog=")

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

    def parent(self, self2, tprog):

        if pvg.opt_debug > 3:
            print("misc.parent()", tprog, self2.arrx[tprog])

        if pvg.opt_debug > 5:
            prarr(self2.arrx, "func pre par feed:", True)

        arithstack.push(tprog)

        #self2._feed(tprog + 1, tprog - 1)
        #if pvg.opt_debug > 5:
        #    prarr(self2.arrx[tprog:tprog+1], "func post par feed:")

        #if pvg.opt_debug > 6:
        #    prarr(self2.arrx, "func paren post:", True)

misc = Misc()

class Fdecl():

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


# EOF
