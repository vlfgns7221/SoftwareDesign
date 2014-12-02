# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 21:11:28 2014

@author: pilhunchoi
"""
from flask import request,jsonify
import datetime

from sqlalchemy.sql.expression import func
from sqlalchemy import or_, and_

from core import server
from models import *

app = server.app
db = server.db


@app.route('/')
def game_init_page():
	return 'Welcome to Fortress of Peter and Benjamin(slave of Peter)'

#sign_up
@app.route('/sign_up', methods=['POST'])
def sign_up():
    user_id=request.form.get('user_id',type=str)
    user = User(user_id)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception, ex:
        db.session.rollback()
        return 'fail'
    return user_id

#login
@app.route('/logjn',methods=['POST'])
def login():
    user_id=request.form.get('user_id',type=str)
    user = User(user_id)
    
    # db check function should be defined
"""    
@app.route(game_id,methods=['GET'])
def game_room(user1, user2):
"""        
    
# example page
@app.route('/gg')
def gg():
	return 'Bonjun is GG'

@app.route('/add', methods=['GET'])
def add():
	a = request.args.get('a',type=int)
	b = request.args.get('b',type=int)
	return 'The answer is '+str(a+b)    
    
    