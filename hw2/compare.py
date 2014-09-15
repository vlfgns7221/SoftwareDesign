# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 11:58:25 2014

@author: Pil Hun, Choi
"""
"""
def com():
    x=raw_input('enter x : ');
    y=raw_input('enter y : ');
    x=float(x);
    y=float(y);
    a=compare(x,y);
    print a;
"""
def compare(x,y):
    if x > y:
        return 1;
    elif x==y:
        return 0;
    else:
        return -1;
        
"com();