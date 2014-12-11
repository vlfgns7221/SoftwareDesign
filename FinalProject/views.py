# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 21:11:28 2014

@author: pilhunchoi
"""
# working directory of Server
from flask import request,jsonify
import datetime

from sqlalchemy.sql.expression import func
from sqlalchemy import or_, and_

from core import server
from models import *

app = server.app
db = server.db

"""
@app.route('/')
def game_init_page():
	return 'Welcome to Fortress of Peter and Benjamin(slave of Peter)'
"""

#sign_up and login,
@app.route('/sign_up', methods=['POST'])
def sign_up():
    user_id=request.form.get('user_id',type=str)
    existing_user = User.query.filter_by(user_id = user_id).first()
    #existing_user = User.query.filter(User.user_id.contains('peter')).first()
    if not existing_user:    
        user = User(user_id) # create new user account
        try:
            db.session.add(user)
            db.session.commit()
        except Exception, ex:
            db.session.rollback()
            return str(ex)
    return "True"

"""    
#login
@app.route('/logjn',methods=['POST'])
def login():
    user_id=request.form.get('user_id',type=str)
    user = User.query.filter_by(user_id = user_id).first()
    if not user:
        return False
    else:
        return True
"""

@app.route('/usernames',methods=['POST'])
def usernames():
    game_id=request.form.get('game_id',type=int)
    user_data=Game.query.filter_by(id=game_id).all()
    username=user_data[len(user_data)-1]
    user1=username.user_id_1
    user2=username.user_id_2
    return jsonify(User1 = user1, User2 = user2)
    
# start game, create new game or join the game room
@app.route('/startgame',methods=['POST'])
def start_game():
    user_id=request.form.get('user_id',type=str)
    room=Game.query.filter_by(room_active = True).all()
    
    if len(room) == 0:  # create new game room
        room_ini=Game(user_id,None)
        try:
            db.session.add(room_ini)
            db.session.commit()
        except Exception, ex:
            db.session.rollback()
            return 'fail'
        room=Game.query.filter_by(room_active = True).all()
        room_active=room[len(room)-1]
    else:
        room_active=room[len(room)-1]
        if room_active.user_id_2 != None:     # if the room is already occupied, 
            room_active2=Game(user_id, None)  # create new game room
            try:
                db.session.add(room_active2)
                db.session.commit()
            except Exception, ex:
                db.session.rollback()
                return 'fail'
            room_act=Game.query.filter_by(user_id_1 = user_id).all()
            room_active3=room_act[len(room_act)-1]
            ID = str(room_active3.id)    
            return ID    
        else:
            """
            if room_active.user_id_1 == user_id:
                return str(room_active.id) # return game number
            else:
            """
            room_active.user_id_2 = user_id # join the game
    
    try:
        db.session.add(room_active)
        db.session.commit()
    except Exception, ex:
        db.session.rollback()
        return 'fail'
    ID = str(room_active.id)    
    return ID # return game number

# check second user(wait for second user)    
@app.route('/checkseconduser',methods=['POST'])
def check_second_user():
    game_id=request.form.get('game_id',type=int)
    room=Game.query.filter_by(id = game_id).all()
    room_active=room[len(room)-1]
    user_id_2 = room_active.user_id_2
    if user_id_2 is None: 
        return "0" # That user_id_2 is None means second user did not join the game
    else:
        return "1"# Second user joined, start the game
 
 # check end
@app.route('/check_end',methods=['Post'])
def check_end():
    game_id=request.form.get('game_id',type=int)
    check = Game.query.filter_by(id = game_id).all()
    checkend=check[len(check)-1]
    return str(checkend.room_active) #if the other user is afk(quit the game), the game would stop
    
@app.route('/closegame',methods=['Post'])
def close_game():
    game_id=request.form.get('game_id',type=int)
    check = Game.query.filter_by(id = game_id).all()
    closegame=check[len(check)-1]
    # if you quit the game, room_active would be False and let the other user know aabout this.
    closegame.room_active = False 
    try:
        db.session.add(closegame)
        db.session.commit()
    except Exception, ex:
        db.session.rollback()
        return 'fail'
    return 'success'

# action update    
@app.route('/action',methods=['POST'])
def action():
    # if you move the tanks, change the angle, direction or fire the missle, update information to the database
    game_id=request.form.get('game_id',type=int)
    turn = request.form.get('turn', type=int)
    posx=request.form.get('posx',type=int)
    power=request.form.get('power',type=int)
    angle=request.form.get('angle',type=int)
    direction=request.form.get('direction',type=int)
    actionlist=Gameroom.query.filter_by(game_id = game_id).all()
    if actionlist ==[]:
        new_action= Gameroom(game_id,turn,posx,angle,power,direction)
    else:
        action=actionlist[len(actionlist)-1]
        if action is None:
            new_action = Gameroom(game_id,turn,posx,angle,power,direction)
        else:
            new_action=action
            new_action.game_id=game_id
            new_action.turn = turn
            new_action.posx=posx
            new_action.power=power
            new_action.angle=angle
            new_action.direction=direction
        
    try:
        db.session.add(new_action)
        db.session.commit()
    except Exception, ex:
        db.session.rollback()
        return 'fail'
    return 'success'

# check the other user's action.
@app.route('/checkaction',methods=['POST'])
def check_action():
    game_id=request.form.get('game_id',type=int)
    # load all the information from the associated gameroom database
    current_turn_action = Gameroom.query.filter_by(game_id=game_id).first()
    if current_turn_action is None:
        #If the database is empty, send the following information
        return jsonify(Turn=1,posx=30, angle = 0, power=0, direction =0)
    else:
        # send the following data
        return jsonify(Turn=current_turn_action.turn, posx=current_turn_action.posx, angle = current_turn_action.angle, power=current_turn_action.power, direction=current_turn_action.direction)
    