# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 21:40:39 2014

@author: pilhunchoi
"""

import core

server = core.init_server()
db = server.db
# DB initializing
from models import *

db.drop_all() #delete all the database in MySQL
db.create_all() #create new database in MySQL