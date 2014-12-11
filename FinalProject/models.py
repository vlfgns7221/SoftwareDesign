# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 21:24:17 2014

@author: pilhunchoi
"""
import datetime
from core import server
db = server.db

# declare game database in mySQL

# Declare and save User in MySQL
class User(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    user_id = db.Column(db.String(40), nullable=False)
    
    def __init__(self,user_id):
        self.id = id
        self.user_id = user_id
    
    def __str__(self):
        return self.user_id
 
# Declare and save Game in MySQL       
class Game(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key=True)  # game number(name)
    user_id_1 = db.Column(db.String(40), nullable = False)    # declare user1
    user_id_2 = db.Column(db.String(40))                      # declare user2
    room_active=db.Column(db.Boolean,nullable=False)          # declare room active?
    gameroom = db.relationship('Gameroom',uselist=False)      
    
    def __init__(self,user_id_1, user_id_2=None):
        self.id = id
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.room_active=True

# Declare and save detail game information in MySQL
class Gameroom(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False) # declare game number
    game = db.relationship('Game',uselist=False)       
    turn = db.Column(db.Integer, nullable=False)   # declare turn information
    
    posx=db.Column(db.Integer, nullable=False)     # declare tank position information
    angle=db.Column(db.Integer, nullable=False)    # declare tank angle information
    power=db.Column(db.Integer, nullable=False)    # declare tank power information
    direction=db.Column(db.Integer, nullable=False) # declare tank direction information
    
    def __init__(self,game_id, turn, posx,angle,power,direction):
        self.id = id                     
        self.game_id = game_id        
        self.turn = turn
        self.posx = posx
        self.angle = angle
        self.power = power
        self.direction = direction
            