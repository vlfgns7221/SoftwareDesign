# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 11:10:01 2014

@author: Pil Hun, Choi
"""

def fermat():
    value=inputt();
    value=integer(value);
    a=value[0];
    b=value[1];
    c=value[2];
    n=value[3];
    check_fermat(a,b,c,n);
    
def check_fermat(a,b,c,n):
    d=a**n + b**n;
    e=c**n;
    if n <= 2:
        print 'n must be greater than 2, enter the values again';
        fermat();
    elif d == e:
        print 'Holy smokes, Fermat was wrong';
    else:
        print 'No, that doesn''t work';
        
def inputt():
    a=raw_input('enter a(it must be integer) : ');
    b=raw_input('enter b(it must be integer) : ');
    c=raw_input('enter c(it must be integer) : ');
    n=raw_input('enter n(it must be integer and greater than 2) : ');
    return a,b,c,n;
    
def integer(value):
    a=int(value[0]);
    b=int(value[1]);
    c=int(value[2]);
    d=int(value[3]);
    return a,b,c,d;
    
fermat();

