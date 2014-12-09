# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 21:40:39 2014

@author: pilhunchoi
"""

import core

server = core.init_server()
db = server.db

from models import *

db.create_all()