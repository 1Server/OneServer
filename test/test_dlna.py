import unittest
from configuration.configManager import ConfigManager
#from mock import Mock

from oneserver.dlna import DLNAService
from manager import OneServerManager

class TestDLNAService(unittest.TestCase):
	
	def setUp(self):
		self.manager = OneServerManager()
		self.config = ConfigManager()
		
		
	def test_DLNAServiceCreation(self):
		with self.assertRaises(ValueError):
			DLNAService(None)
		
		
	def test_start(self):
		pass
		
	def test_stop(self):
		pass
		
	def test_deviceEventHandler(self):
		pass
		
	def test_handleActionRequest(self):
		pass
		
	def test_findServiceAction(self):
		pass

if __name__ is "__main__":
	unittest.main()


