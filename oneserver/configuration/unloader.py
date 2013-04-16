##
# @author Benjamin Ebert
# @date 10-15-12
# @version 1.0
from configError import DumpingError
import yaml

##
# A helper class that all it does is keep track of the file path you want to save the config to
# and save a dictionary to that config file
class ConDumper(object):
	
	##
	# Holdes the Filename and path of the config file
	fileName = 'config.yaml'
	
	##
	# Constructs a ConDumper
	#
	# @param fileName - the name of the config file
	def __init__(self, fileName):
		self.fileName = fileName
	
	##
	# Dumps a dictionary a config file
	#
	# @param config - The dictionary you want to save
	def dumpFile(self, config):
		try:
			stream = file(self.fileName, 'w')
			yaml.dump(config, stream, default_flow_style=False)
		except yaml.YAMLError, exc:
			raise DumpingError('Yaml Error', 'dumpFile')
		
	##
	# Sets the file name and path to the config file
	#
	# @param fileName - the name of the file
	def setFileName(self, fileName):
		self.fileName = fileName
