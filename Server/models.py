# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 21:24:17 2014

@author: pilhunchoi
"""

from core import server
db = server.db

class User(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    user_id = db.Column(db.String(40), nullable=False)
    
    def __init__(self,user_id):
        self.id = id
        self.user_id = user_id
    
    def __str__(self):
        return self.user_id
 
       
class Game(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key=True)
#    user_id = db.Column(db.String(40), nullable=False, Foreignkey(user.user_id))
    
    def __init__(self,user_id):
        self.id = id
        self.user_id = user_id

    def __str__(self):
        return self.user_id

            