# -*- coding: utf-8 -*-
"""
Random_art.py

@author: amonmillner, adapted from pruvolo work
"""

# you do not have to use these particular modules, but they may help
from random import randint
from math import *
import Image

def sin_pi(a):
    return sin(pi*a)

def cos_pi(a):
    return cos(pi*a)

def square(a):
    return a**2
    
def sin_ab(a,b):
    return sin(a*b*pi)
        
def prod(a,b):
    return a*b    
    
def x(a,b):
    return a

def y(a,b):
    return b
    
def selection(t):
    if t==1:
        k=randint(1,2);
        if k==1:
            return ["x"]
        elif k==2:
            return ["y"]
    else: 
        k=randint(1,5);
        if k==1:
            return ["sin_pi",selection(t-1)]
        elif k==2:
            return ["cos_pi",selection(t-1)]
        elif k==3:
            return ["prod",selection(t-1),selection(t-1)]
        elif k==4:
            return ["square",selection(t-1)]
        elif k==5:
            return ["sin_ab",selection(t-1),selection(t-1)]

def build_random_function(min_depth, max_depth):
    """ your doc string goes here
    """
    # your code goes here
    sentence=[];
    ran1=randint(min_depth, max_depth);
    sentence=selection(ran1)
    return sentence
                  
def evaluate_random_function(f, x, y):
    """ your doc string goes here
    """
    # your code goes here    
    if f[0]=='x':
        return x
    elif f[0]=='y':
        return y
    elif f[0]=='sin_pi':
        return sin_pi(evaluate_random_function(f[1],x,y))
    elif f[0]=='cos_pi':
        return cos_pi(evaluate_random_function(f[1],x,y))        
    elif f[0]=='square':
        return square(evaluate_random_function(f[1],x,y))        
    elif f[0]=='sin_ab':
        return sin_ab(evaluate_random_function(f[1],x,y),evaluate_random_function(f[2],x,y))
    elif f[0]=='prod':
        return prod(evaluate_random_function(f[1],x,y),evaluate_random_function(f[2],x,y))        

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        TODO: please fill out the rest of this docstring
    """
    # your code goes here
    input_diff=(input_interval_end-input_interval_start);
    output_diff=(output_interval_end - output_interval_start);
    output=(val-input_interval_start)*output_diff/float(input_diff)+output_interval_start;
    return output

#your additional code and functions go here
def plotin(equ, pixel):
    canvas=Image.new("L",(pixel,pixel))
    for i in range(pixel):
        val1=remap_interval(i,0,pixel,-1,1)
        for j in range(pixel):
           val2=remap_interval(j,0,pixel,-1,1)
           val=evaluate_random_function(equ,val1,val2)
           intensity=int(remap_interval(val,-1,1,0,255))
           canvas.putpixel((i,j), intensity)
    return canvas
    
def RGBcolor(red_eq,blue_eq,green_eq,pixel):
    red = plotin(red_eq,pixel)
    green = plotin(green_eq,pixel)
    blue = plotin(blue_eq,pixel)
    return Image.merge("RGB", (red, green, blue))

def draw(pixel):
    for i in range(0,10):
        red_eq=build_random_function(3,4);
        blue_eq=build_random_function(3,5);
        green_eq=build_random_function(3,6);
        im=RGBcolor(red_eq,blue_eq,green_eq,pixel)
        im.save("example" + str(i+1) + ".png", "PNG")

draw(350)