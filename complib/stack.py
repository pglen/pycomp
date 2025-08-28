#!/usr/bin/env python

import sys

class StackError(Exception):
    pass

class pStack():

    def __init__(self, raisex = False):
        self._store = []
        self.raisex = raisex   # Pass False if production code
        self.verbose = False

    def __iter__(self):
        for aa in self._store:
            yield aa

    def empty(self):
        self._store = []

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
        if len(self._store) == 0:
            if self.raisex: raise StackError("No data to pop")
            return None
        item = None
        try:
            item = self._store.pop(len(self._store) - 1)
        except Exception as xxx:
            item = None
            if self.raisex: raise ValueError
            else:
                if self.verbose:
                    print ("exception:", xxx, sys.exc_info())
        return item

    def get(self, idx):
        if len(self._store) == 0: return None
        try:
            item = self._store[idx]
            if self.raisex: raise
        except:
            item = None
        return item

    # Non destructive peek
    def peek(self):
        if len(self._store) == 0: return None
        xlen = len(self._store)
        if xlen <= 0: return None
        item = self._store[xlen - 1]
        return item

    def getlen(self):
        return len(self._store)

    def dump(self):
        strx = ""; cnt = 0; xlen = len(self._store)
        while True:
            if cnt >= xlen:
                break
            strx += str(self._store[cnt]) + " "
            cnt += 1
        return strx;

    def show(self):
        cnt = len(self._store) - 1
        while cnt >= 0:
            print (self._store[cnt]);  cnt -= 1

    def __getitem__(self, idx):
        try:
            item = self._store[idx]
        except:
            if self.raisex: raise
            else: item = None
        return  item

    #def __setitem__(self, idx, item):
    #    self._store[idx] = item
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
    assert ss != None
    vvv = "abc"
    ss.push(vvv)
    assert ss.getlen() == 1
    tt = ss.pop()
    assert tt == vvv
    ttt = ss.pop()
    assert ttt == None
    assert ss.getlen() == 0

def test_pop():
    ss = pStack()
    assert ss != None
    ss.raisex = True
    vvv = "abc"
    ss.push(vvv)
    tt = ss.peek()
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

def test_empty():
    ss = pStack()
    vvv = "abc"
    ss.push(vvv)
    assert len(ss) == 1
    ss.empty()
    assert len(ss) == 0

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
    print("iter:", st[1])
    print("peek:", st.peek())
    print("pop:", st.pop())
    print("pop:", st.pop())

    print("pop:", st.pop())
    print("iter:", st[0])

    st.push("hello2") ;  st.push("world2")
    st.show()
    st.empty()
    st.show()


# EOF
