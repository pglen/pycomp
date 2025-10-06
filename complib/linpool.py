#!/usr/bin/env python

''' syntab functions for the lin parser '''

import complib.stack as stack
import complib.linfunc  as linfunc

try:
    from complib.utils import *
except:
    from utils import *

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

gpool = stack.pStack()                 # Symtab pool

def addtopool(self2, xstack, nameoff = 0, typeoff = 1):

    ''' Add to global pool -- parse stack / symbol lookup table '''

    typename = self2.arrx[xstack.get(0)].mstr
    varname = self2.arrx[xstack.get(2)].mstr
    if  xstack.getlen() > 4:
        varval = self2.arrx[xstack.get(4)].mstr
    else:
        varval = 0

    print("addto:", self2.arrx[xstack.get(2)])

    linenum = self2.arrx[xstack.get(2)].linenum
    colnum = self2.arrx[xstack.get(2)].lineoffs

    ret = add2pool(self2, typename, varname, varval, linenum, colnum)
    return ret

def add2pool(self2, typename, varname, varval, linenum):

    if pvg.opt_debug > 7  or "pool" in pvg.opt_ztrace:
        print("addtopool:", "type:", pp(typename),
                        "var:", pp(varname), "val:", pp(varval))
    for aa in gpool:
        if aa.namex == varname:
            if pvg.opt_debug > 3:
                print("Dumping pool:")
                for aa in gpool:
                    print(" pool:", aa)
            error(self2, "Duplicate definition (from line: %d) " % (aa.linenumx + 1))
            sys.exit(1)

    tpi = TypI(typename, varname, varval, linenum)
    gpool.push(tpi)
    datatype = pctona(typename)
    return datatype

def showpool(self2):
    for aa in gpool:
        print(aa)

def lookpool(self2, varname):

    ''' Get symbol from name '''
    ret = None
    for aa in gpool:
        if pvg.opt_debug > 7:
            print("lookpool:", "'" + aa.namex + "'")
        if aa.namex == varname:
            ret = aa
            break
    return ret

def emptypool():
    gpool.empty()

def pctona(ddd):

    ''' Transform data type string to assembler equivalent '''
    #print("pctona:", ddd)
    retx = "db"
    if ddd == "u8" or ddd == "s8":
        retx = "db"
    elif ddd == "arr":
        retx = "db"
    elif ddd == "u16" or ddd == "s16":
        retx = "dw"
    elif ddd == "u32" or ddd == "s32":
        retx = "dd"
    elif ddd == "u64" or ddd == "u64":
        retx = "dq"
    elif ddd == "float":
        retx = "dd"
    elif ddd == "double":
        retx = "dq"
    elif ddd == "quad":
        retx = "dt"
    return retx

def pctocast(ddd):

    ''' Transform data type string to assembler equivalent '''
    #print("pctona:", ddd)
    retx = "db"
    if ddd == "arr":
        retx = "byte"
    elif ddd == "u8" or ddd == "s8":
        retx = "byte"
    elif ddd == "u16" or ddd == "s16":
        retx = "word"
    elif ddd == "u32" or ddd == "s32":
        retx = "dword"
    elif ddd == "u64" or ddd == "u64":
        retx = "qword"
    elif ddd == "float":
        retx = "float"
    elif ddd == "double":
        retx = "double"
    elif ddd == "quad":
        retx = "quad"
    return retx

class TypI:

    ''' Global type structure '''

    def __init__(self, typex, namex, valx, linenumx, colx = 0):
        self.typex = typex
        self.namex = namex
        self.valx = valx
        self.linenumx = linenumx
        self.colx = colx

    def __str__(self):
        return str(self.typex) + " : " + str(self.namex) + \
                " = " + str(self.valx) + " -- line: " + \
                str(self.linenumx) + " : " + str(self.colx)

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

def test_pool():

    class testx():
        def __init__(self):
            self.arrx = []
    self2 = testx()
    xstack =  stack.pStack()

    # Syntesize array of tokens
    import complib.lexdef as lexdef
    ss = lexdef.LexI(lexdef.StI(lexdef.xtokens[0]), "test")
    rr = lexdef.LexI(lexdef.StI(lexdef.xtokens[1]), "test2")
    self2.arrx.append(ss) ; self2.arrx.append(rr)
    xstack.push(0) ; xstack.push(1)

    ret = addtopool(self2, xstack)
    #print(ret)
    assert ret == "dq"
    ret = lookpool(self2, "test2")
    #print("'" + str(ret) + "'")
    assert "test : test2 = 0" == str(ret)

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

    if pvg.opt_debug > 4:
        print(" execop:", arg1, op, arg2, "; ret = ", ret, )

    return ret

def reduce(self2, xstack, filter, pos = 0):

    if pvg.opt_debug > 6:
        print("reduce():", "filter =", pp(filter), "pos =", pos)
    if pvg.opt_debug > 7:
        dumpstack(self2, xstack, label="pre reduce:")

    # Walk the stack
    loopx = pos ; wasop = False
    statex = 0 ; numidx = -1 ; opidx = -1 ;  num2idx = -1
    #for idx in xstack[pos:]:
    while True:
        if loopx >= xstack.getlen():
            break
        idx = xstack[loopx]
        if pvg.opt_debug > 7:
            print("item:", pp(self2.arrx[idx].stamp.xstr), "mstr:", self2.arrx[idx].mstr)
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
            if filter == "":
                self2.arrx[idx].flag = 1
            # Recurse into parenthases
            for aa in linfunc.ops_prec:
                prog = reduce(self2, xstack, aa, loopx + 1)
            #loopx = prog + 1
            if pvg.opt_debug > 7:
                print(" ** after recurse", prog )
            if pvg.opt_debug > 7:
                print("\nxstack post recurse:", end = " ")
                dumpstack(xstack)
            loopx += 1 #prog
            continue
        if self2.arrx[idx].stamp.xstr == ")":
            if pvg.opt_debug > 7:
                print("\nparen2:", idx, pp(self2.arrx[idx].stamp.xstr), loopx)
            if filter == "":
                self2.arrx[idx].flag = 1
            else:
                return loopx
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
    return loopx

# EOF
