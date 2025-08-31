#!/usr/bin/env python3
#

import os, sys, subprocess

''' Codegen '''

#///////////////////////////////////////////////////////////////////////////
#//
#// Code generator for FASM output
#//
#// Automatically generated, will be overwritten.
#//

prolstr = '''\
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n\
;                                                                         \n\
;   Compile with NASM                                                     \n\
;                                                                         \n\
;   Automatically generated, will be overwritten.                         \n\
;                                                                         \n\
                                                                          \n\
        global main                                                       \n\
        extern printf                                                     \n\
        section .text                                                     \n\
        bits 64

%include "codegen/crt.inc"

 main:


'''

epilstr = '''
   \nenc_code:\n    ;End of program\n\n

    mov     rdi, endx
    call    printf
    ret
    ret

section .data
format:    db      "Hello world", 10, 0
endx:      db      "End program.", 10, 0

'''

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
    if lpg.opt_verbose.cnt:
        print("assemble:",  linprog)
    try:
        ret = subprocess.Popen(linprog, stdout=subprocess.PIPE)
        res = ret.wait()
    except:
        print("assemble", sys.exc_info())

def link(fname, lpg):

    objname = os.path.splitext(fname)[0] + ".o"
    outname = os.path.splitext(fname)[0]
    linprog = ["ld", objname, "codegen/main.o", "codegen/crtasm.o",
                "-o", outname, "-dynamic-linker",
                "/lib64/ld-linux-x86-64.so.2", "-lc", ]
    if lpg.opt_verbose.cnt:
        print("link:",  linprog)
    try:
        ret = subprocess.Popen(linprog, stdout=subprocess.PIPE)
        res = ret.wait()
    except:
        print("link", sys.exc_info())

def output(fname, contents, datax = ""):

    #print("outfile:", fname)

    fp = open(fname, "w")
    fp.write(prolstr)
    fp.write(contents)
    fp.write(epilstr)
    fp.write(datax)
    fp.close()

xcode = '''

    main:
        ;mov     rax, 0
        ;mov     rax, [ rax ]

        mov     rdi, format
        call    printf

        ret

    '''
xdata = '''
    format:    db      "Hello world", 10, 0
'''

if __name__ == "__main__":
    #print ("This module was not meant to operate as main.")
    print(prolstr)
    print(epilstr)

# EOF
