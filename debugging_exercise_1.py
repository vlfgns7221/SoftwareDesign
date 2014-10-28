# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 17:52:54 2014

@author: pruvolo
"""

def cumulative_sum(L):
    """ returns a list where each element in the returned list is the
    	cumulative sum of the elements up to the corresponding element in
	the original list.
	
	L: the original list
	returns: a new list where element i is equal to the sum of element
		 0 through i in the original list """
    for i in range(len(L)):
        if i-1 >= 0: 
            L[i] = L[i-1] + L[i];
        else :
            L[i]=L[i];
    return L

if __name__ == '__main__':
    print cumulative_sum([1, 2, 3])
