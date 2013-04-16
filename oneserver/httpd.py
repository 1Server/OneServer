from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import TCPServer
from threading import Thread

from manager import OneServerManager

##
# A simple HTTP daemon that directs as needed to different handlers.
class Httpd(BaseHTTPRequestHandler):
	##
	# Creates and sets up the server but does not start it.
	#
	# @param address - the server address (can be empty string)
	# @param port - the port to listen on
	def __init__(self, address, port):
		self.httpd = TCPServer((address, port), self)
		self.thread = None

		manager = OneServerManager()
		self.log = manager.log
	
	##
	# Starts the server and handles requests.
	def start(self):
		def run():
			self.httpd.serve_forever()

		self.log.debug('Starting HTTPD server')

		self.thread = Thread(group = None, target = run)
		self.thread.start()

	##
	# Stops the server from handling requests.
	def stop(self):
		self.log.debug('Shutting down HTTPD server')

		self.httpd.shutdown()
		self.thread.join(15.0)

		if self.thread.isAlive():
			self.log.error('HTTPD thread could not be stopped!')

	##
	# Handles GET requests.
	def do_GET(self):
		self.log.debug('GET request received: ' + self.path)

		pass
	
	##
	# Handles POST requests.
	def do_POST(self):
		self.log.debug('POST request received')

		pass
	
	##
	# Handles HEAD requests.
	def do_HEAD(self):
		self.log.debug('HEAD request received')

		pass
	
	##
	# Handles SIMPLEGET requests.
	def do_SIMPLEGET(self):
		self.log.debug('SIMPLEGET request received')

		pass

	##
	# Handles NOTIFY requests.
	def do_NOTIFY(self):
		self.log.debug('NOTIFY request received')

		pass
	
	##
	# Handles SUBSCRIBE requests.
	def do_SUBSCRIBE(self):
		self.log.debug('SUBSCRIBE request received')

		pass

	##
	# Handles UNSUBSCRIBE requests.
	def do_UNSUBSCRIBE(self):
		self.log.debug('UNSUBSCRIBE request received')

		pass
	
	##
	# Handles MPOST requests.
	def do_MPOST(self):
		self.log.debug('MPOST request receieved')

		pass

