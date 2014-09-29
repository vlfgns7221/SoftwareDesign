# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 12:53:05 2014

@author: Pil Hun, Choi
"""

from pattern.web import *

def extract(x):
    return x.encode()
    
def sear(y):
    return Wikipedia().search(y)
    
def gather(s,t):
    return t+map(extract,s)  
    
def chooseword(initial_word,t,total,total_number):
    number=raw_input('Enter the number you want to see(0 : back) : ');
    number=int(number);
    if number == 0:
        main(initial_word,total,total_number);
    else:
        main(t[number-1],total,total_number);  

def stat(t,total,total_number):
    length=len(total)
    if total==[]:
        total=t;
        for i in range(len(t)):
            total_number.append(1)
    else:
        for j in range(len(t)):
            k=0;
            for i in range(length):
                if total[i]==t[j]:
                    total_number[i]+=1
                    k=1;
            if k==0:
                total.append(t[j])
                total_number.append(1)
    return total, total_number
                    
def topfive(total, total_number):
    save=list(total_number);
    print '\n Top five words : \n '
    for i in range(5):
        k=save.index(max(save));
        print str(i+1)+'. '+total[k]+' : '+str(max(save));
        save[k]=0;        
    
def main(initial_word,total,total_number):
    article = sear(initial_word)
    print '\n'+article.title+'\n';
    print article.string
    t=[];
    for section in article.sections:
        s=section.links
        t=gather(s,t)
    print '\n The related articles :  ';    
    for i in range(len(t)):
        a=str(i+1);
        print a+'. '+t[i]    
    (total, total_number)=stat(t,total,total_number)
    topfive(total, total_number);
    chooseword(initial_word,t,total,total_number);
    
ini=raw_input('\n Enter the words you want to search : ');
main(ini,[],[])
