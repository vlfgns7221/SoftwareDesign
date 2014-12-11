import core
# server information
server = core.init_server()
app = server.app

from views import *
  
if __name__ == '__main__':
	app.run('0.0.0.0', port=9000, debug=True, threaded=True)


