##
# @author Benjamin Ebert
# @date 10-15-12
# @version 1.0
from configError import LoadingError

import os
import yaml

##
# A helper class that all it does is keep track of the file path you want to load the config from
# and load that config file with YAML
class ConLoader(object):
	
	##
	# Holds the Filename and path of the config file
	fileName = 'config.yaml'

	##
	# Constructs a ConLoader
	#
	# @param fileName - the name of the file
	def __init__(self, fileName):
		self.fileName = fileName

	##
	# Loads in the config file
	#
	# @return Dictionary that contains the config info or None if no file is found
	def loadFile(self):
		# Check if the file exists and if not then create it.
		if not os.path.exists(self.fileName):
			with open(self.fileName, 'w') as f:
				f.write('')

		config = None
		try:
			config = yaml.load(file(self.fileName, 'r'))
		except yaml.YAMLError, exc:
			raise LoadingError('Yaml Error', 'loadFile')
		return config
		
	##
	# Sets the file name and path to the config file
	#
	# @param fileName - the name of the file
	def setFileName(self, fileName):
		self.fileName = fileName

