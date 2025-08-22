#!/usr/bin/env python

class TreeNode:

    def __init__(self, datax = None):
        self.data = [] ;  self.subs = [] ; self.det = []
        self.parent = None
        self.data.append(datax)

    def addata(self, datax):
        ''' add Data '''
        self.data.append(datax)

    def addet(self, datax):
        ''' add detail '''
        self.det.append(datax)

    def add(self, sub):
        ''' add subtree level '''
        sub.parent = self
        self.subs.append(sub)
        return sub

    def _level(self, res, res2):
        ''' add result of level '''
        res3 = self.data, self.det
        res.append(res3)
        if  self.parent:
            res2.append(self.parent.data)
        for aa in self.subs:
            aa._level(res, res2)

    def __str__(self):
        res = [] ; res2 = []
        self._level(res, res2)
        return str(res)
        #return str(res) + " par: " + str(res2)

treeroot = TreeNode("root")
lastnode = treeroot

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

    #lastnode = treeroot.add(TreeNode("func"))
    #lastnode.addet("name")
    #lastnode = lastnode.add(TreeNode("args"))
    #lastnode.addet("arg1")
    #lastnode.addet("arg2")
    #lastnode = lastnode.add(TreeNode("body"))
    #lastnode.addet("statm1")
    #lastnode.addet("statm2")
    #print(treeroot)

def test_tree():

    lastnode = treeroot.add(TreeNode("func"))
    #print(str(lastnode))
    assert str(lastnode) == "[(['func'], [])] par: [['root']]"

def test_fulltree():

    lastnode = treeroot.add(TreeNode("func"))
    lastnode.addet("name")
    lastnode = lastnode.add(TreeNode("args"))
    lastnode.addet("arg1")
    lastnode.addet("arg2")
    lastnode = lastnode.add(TreeNode("body"))
    lastnode.addet("statm1")
    lastnode.addet("statm2")

    #print(treeroot)
    res = "[(['root'], []), (['func'], []), (['func'], ['name']), " \
            "(['args'], ['arg1', 'arg2']), (['body'], ['statm1', 'statm2'])] " \
              "par: [['root'], ['root'], ['func'], ['args']]"

    assert str(treeroot) == res

# EOF
