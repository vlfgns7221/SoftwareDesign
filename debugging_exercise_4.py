# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 17:52:54 2014

@author: pruvolo

"""


def get_multiple_of_list(L,n):
    for i in range(len(L)):
        L[i] = L[i]*n
    return L
    
def get_double_and_triple():
    return get_multiple_of_list([1, 4, 8],2)+get_multiple_of_list([1, 4, 8],3);
    
if __name__ == '__main__':
    print get_double_and_triple()
