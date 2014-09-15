# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:36:53 2014

@author: Pil Hun, Choi
"""


def pl():
    print '+',

def mi():
    print '---- +',

def sp():
    print '     |',
    
def bar():
    print '|',
    
def ent():
    print '\n',
    
def do_twice(f):
    f()
    f()
    
def do_four(f):
    do_twice(f)
    do_twice(f)
    
def firstrow():
    pl()
    do_twice(mi)
    ent()
    
def middlerow():
    bar()
    do_twice(sp)
    ent()
    
def grid():
    firstrow()
    do_four(middlerow)
    firstrow()
    do_four(middlerow)
    firstrow()
    
    
grid()