#!/usr/bin/env python3
#

import os, subprocess

''' Codegen '''

#///////////////////////////////////////////////////////////////////////////
#//
#// Code generator for FASM output
#//

prolstr = '''\
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n\
;                                                                         \n\
;   Compile with NASM                                                     \n\
;                                                                         \n\
                                                                          \n\
        global main                                                       \n\
        extern printf                                                     \n\
        section .text                                                     \n\
        bits 64

%include "codegen/crt.inc"

'''

epilstr = '''
   \nenc_code:\n    ;End of program\n\n

section .data
'''

def dep_assemble():

    ''' Conditionally greate CRT objects '''

    fnames = "codegen/main.inc", "codegen/crtasm.inc"
    for fname in fnames:
        oname = os.path.splitext(fname)[0] + ".o"
        if not os.path.isfile(oname):
            print("create:", fname, oname)
            linprog = ["nasm", "-felf64", "-Icodegen", fname, "-o", oname]
            try:
                ret = subprocess.Popen(linprog, stdout=subprocess.PIPE)
                ret.wait()
            except:
                print("assemble", sys.exc_info())

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

def output(fname, contents, datax):

    #print("outfile:", fname)

    fp = open(fname, "w")
    fp.write(prolstr)
    fp.write(contents)
    fp.write(epilstr)
    fp.write(datax)
    fp.close()

if __name__ == "__main__":
    #print ("This module was not meant to operate as main.")
    print(prolstr)
    print(epilstr)

# EOF
