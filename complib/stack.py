#!/usr/bin/env python

import sys

def funcpvg(xpvg):
    global pvg
    pvg = xpvg

class StackError(Exception):
    pass

class pStack():

    def __init__(self, raisex = False, name = ""):
        self._store = []
        self.raisex = raisex   # Pass False if production code
        self.name = name

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
            print ("exception:", xxx, sys.exc_info(), self.name)
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
            if pvg.opt_debug > 2:
                print("Warn: stack underflow.", self.name)
            if self.raisex:
                raise StackError("No data to pop on: %s" % self.name)
            return None
        item = None
        try:
            item = self._store.pop(len(self._store) - 1)
        except Exception as xxx:
            item = None
            if self.raisex:
                raise ValueError
            else:
                print("exception:", xxx, sys.exc_info(), self.name)
        return item

    def get(self, idx):
        if len(self._store) == 0:
            if pvg.opt_debug > 2:
                print("Warn: stack underflow", self.name)
            return None
        try:
            item = self._store[idx]
            if self.raisex: raise
        except:
            item = None
        return item

    # Non destructive peek
    def peek(self):
        if len(self._store) == 0:
            return None
        xlen = len(self._store)
        if xlen <= 0: return None
        item = self._store[xlen - 1]
        return item

    def len(self):
        return len(self._store)

    def getlen(self):
        return len(self._store)

    def dump(self, sep = " "):
        strx = ""; cnt = 0; xlen = len(self._store)
        while True:
            if cnt >= xlen:
                break
            strx += str(self._store[cnt]) + sep
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
            if self.raisex:
                raise
            else:
                if pvg.opt_debug > 2:
                    print("Warn: stack undeflow", self.name)
                item = None
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
    fakedummy()
    print("Tests:")
    ss = pStack(name="test")
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
    fakedummy()
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
    fakedummy()
    ss = pStack()
    vvv = "abc"
    ss.push(vvv)
    assert len(ss) == 1
    ss.empty()
    assert len(ss) == 0

def fakedummy():
    ''' Simulate runtime debug var '''
    global pvg;
    class dummy(): pass
    pvg = dummy()
    pvg.opt_debug = 0

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    fakedummy()

    st2 =  pStack(True, "st2")
    st =  pStack()
    st.push("hello") ;  st.push("world")
    print("stack len:", len(st), st.getlen())
    st.show()
    print("stack len:", len(st))
    print("dump:", st.dump(", "))
    print("first:", st.first())
    print("last:", st.last())
    print("get:", st.get(1), end = " ")
    print("iter:", st[1], end = " ")
    print("peek:", st.peek())
    print("pop:", st.pop(), end = " ")
    print("pop:", st.pop(), end = " ")
    print("pop:", st.pop(), end = " ")
    print("iter:", st[0])

    st.push("hello2") ;  st.push("world2")
    st2.push("1111") ;  st2.push("2222")
    st.show()
    st.empty()
    print("empty: ", end = "'" ) ; st.show() ; print("'")
    st2.show()
    st2.empty()
    print("empty2: ", end =  "'") ; st2.show() ; print("'")

    # Exeption:
    try:
        st2.pop()
    except:
        #print(sys.exc_info())
        print("pop exc OK")
# EOF
