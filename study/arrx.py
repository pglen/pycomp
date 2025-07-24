#!/usr/bin/env python

''' functions for the linear parser '''

def slx(arry, st, end):
    for aa in range(st, end):
        arry[aa] = arry[aa] + 1
    #print(arry)

arrx = [1,2,3,4,5,6,7,8 ]

print(arrx)
for aa in range(len(arrx)):
    arrx[aa] = arrx[aa] + 1
print(arrx)

slx(arrx, 3, 6)

print(arrx)

