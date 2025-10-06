#!/usr/bin/env python

''' Functions for the lin parser, to call on stamp match '''

import complib.stack as stack
import complib.linpool as linpool
import complib.lexdef as lexdef
import codegen.codegen as codegen

#import complib.lindef as lindef

# End it with empty "" operator for cleanup
#ops_prec = "**", "*", "/", "%", "+", "-", ">>", "<<", "=", ""
ops_prec = "*","+", ""

int_types = "u64", "s64", "u32", "s32", "u16", "s16", "u8", "s8",
float_types = "float", "double", "quad"

numtypes = "float", "double", "quad", "decl"
numvals = "num", "num2"

try:
    from complib.utils import *
except:
    from utils import *

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

# Stack definitions

inststack  = stack.pStack(name='inststack')       # Instructions
arithstack = stack.pStack(name='arithstack')      # Arithmetic
argstack   = stack.pStack(name='argstack')        # Function arguments
callstack  = stack.pStack(name='callstack')       # Function calls
extstack   = stack.pStack(name='extstack')        # External definitions
scopestack = stack.pStack(name='scopestack')      # Inside function scope
funcstack  = stack.pStack(name='funcstack')       # Function name definitions
stackstack = stack.pStack(name='stackstack')      # Stack of stacks

currptr =  arithstack

def initall():
    arithstack.empty()
    argstack.empty()
    callstack.empty()
    extstack.empty()
    funcstack.empty()
    scopestack.empty()
    scopestack.push("")    # Empty (global) scope

    stackstack.empty()
    global  currptr
    currptr =  arithstack
    stackstack.push(currptr)

def emitstack(self2, xstack, xcontext):

    ''' Parse stack for instructions, output assembly '''

    argcnt = 0
    strxx = "" ; datax = "" ; typey = "" ; typex = "" ;
    statex = 0; lab = "" ; val = "" ; linenum = 0; orgline = 0
    for aa in xstack:
        if "parse" in pvg.opt_ztrace:
            print("parse: [", xcontext, "] state:",
                statex, "tok:", pp(self2.arrx[aa].stamp.xstr), "type:", typey,
                        "lab:", lab, "val:", val)
        if statex == 0:
            #if self2.arrx[aa].stamp.xstr == "decl":
            if self2.arrx[aa].stamp.xstr in numtypes:
                statex = 1
                typey = self2.arrx[aa].mstr
                typex = linpool.pctona(self2.arrx[aa].mstr)
            if self2.arrx[aa].stamp.xstr == "ident":
                statex = 4
                orgline =  self2.arrx[aa].linenum
                val = ""
                lab = scopestack.peek() + self2.arrx[aa].mstr
        elif statex == 1:
            if self2.arrx[aa].stamp.xstr == "ident":
                lab = scopestack.peek() + self2.arrx[aa].mstr
                statex = 2
        elif statex == 2:
            if self2.arrx[aa].stamp.xstr == "ident":
                linpool.add2pool(self2, typey, lab, val, linenum)
                datax += lab + " : " + typex + " "  + " 0 " + \
                        "; line: " + str(orgline+1) + \
                        " generated from " + pp(lab) + "\n"
                #print("      ", "type:", typey, "lab:", lab, "val:", val)
                statex = 1
            if self2.arrx[aa].stamp.xstr == "=":
                statex = 3
        elif statex == 3:
            val = self2.arrx[aa].mstr
            linenum = self2.arrx[aa].linenum
            linpool.add2pool(self2, typey, lab, val, linenum)
            if typey.lower() in int_types:
                if xcontext == "args_end":
                    strxx += "    %define " + lab + " rbp + %d " % (argcnt * 8) + "\n" # + \
                       # " ; -- args " + lab + "\n"
                    argcnt += 1
                elif xcontext == "instr":
                    strxx +=  "    %define " + lab + " rbp + %d " % (argcnt * 8) + "\n" # + \
                       # " ; -- args " + lab + "\n"
                else:
                    print("def context")

            elif typey.lower() in float_types:
                datax +=  lab + " : " + typex + " " + val
            else:
                error(self2, "No type specified", )
            statex = 0
            val = 0 ; lab = "" ; typex = "" ; typey = ""
        elif statex == 4:
            if self2.arrx[aa].stamp.xstr == "num" or \
                    self2.arrx[aa].stamp.xstr == "ident":
                state = 0
                tpi = linpool.lookpool(self2, lab)
                if not tpi:
                    error(self2, "Undefined variable: '%s'" % lab)
                typex = linpool.pctona(tpi.typex)
                typey = tpi.typex
                val = self2.arrx[aa].mstr
                # output assn opeartion
                ttt = linpool.pctocast(typey)
                strxx += "    mov   " + ttt + " [" + lab + "], " + val + \
                         "; line: " + str(orgline+1) + \
                          " generated from " + pp(lab) + "\n"
                statex = 0
        else:
            pass
            print("Warn: invalid state", __file__, __line__)

    if statex == 1:
        # State machine left this incomplete
        print("left over:", lab, typex, val)
        datax += self2.arrx[aa].mstr + " : " + typex + " 0 " + "; line: " \
                                    + str(self2.arrx[aa].linenum+1) \
                                    + " -- generated from " \
                                    + self2.arrx[aa].mstr + "\n"
    return strxx, datax

class   FuncCall():

    def start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call.start()", pp(self2.arrx[tprog].mstr))
        if pvg.opt_debug > 5:
            print("func arithstack: len =", arithstack.getlen(), end = " ")
            for aa in arithstack:
                print(self2.arrx[aa], end = " ")
            print()
        argstack.empty()
        callstack.empty()
        callstack.push(arithstack.pop())

    def val(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call.decl_val()", self2.arrx[tprog])
        #argstack.push(tprog)

    def comma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call.decl_comma()", self2.arrx[tprog])

    def end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("call.end()", pp(self2.arrx[tprog].mstr))

        if pvg.opt_debug > 6:
            dumpstack(self2, callstack)
            dumpstack(self2, argstack)

        if pvg.opt_debug > 6 or "arith" in pvg.opt_ztrace:
            dumpstack(self2, arithstack)

        idx  =   callstack.get(0)
        funcname =  self2.arrx[idx].mstr
        linex = self2.arrx[idx].linenum + 1

        estr = ""
        # Exception on printf stack call
        if funcname == "printf":
            estr += "    and    rsp, 0xfffffffffffffff0 ; align 16 stack\n"
            estr += "    mov    rbp, rsp\n"
        else:
            # Check prototype
            pass

        cnt = 0; tpi = None
        for aa in argstack:
            if pvg.opt_debug > 7:
                print("arg:", self2.arrx[aa].stamp.xstr, self2.arrx[aa].mstr)
            tpi = linpool.lookpool(self2, self2.arrx[aa].mstr)
            if self2.arrx[aa].stamp.xstr == "ident":
                if not tpi:
                    error(self2, "Undefined variable '%s'" % self2.arrx[aa].mstr)
            elif self2.arrx[aa].stamp.xstr == "str":
                if not tpi:
                    # Generate entry for immidiate variable
                    uuu = "str_%d" % unique()
                    strx =  uuu + " : db " + asmesc(self2.arrx[aa].mstr) + "\n"
                    linpool.add2pool(self2, self2.arrx[aa].stamp.xstr,
                                                uuu, self2.arrx[aa].mstr, linex)
                    tpi = linpool.lookpool(self2, uuu)
                    codegen.emitdata(strx)

            elif self2.arrx[aa].stamp.xstr == "num":
                if not tpi:
                    # Generate entry for immidiate variable
                    uuu = "num_%d" % unique()
                    linpool.add2pool(self2, self2.arrx[aa].stamp.xstr,
                                                uuu, int(self2.arrx[aa].mstr),
                                                int(self2.arrx[aa].linenum))
                    tpi = linpool.lookpool(self2, uuu)
                    # We do not need this number in memory :-)
                    #strx =  uuu + " : dq " + asmesc(self2.arrx[aa].mstr) + "\n"
                    #codegen.emitdata(strx)
            elif self2.arrx[aa].stamp.xstr in int_types:
                print("call ints")
            elif self2.arrx[aa].stamp.xstr in float_types:
                print("call float")
            else:
                print("Unkown type", self2.arrx[aa].stamp.xstr)
                pass

            if cnt  >= len(codegen.regorder) - 1:
                error(self2, "Too many arguments to function: '%s'" % funcname )
                pass
            # Skip first arg as syscall opcode is in rax # ????
            # Expand types
            if tpi.typex == "str":
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov    " + codegen.regorder[cnt+1]
                    estr += "  , " + tpi.namex  + "\n"
            elif  tpi.typex == "num" :
                estr += "    mov   rax, " + str(self2.arrx[aa].ival) + "\n"
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                                ", rax\n"
            elif  tpi.typex == "u32" or tpi.typex == "s32" :
                estr += "    mov   rax, 0\n"
                estr += "    mov   ax, word [" + self2.arrx[aa].mstr + "]\n"
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                             ", [" + self2.arrx[aa].mstr + "]\n"
            elif  tpi.typex == "u16" or tpi.typex == "s16":
                estr += "    mov   rax, 0\n"
                estr += "    mov   ax, word [" + self2.arrx[aa].mstr + "]\n"
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                                    ", rax\n"
            elif  tpi.typex == "u8" or tpi.typex == "s8":
                estr += "    mov   rax, 0\n"
                estr += "    mov   al, byte [" + self2.arrx[aa].mstr + "]\n"
                if cnt  >= len(codegen.regorder) - 1:
                    estr += "    push   rax \n"
                else:
                    estr += "    mov  " + codegen.regorder[cnt+1] + "  " + \
                                     ", rax\n"
            else:
                print("Unkown type:", tpi.typex)
            cnt += 1

        estr += "    xor    rax, rax" + "\n"
        #print("estr =\n", estr)

        estr += "    extern " +  funcname + "\n"
        estr += "    call   " +  funcname
        estr +=  " ; line:  " + str(linex + 1) + " -- " + funcname + "\n"
        codegen.emit(estr)

        # Finally, output return assignments
        if len(arithstack) >= 6:
            #dumpstack(self2, arithstack)
            if self2.arrx[arithstack[1]].mstr == "=":
                xstr = "    mov [ " + \
                        self2.arrx[arithstack[0]].mstr + " ] " + \
                        ", rax " + \
                        "; line: " + str(linex + 1) + "\n"
                codegen.emit(xstr)

fcall = FuncCall()

class   Funcs():

    def start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.start()", pp(self2.arrx[tprog]))
        argstack.empty()
        funcstack.empty()
        inststack.empty()
        funcstack.push(tprog)
        scopestack.push(self2.arrx[tprog].mstr + "_")
        #print("scopestack:", pp(scopestack.peek()) )

    def startbody(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.startbody()", pp(self2.arrx[tprog]))
        global currptr
        stackstack.push(currptr)
        currptr = inststack

    def additem(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.additem()", pp(self2.arrx[tprog]))

    def initval(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.initval()", pp(self2.arrx[tprog]))

    def enter(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.enter()", "tprog =", tprog, self2.arrx[tprog])
        #arithstack.push(tprog)

    def enter_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.enter_end()", "tprog =", tprog, self2.arrx[tprog])
        #arithstack.push(tprog)

    def leave(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.leave()", "tprog =", tprog, self2.arrx[tprog])
        #arithstack.push(tprog)

    def leave_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.leave_end()", "tprog =", tprog, self2.arrx[tprog])
        #arithstack.push(tprog)

    def args_start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.args_start()", pp(self2.arrx[tprog]))
        scopestack.push(scopestack.peek() + "arg_")
        if pvg.opt_debug > 3:
            print("scopestack:", scopestack.dump())
        global currptr
        stackstack.push(currptr)
        currptr = argstack
        #print("currptr:", print_id(currptr))

    def args_end(self, self2, tprog):

        if pvg.opt_debug > 1:
            print("funcs.args_end()", pp(self2.arrx[tprog]))

        ccc, ddd = emitstack(self2, argstack, "args_end")

        if "emit" in pvg.opt_ztrace:
            print("args emit got:\n", ccc, ddd)

        # Restore stack
        stackstack.pop()
        global currptr
        currptr = stackstack.peek()
        scopestack.pop()

    def ret_start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.ret()", "tprog =", tprog, self2.arrx[tprog])
        #global currptr
        #stackstack.push(currptr)
        #currptr = inststack
        #currptr.push(tprog)

    def ret_id(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.ret_id()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def ret_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.ret_end()", "tprog =", tprog, self2.arrx[tprog])
        global currptr
        statckstack.pop()
        currptr = stackstack(peek())

    def endbody(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("funcs.endbody()", pp(self2.arrx[tprog]))

        if pvg.opt_debug > 4 or "arith" in pvg.opt_ztrace:
            dumpstack(self2, funcstack)
            dumpstack(self2, argstack)
            dumpstack(self2, inststack)

        #print("scopestack:", scopestack.dump())
        fff = self2.arrx[funcstack.peek()]
        strx = fff.mstr + ": ; Function '" + fff.mstr + "'\n"

        # Prologue
        strx += "    push    rbp\n"
        strx += "    mov     rbp, rsp\n"
        strx += "\n    ; line: %d -- Function body\n\n" % \
                                    (self2.arrx[tprog].linenum + 1)
        codegen.emit(strx)

        # Actual code
        ccc, ddd = emitstack(self2, inststack, "instr")
        if "emit" in pvg.opt_ztrace:
            print("code emit got:", ccc)
            print("data emit got:", ddd)

        codegen.emit(ccc)
        codegen.emitdata(ddd)

        # Epilogue
        strx =  "    mov     rsp, rbp\n"
        strx += "    pop     rbp\n"
        strx += "    ret\n"
        codegen.emit(strx)

        scopestack.pop()
        #print("scopestack:", scopestack.dump())

        global currptr
        stackstack.pop()
        currptr = stackstack.peek()
        #print(currptr)

funcs = Funcs()

class Arith():

    def arith_stop(self, self2, tprog):

        if pvg.opt_debug > 1:
            print("arith.arith_stop()", "tprog =", tprog, self2.arrx[tprog])

        if pvg.opt_debug > 6 or "arith" in pvg.opt_ztrace:
            dumpstack(self2, arithstack, eol="\n", label="arith stop:")

        # Execute as operator precedence
        for aa in ops_prec:
            linpool.reduce(self2, currptr, aa)

        if pvg.opt_debug > 6 or "arith" in pvg.opt_ztrace:
            dumpstack(self2, currptr, eol="\n",
                                    label="arith stop post:", active=True)

    def arithstart(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.arithstart()", "tprog =", tprog, self2.arrx[tprog])
        #currptr.empty()
        currptr.push(tprog)

    def arithop(self, self2, tprog):
        #if pvg.opt_debug > 1:
        #    print("arith.arithop()", "tprog =", tprog, self2.arrx[tprog])
        if pvg.opt_debug > 5:
            print("arith.arithop()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def addexpr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.addexpr()", "tprog =", tprog, self2.arrx[tprog])
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("arith.addexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        currptr.push(tprog)

    def subexpr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.subexpr()", "tprog =", tprog, self2.arrx[tprog])
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("arith.subexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        currptr.push(tprog)

    def divexpr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.divexpr()", "tprog =", tprog, self2.arrx[tprog])
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("arith.divexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        currptr.push(tprog)

    def expexpr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.expexpr()", "tprog =", tprog, self2.arrx[tprog])
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("arith.expexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        currptr.push(tprog)

    def mulexpr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.mulexpr()", "tprog =", tprog, self2.arrx[tprog])

        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("misc.mulexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        currptr.push(tprog)

    def assnexpr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.assnexpr()", "tprog =", tprog, self2.arrx[tprog])
        if pvg.opt_debug > 5:
            tprog2 = arithstack.peek()
            print("assnexpr: ",
                    "tprog  =", tprog,  self2.arrx[tprog],
                    "tprog2 =", tprog2, self2.arrx[tprog2] )
        currptr.push(tprog)

    def expr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.expr()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def eqeq_start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.eqeq_start()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def eqeq(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.eqeq()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def orx_start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.orx_start()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def orx(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("arith.orx()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

arith = Arith()

# ------------------------------------------------------------------------

class RAssn():

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

    def rassn_start(self2, tprog):
        if pvg.opt_debug > 1:
            print("assn_start()", "tprog =", tprog, self2.arrx[tprog])
        #arithstack.empty()
        arithstack.push(tprog)

    def rassn_assn(self2, tprog):
        if pvg.opt_debug > 1:
            print("rassn_assn()", "tprog =", tprog, self2.arrx[tprog])
        arithstack.push(tprog)

    def rassn_stop(self2, tprog):
        if pvg.opt_debug > 1:
            print("rassn_stop()", "tprog =", tprog)
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

        #print("tpi:", tpi, self2.arrx[arithstack.get(0)],
        #                    self2.arrx[arithstack.get(2)])

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

assn = RAssn()

class Adecl():

    def astart(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.astart()", "tprog =", tprog, self2.arrx[tprog])
        currptr.empty()

    def aident(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.aident()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def aequ(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.aeq()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def astr(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.astr()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def amul(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.amul()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def anum(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.anum()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def aadd(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.aadd()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def acol(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.acol()", "tprog =", tprog, self2.arrx[tprog])

    def aeq(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.aeq()", "tprog =", tprog, self2.arrx[tprog])

    def acomma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("adecl.acomma()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def adown(self, self2, tprog):

        if pvg.opt_debug > 1:
            print("adecl.adown()", "tprog =", tprog, self2.arrx[tprog])

        #if pvg.opt_debug > 6  or "arith" in pvg.opt_ztrace:
        #    dumpstack(self2, arithstack, label="adown:")

        strx = "" ; statex = 0; lab = "" ; val = "" ; linenum = 0;
        for aa in currptr:
            if statex == 0:
                if self2.arrx[aa].stamp.xstr  == "ident":
                    statex = 1
                    lab = self2.arrx[aa].mstr
                    linenum = self2.arrx[aa].linenum
            elif statex == 1:
                if self2.arrx[aa].stamp.xstr  == "str":
                    statex = 2
                    #val = asmesc(self2.arrx[aa].mstr)
                    val = self2.arrx[aa].mstr
            elif statex == 2:
                if self2.arrx[aa].stamp.xstr  == "+":
                    statex = 3
                elif self2.arrx[aa].stamp.xstr  == "*":
                    statex = 4
                else:
                    linpool.add2pool(self2, "str", lab, val, linenum)
                    strx += lab + ": db "
                    strx += asmesc(val)  + "\n"
                    statex = 0
            elif  statex == 3:
                val = val[0] + val[1:-1] + self2.arrx[aa].mstr[1:-1] + val[-1]
                statex = 0
            elif  statex == 4:
                if pvg.opt_debug > 6:
                    print("val:", val)
                val = val[0] + val[1:-1] * self2.arrx[aa].ival + val[-1]
                statex = 0
            else:
                print("invalid state", __line__)

        linpool.add2pool(self2, "str", lab, val, linenum)
        strx +=  lab + ": db "
        strx +=  asmesc(val)  + "\n"

        codegen.emitdata(strx)

adecl = Adecl()

class Decl():

    def start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.start()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def col(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.col()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def ident(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.ident()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def val(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.val()", "tprog =", tprog, self2.arrx[tprog])
        currptr.push(tprog)

    def comma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("decl.comma()", "tprog =", tprog, self2.arrx[tprog])
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
        currptr.push(tprog)

decl = Decl()

class Loop():

    def start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("loop.start()", "tprog =", tprog)

    def enter(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("loop.enter()", "tprog =", tprog)

    def enter_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("loop.enter_end()", "tprog =", tprog)

    def leave(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("looop.leave()", "tprog =", tprog)

    def leave_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("looop.leave_end()", "tprog =", tprog)

    def end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("looop.end()", "tprog =", tprog)

    def breakx(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("looop.break()", "tprog =", tprog)

loop = Loop()

# ------------------------------------------------------------------------

class Exter():

    def extern(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.extern()", "tprog =", tprog)
        extstack.empty()

    def dbldwn(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.dbldwn()", "tprog =", tprog)
        #extstack.empty()
        if pvg.opt_debug > 3 or "arith" in self.pvg.opt_ztrace:
            dumpstack(self2, arithstack)

    def extadd(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.extadd()", "tprog =", tprog)
        extstack.push(tprog)

    def extcomma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.extcomma()", "tprog =", tprog)

    def exdn(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.extdn()", "tprog =", tprog)
        strx = ""
        for aa in extstack:
            #print("extstack:", self2.arrx[aa].mstr, self2.arrx[aa].stamp.xstr)
            if self2.arrx[aa].stamp.xstr == "str":
                strx += "extern " + self2.arrx[aa].mstr[1:-1]
            else:
                strx += "extern " + self2.arrx[aa].mstr
            strx += " ; line: %d -- " % (self2.arrx[aa].linenum + 1)
            strx += " extern " + self2.arrx[aa].mstr + "\n"
        codegen.emit(strx)

        # ----------------------------------------------------------------------

    def glob(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.global()", "tprog =", tprog)
        extstack.empty()

    def gndwn(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.gndwn()", "tprog =", tprog)
        #extstack.empty()
        if pvg.opt_debug > 3 or "arith" in self.pvg.opt_ztrace:
            dumpstack(self2, arithstack)

    def globadd(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.globadd()", "tprog =", tprog)
        extstack.push(tprog)

    def globcomma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.globcomma()", "tprog =", tprog)

    def gldn(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.gldn()", "tprog =", tprog)
        strx = ""
        for aa in extstack:
            #print("extstack:", self2.arrx[aa].mstr, self2.arrx[aa].stamp.xstr)
            if self2.arrx[aa].stamp.xstr == "str":
                strx += "global " + self2.arrx[aa].mstr[1:-1]
            else:
                strx += "global " + self2.arrx[aa].mstr
            strx += " ; line: %d -- " % (self2.arrx[aa].linenum + 1)
            strx += " global " + self2.arrx[aa].mstr + "\n"
        codegen.emit(strx)

    # ----------------------------------------------------------------------

    def assem(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.assem()", "tprog =", tprog)
        extstack.empty()

    def gndwn(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.gndwn()", "tprog =", tprog)
        #extstack.empty()
        if pvg.opt_debug > 3 or "arith" in self.pvg.opt_ztrace:
            dumpstack(self2, arithstack)

    def asmadd(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.asmadd()", "tprog =", tprog)
        extstack.push(tprog)

    def asmcomma(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.asmcomma()", "tprog =", tprog)

    def asmdn(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.asmdn()", "tprog =", tprog)
        strx = ""
        for aa in extstack:
            #print("extstack:", self2.arrx[aa].mstr, self2.arrx[aa].stamp.xstr)
            if self2.arrx[aa].stamp.xstr == "str":
                strx += "asm " + self2.arrx[aa].mstr[1:-1]
            else:
                strx += "asm " + self2.arrx[aa].mstr
            strx += " ; line: %d -- " % (self2.arrx[aa].linenum + 1)
            strx += " asm " + self2.arrx[aa].mstr + "\n"
        codegen.emit(strx)

    def asm_start(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.asmstart()", "tprog =", tprog)

    def asm_item(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.asm_item()", "tprog =", tprog, self2.arrx[tprog])

    def asm_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("exter.asm_end()", "tprog =", tprog)

exter = Exter()

class Misc():

    def ifx(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("misc.ifx()", "tprog =", tprog)

    def elifx(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("misc.elifx()", "tprog =", tprog)

    def elifx_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("misc.elifx_end()", "tprog =", tprog)

    def if_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("misc.if_end()", "tprog =", tprog)
    def if_body_end(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("misc.if_body_end()", "tprog =", tprog)

    def space(self, self2, tprog):
        if pvg.opt_debug > 8:
            print("misc.space()", "tprog =", tprog)
        self2.arrx[tprog].flag = 1

    def tab(self, self2, tprog):
        if pvg.opt_debug > 8:
            print("misc.tab()", "tprog =", tprog)
        self2.arrx[tprog].flag = 1

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

        if pvg.opt_debug > 1:
            print("misc.parent()", tprog, self2.arrx[tprog])

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
            if self2.arrx[tprog + uprog].flag:
                uprog += 1
                continue
            if "num" == self2.arrx[tprog + uprog].stamp.xstr:
                break
            uprog += 1

        #print("num[", uprog, self2.arrx[tprog + uprog][2])
        startx = uprog
        ttt =  self2.arrx[tprog + uprog]
        # Skip till operator
        while 1:
            #if uprog >= iprog: return
            if self2.arrx[tprog + uprog].flag:
                uprog += 1
                continue
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
        if pvg.opt_debug > 1:
            print("mul() tprog =", tprog)
        if pvg.opt_debug > 3:
            prarr(self2.arrx[tprog:tprog], "mul pre: ")
        #_func_arith(self2, "*", tprog)
        #if pvg.opt_debug > 5:
        #    prarr(self2.arrx[tprog:tprog], "mul post: ")

    def func_add(self, self2, tprog):
        if pvg.opt_debug > 1:
            print("add() tprog =", tprog)
        if pvg.opt_debug > 6:
            prarr(self2.arrx[tprog:tprog], "add pre: ")
        #_func_arith(self2, "+", tprog)
        #if pvg.opt_debug > 6:
        #    prarr(self2.arrx[tprog:tprog], "add post: ")

# EOF
