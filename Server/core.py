# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 20:55:15 2014

@author: pilhunchoi
"""

server = None

def init_server():
    from flask import Flask
    from flask.ext.sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = r'mysql://peter:0905@localhost'
    
    db = SQLAlchemy(app)
    
    global server
    class ServerObject(object):
        pass
    server = ServerObject()
    server.app = app
    server.db = db
    
    return server