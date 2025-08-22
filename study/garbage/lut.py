# Connect parser token to lexer item. This way the definitions are synced
# without the need for double definition
# Look up, create if not found

class Lut:

    def __init__(self):
        self.tokdef = []

    def lookup(self, strx):
        ret = None
        for aa in self.tokdef:
            if strx == aa[1]:
                #print "found", aa
                ret = aa
                break
        if ret == None:
            #print ("Token '" + strx + "' not found, adding ... ", end = " " )
            self.tokdef.append((unique(), strx))
            for aa in  self.tokdef:
                if strx == aa[1]:
                    #print(aa)
                    ret = aa
                    break
            if ret == None:
                print ("Token '" + strx + "' not found, please correct it.")
        return aa

    def rlookup(self, idn):
        ret =  "none"
        for aa in  self.tokdef:
            #print("idx =", idn, "aa =", aa)
            if idn == aa[0]:
                ret = aa[1]
                break
        return ret

    def dump(self, pad = 15, perline = 5):
        res = ""
        cnt = 0
        for aa in  self.tokdef:
            strx = str(aa[0]) + " = " + "'" + aa[1] + "'"
            xlen = pad - len(strx)
            res += "%s%s" % (strx, " " * xlen)
            cnt += 1
            if cnt % perline == 0:
                res += "\n"
        #res += "\n"
        return res

