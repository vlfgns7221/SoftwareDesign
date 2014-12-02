'''
from flask import Flask
from flask import request
from flask import jsonify
'''
import core

server = core.init_server()
app = server.app

from views import *

"""
@app.route('/')
def hello_world():
	return 'Harsh is a smart guy'

@app.route('/gg')
def gg():
	return 'Bonjun is GG'

@app.route('/add', methods=['GET'])
def add():
	a = request.args.get('a',type=int)
	b = request.args.get('b',type=int)
	return 'answer'+str(a+b)

@app.route('/login', methods=['POST'])
def login():
    user_id=request.form.get('user_id',type=str)
    return user_id
"""    
if __name__ == '__main__':
	app.run('0.0.0.0', port=7890, debug=True, threaded=True)


