#!/usr/bin/python

"""
basic_fortune.py
date created: 2014 September 10

This python script is a basic program that allows users to introduce themselves to the computer and receive a fortune message. If another user runs the program and introduces his or herself, it is possible that s/he will receive a different message (provided that the name is of a different length in this version).

Students should use this script to get familiar with the Olin College Software Design course Fall 2014 GitHub repository. Each student should add a message and/or some functionality. We will explore how to get past any merge messes that arise.

author = amonmillner
"""

def fortune():
   """
   This function allows a user to type a name and receive a fortune.
   The fortune selected from the list of possibilities depends on the
   length of the name or string that a user inputs.
   """
   username = raw_input('what is your name?')
   fortuner = ['you will soon get a big surprise', 'happiness will soon find you', 'things are looking up', 'a wish that you made in the past is about to come true', 'you will be greeted with a gift in the near future', 'the sky will fall on you tomorrow','if tomorrow is a chicken butt, what is a carrot do on Sundays?', 'Rainy Days and Mondays always get me down']
   print fortuner[(len(username)-1)%len(fortuner)]

fortune()
