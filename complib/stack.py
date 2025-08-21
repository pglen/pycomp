#!/usr/bin/env python

import sys

class pStack():

    def __init__(self):
        self._store = []
        self.raisex = False
        self.verbose = False

    def push(self, item):
        try:
            self._store.append(item)
            #self.cnt = self.cnt+1
        except Exception as xxx:
            if self.verbose:
                print ("exception:", xxx, sys.exc_info())
            if self.raisex: raise

    def last(self):
        xlen = len(self._store)
        if xlen == 0: return None
        item = self._store[xlen - 1]
        return item

    def first(self):
        xlen = len(self._store)
        if xlen == 0: return None
        item = self._store[0]
        return item

    def pop(self):
        if len(self._store) == 0: return None
        item = None
        try:
            item = self._store.pop(len(self._store) - 1)
        except Exception as xxx:
            item = None
            if self.raisex: raise
            else:
                if self.verbose:
                    print ("exception:", xxx, sys.exc_info())
        return item

    def get(self, idx):
        if len(self._store) == 0: return None
        item = self._store[idx]
        return item

    # Non destructive pop
    def pop2(self):
        if len(self._store) == 0: return None
        xlen = len(self._store)
        if xlen <= 0: return None
        item = self._store[xlen - 1]
        return item

    def stacklen(self):
        return len(self._store)

    def dump(self):
        strx = ""; cnt = 0; xlen = len(self._store)
        while cnt < xlen:
            strx += str(self._store[cnt]) + " "
            cnt += 1
        return strx;

    def show(self):
        cnt = len(self._store) - 1
        while cnt >= 0:
            print (self._store[cnt]);  cnt -= 1

    #def __repr__(self):
    #    strx = self.dump()
    #    return strx

    def __str__(self):
        strx = self.dump()
        return strx

    def __len__(self):
        return len(self._store)


def test_main():
    print("Tests:")
    ss = pStack()
    assert ss
    vvv = "abc"
    ss.push(vvv)
    tt = ss.pop()
    assert tt == vvv
    ttt = ss.pop()
    assert ttt == None

def test_pop():
    ss = pStack()
    assert ss
    ss.raisex = True
    vvv = "abc"
    ss.push(vvv)
    tt = ss.pop2()
    assert tt == vvv
    tt2 = ss.pop()
    assert tt2 == vvv

    # Test if exception
    exc = 0
    try:
        tt3 = ss.pop()
    except:
        exc = 1
    assert exc == 1

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

    st =  pStack()
    print("stack len:", len(st))
    st.push("hello") ;  st.push("world")
    st.show()
    print("stack len:", len(st))
    print("dump:", st.dump())
    print("first:", st.first())
    print("last:", st.last())
    print("get:", st.get(1))
    print("pop2:", st.pop2())
    print("pop2:", st.pop2())
    print("pop:", st.pop())
    print("pop:", st.pop())
    print("pop:", st.pop())

# EOF
