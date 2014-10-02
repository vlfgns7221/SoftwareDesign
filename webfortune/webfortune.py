"""
webfortune.py
date created: 2014 September 18
author: amonmillner

This script is a quick demonstration of using the Pattern package to grab the text content of a webpage.

There are some lines below that introduce some concepts that the Software Design class might be seeing for the first time. There are string manipulations and actions performed on lists that we will discuss during the demonstration.

There are countless ways to write a program that would achieve the outcome of grabbing text from a webpage - but we'll start with this less-elegant way of performing the task and collaboratively explore alternative ways to get the results we're looking for - random fortunes.

"""

#brings in the tools that we want to use.
from pattern.web import *
from random import randint
import re

def scrape():
    """Uses Pattern's URL download function to pull HTML code from the website listed below"""
    random_50_fortunes = plaintext(URL('http://www.fortunecookiemessage.com/archive.php?start='+str(randint(0,16)*50)).download())
    #creates a list from the large plaintext grab, making new list entries for each newline in the page
    fortune_list = random_50_fortunes.split('\n\n')

    #one way to traverse a list looking for content - enumerate is used to capture the size of the list in this case
    for i, j in enumerate(fortune_list):
        #looking for the start of the actual fortunes on the page
        if 'Fortune Cookie Quotes' in j and '\n' in j:
            starter = i+1
        #looking for the end of the actual fortunes on the page
        if 'Total quotes in our database' in j:
            ender = i
    #removing webpage content before and after the fortunes
    fortune_list = fortune_list[starter:ender]
    #printing the random quote each time we run the program
    fortune = fortune_list[randint(0,(len(fortune_list)-1))]

    #in class crowdsourced solution for removing parenthetical info about the number of comments a fortune received... and cleaned up a bit by amonmillner
    x = len(fortune)
    #treating the string fortune like a list of characters to traverse it looking for an open parenthesis
    for n in range(x):
        if fortune[n] == '(':
            #if found, a new string will be created only from the characters in the fortune string before the open parenthesis
            truncater = n
            fortune = fortune[:truncater]
            break
    print fortune

scrape()
