# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 13:43:31 2014

@author: pilhunchoi
"""
import pdb
def factorial(n):

    """ Computes the factorial of the non-negative input integer n """

    return_val = 1

    for i in range(n):

        assert(return_val >= 1)

        return_val *= i

    return return_val


if __name__ == '__main__':

    print factorial(5)
    
