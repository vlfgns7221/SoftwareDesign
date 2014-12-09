import core

server = core.init_server()
app = server.app

from views import *
  
if __name__ == '__main__':
	app.run('0.0.0.0', port=7890, debug=True, threaded=True)


