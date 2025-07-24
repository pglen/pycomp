#!/usr/bin/env python

''' Definitions for the linear parser '''

arrx = []

class Testx():
    def __init__(self, tok = "", val = ""):
        ''' Doc '''
        self.token = tok
        self.value = val
    def __repr__(self):
        return self.token + " = " + self.value

for aa in range(5):
    arrx.append(Testx("tok"+str(aa), "val"+str(aa+2)))

print(arrx)

# EOF
