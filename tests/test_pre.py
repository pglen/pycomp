#!/usr/bin/env python3

import pytest, os, sys
from mytest import *

# Test for pycomp

def setup_module(module):
    """ setup any state specific to the execution of the given module.
    """
    pass

def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
        method.
    """
    pass

def setup_function(function):
    pass

def teardown_function(function):
    pass

# ------------------------------------------------------------------------
# Start

sys.path.append("..")

from complib import stack

def test_pre():

    ss = stack.Stack()
    assert ss
    var  = "aa" * 10
    ss.push(var)
    bb = ss.pop()
    assert bb == var
    cc = ss.pop()
    assert cc == None
    #print(var)
    #assert 0

# EOF
