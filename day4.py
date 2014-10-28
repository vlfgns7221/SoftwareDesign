# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:40:13 2014

@author: pilhunchoi
"""
import math;
import random;
from decimal import *


def double(n):
    return 2*n;
    
    
def mysqrt(n):
    return math.sqrt(n);
    
def is_between(x,y,z):
    if (y>=x) & (y<=z):
        return True;
    else:
        return False;
        
def random_float(start, stop):
    a=random.randint(start, stop);
    return a;
    
    
def factorial(n):
    m=1;
    for i in range(n):
        m=m * (i+1);
    return m;

def sum_integers(x,y):
    t=0;
    for i in range(x,y+1):
        t=t+i;
    return t;
    
def is_prime(n):
    for i in range(2,n):
        if n%i ==0:
            return False;
    return True;            
        
def is_palindrome(x):
    n=len(x);
    for i in range(n):
        if x[i] != x[n-i-1]:
            return False;
    return True;
    
def approximate_e(n,x,p):
    m=0;
    for i in range(n):
        getcontext().prec = p;
        m=m+Decimal(x**i)/Decimal(factorial(i));
    return m;

def main():
    a=7
    k1=double(a);
    k2=mysqrt(a);
    k3=is_between(3,5,6);
    k4=random_float(3,100);
    k5=factorial(7);
    k6=sum_integers(3,7);
    k7=is_prime(101);
    k8=is_palindrome('status');
    k9=approximate_e(1000,1,50); 
    """approximate_e(n,x,p) n: number of operation for Talyor series
                            x: e^x
                            p: decimal palces
    """
    print k1, k2, k3, k4, k5, k6, k7, k8;
    print k9;

main()