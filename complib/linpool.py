#!/usr/bin/env python

''' syntab functions for the parser '''

import complib.stack as stack

gpool = stack.pStack()                 # Symtab pool

def addtopool(self2, xstack, nameoff = 0, typeoff = 1):

    ''' Add to global pool -- parse stack / symbol lookup table '''

    typename = self2.arrx[xstack.get(0)].mstr
    varname = self2.arrx[xstack.get(1)].mstr

    if  xstack.getlen() > 2:
        varval = self2.arrx[xstack.get(2)].mstr
    else:
        varval = 0

    for aa in gpool:
        if aa.namex == varname:
            error(self2, "Duplicate definition", self2.arrx[xstack.get(0)].pos)
            sys.exit(1)
    tpi = TypI(typename, varname, varval)
    gpool.push(tpi)
    datatype = pctona(self2.arrx[xstack.get(0)].mstr)
    return datatype

def lookpool(self2, varname):

    ''' Get symbol from name '''
    ret = None
    for aa in gpool:
        print("lookpool:", "'" + aa.namex + "'")
        if aa.namex == varname:
            ret = aa
            break
    return ret

def pctona(ddd):

    ''' Transform data type string to assembler equivalent '''
    #print("pctona:", ddd)
    retx = "dq"
    if ddd == "u8":
        retx = "db"
    elif ddd == "u16":
        retx = "dw"
    elif ddd == "u32":
        retx = "dd"
    elif ddd == "u64":
        retx = "dq"
    elif ddd == "float":
        retx = "dd"
    elif ddd == "double":
        retx = "dq"
    elif ddd == "extended":
        retx = "dt"
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

    import complib.lexdef as lexdef
    # Syntesize array of tokens
    class testx():
        def __init__(self):
            self.arrx = []
    self2 = testx()
    xstack =  stack.pStack()
    ss = lexdef.LexI(lexdef.StI(lexdef.xtokens[0]), "test")
    rr = lexdef.LexI(lexdef.StI(lexdef.xtokens[1]), "test2")
    self2.arrx.append(ss) ;  self2.arrx.append(rr)
    xstack.push(0) ;  xstack.push(1)
    ret = addtopool(self2, xstack)
    #print(ret)
    assert ret == "dq"
    ret = lookpool(self2, "test2")
    #print("'" + str(ret) + "'")
    assert "test : test2 = 0" == str(ret)

# EOF
