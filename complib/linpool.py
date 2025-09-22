#!/usr/bin/env python

''' syntab functions for the lin parser '''

import complib.stack as stack

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
    ret = add2pool(self2, typename, varname, varval)
    return ret

def add2pool(self2, typename, varname, varval):

    if pvg.opt_debug > 7:
        print("addtopool:", "type:", pp(typename),
                        "var:", pp(varname), "val:", pp(varval))
    for aa in gpool:
        if aa.namex == varname:
            if pvg.opt_debug > 3:
                print("Dumping pool:")
                for aa in gpool:
                    print(" pool:", aa)
            error(self2, "Duplicate definition") #, varname)
            sys.exit(1)

    tpi = TypI(typename, varname, varval)
    gpool.push(tpi)
    datatype = pctona(typename)
    return datatype

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

class   Xenum():

    ''' Simple autofill enum to use in parser '''

    def __init__(self, *val):
        self.arr = [] ; self.narr = {}
        self.add(*val)

    def add(self, *val):
        for aa in val:
            self.narr[aa] = len(self.arr)
            self.arr.append(aa)

    def dump(self):
        strx = ""
        for cnt, aa in enumerate(self.arr):
            #print(cnt, aa)
            strx += str(cnt) + " = " + str(aa) + "\n"
        return strx

    def get(self, cnt):
        return self.arr[cnt]

    def val(self, name):
        try:
            ret = self.narr[name]
        except:
            if 0: #pvg.opt_verbose:
                print("Warn: adding:", name)
            self.add(name)
            ret = self.narr[name]
        return ret

class TypI:

    ''' Global type structure '''

    def __init__(self, typex, namex, valx):
        self.typex = typex
        self.namex = namex
        self.valx = valx

    def __str__(self):
        return str(self.typex) + " : " + str(self.namex) + \
                " = " + str(self.valx)

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

def test_xenum():

    eee = Xenum("no", "yes",)
    eee.add( "maybe")

    #print(eee.dump(), end = "")
    #print(eee.val("no"))
    #print(eee.val("yes"))

    assert eee.get(0) == "no"
    assert eee.get(1) == "yes"
    assert eee.val("no")  == 0
    assert eee.val("yes") == 1

    # Autogen
    assert eee.val("none") == 3

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

    if pvg.opt_debug > 5:
        print(" execop:", arg1, op, arg2, "; ret = ", ret, )

    return ret

def reduce(self2, xstack, filter, pos = 0):

    if pvg.opt_debug > 5:
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

# EOF
