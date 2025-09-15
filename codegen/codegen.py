#!/usr/bin/env python3

import os, sys, subprocess

'''  Code generator for FASM output '''

cummulate  = ""
cummulate2 = ""

# ABI 64 bit
regorder = ( "rax", #arg0
             "rdi", #arg1
             "rsi", #arg2
             "rdx", #arg3
             "rcx", #arg4
             # ???? "r10", #arg4
             "r8",  #arg5
             "r9",  #arg6
            )
reglist = ( "rax", #arg0
            )

prolstr = '''\
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n\
;                                                                         \n\
;   Compile with NASM                                                     \n\
;                                                                         \n\
;   Automatically generated, will be overwritten.                         \n\
;                                                                         \n\
        extern  printf                                                    \n\
        extern  fflush                                                    \n\
        extern  exit                                                      \n\
        global main                                                       \n\
        bits 64

%include "codegen/crt.inc"

section .text                                                     \n\

main:

    push    rbp
    mov     rbp, rsp

    ;call    _print_regs
    ;mov     rdi, hellodef
    ;and     rsp, 0xfffffffffffffff0
    ;call    printf

'''

epilstr = '''
end_code:    ;  End of program\n
    ; This is just in case of no exit statement
    ;xor     rax,rax
    ;mov     rdi, endx
    ;and     rsp, 0xfffffffffffffff0
    ;call    printf

    ; Flush stdout, in case of missing terminating newline
    mov     rdi, 0
    call    fflush

    ; Exit here
    ;mov     qword [exit_code], 44   ; test exit code
    mov     rdi, [exit_code]
    call    exit

    ; return value -> exit code
    mov     rax, 0

    mov     rsp, rbp
    pop     rbp

    ret

section .data

exit_code   dq      0
hellodef:   db      "Start program", 10, 0
endx2:      db       "End program.", 10, 0
endx:       db      10, 0

'''

endstr = '''
; EOF
'''

def emit(*argx):

    ''' Accumulate TEXT output '''

    global cummulate;
    for strx in argx:
        cummulate += strx
    cummulate += "\n"

def emitdata(*argx):

    ''' Accumulate DATA output '''

    global cummulate2;
    for strx in argx:
        cummulate2 += strx
    cummulate2 += "\n"

def show_emit():
    print("emit code results:")
    print(cummulate)
    print("emit data results:")
    print(cummulate2)


# ------------------------------------------------------------------------

def isnewer(targ, *file2):

    ''' return True if file does not exist or ...
       modify time is newer  '''

    #print("isnewer:", targ, file2)
    retx = False; targinfo = 0; statinfo2 = 0
    while True:
        #print("targ file:", targ)
        try: targinfo = os.stat(targ)
        except:
            #print("warn: no targ file", targ, targ, sys.exc_info())
            return True
        for aaa in file2:
            try : statinfo2 = os.stat(aaa)
            except:
                #print("warn: no test file:", aaa, sys.exc_info())
                return True
            #print("isnewer cmp:", retx, targinfo.st_mtime, statinfo2.st_mtime)
            if targinfo.st_mtime < statinfo2.st_mtime:
                retx |= True
                break
            break
        break

    return retx

def dep_assemble(lpg):

    ''' Conditionally greate CRT objects '''

    depnames = "codegen/crt.inc",
    fnames = "codegen/main.inc", "codegen/crtasm.inc"
    for fname in fnames:
        oname = os.path.splitext(fname)[0] + ".o"
        if not isnewer(oname, fname, *depnames):
            continue
        if lpg.opt_verbose:
            print("create crt:", fname, oname)
        linprog = ["nasm", "-felf64", "-Icodegen", fname, "-o", oname]
        try:
            ret = subprocess.Popen(linprog, stdout=subprocess.PIPE)
            ret.wait()
        except:
            print("err on assemble", fname, sys.exc_info())

def assemble(fname, lpg):

    outname = os.path.splitext(fname)[0] + ".o"

    linprog = ["nasm", "-felf64", fname, "-o", outname]
    if lpg.opt_verbose.cnt > 2:
        print("assemble:",  linprog)
    try:
        ret = subprocess.Popen(linprog, stdout=subprocess.PIPE)
        res = ret.wait()
    except:
        print("assemble", sys.exc_info())

def link(fname, outname, lpg):

    objname = os.path.splitext(fname)[0] + ".o"
    linprog = ["ld", objname, "codegen/main.o", "codegen/crtasm.o",
                "-o", outname, "-dynamic-linker",
                "/lib64/ld-linux-x86-64.so.2", "-lc"]
    if lpg.opt_verbose.cnt > 2:
        print("link:",  linprog)
    try:
        ret = subprocess.Popen(linprog, stdout=subprocess.PIPE)
        res = ret.wait()
    except:
        print("link", sys.exc_info())

def output(fname, codex, datax):

    #print("outfile:", fname)
    fp = open(fname, "w")
    fp.write(prolstr)
    fp.write(codex)
    fp.write(epilstr)
    fp.write(datax)
    fp.write(endstr)
    fp.close()

if __name__ == "__main__":
    #print ("This module was not meant to operate as main.")
    print(prolstr)
    print(epilstr)
    print(endstr)
# EOF
