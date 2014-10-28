# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 13:31:49 2014

@author: pilhunchoi
"""

def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)
    
print factorial(7);

def fib(n):
    if n ==1:
        return 1
    elif n ==0:
        return 1
    return fib(n-1)+fib(n-2)

print fib(7)