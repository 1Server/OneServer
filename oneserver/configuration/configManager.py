##
# @author Benjamin Ebert
# @date 10-15-12
# @version 1.0
from loader import ConLoader
from unloader import ConDumper
from configError import *

##
# A Manager that controls writing and reading a configuration file.
class ConfigManager(object):

	##
	# Represents the Dictionary that holds all the config data
	configHolder = None

	##
	# Separator for the section names.
	sectionSeparator = '.'

	##
	# The root level of the configuration file.
	root = 'Core'

	##
	# The plugin section of the configuration file.
	pluginsNode = 'Plugins'

	##
	# The plugin path in the config file.
	pluginPath = root + sectionSeparator + pluginsNode
	
	##
	# Constructs a configManager
	def __init__(self):
		pass
	
	##
	# Loads in a file through the loader.py class
	#
	# @param fileName Filename/path for the config file you want to load
	def loadConfigFile(self, fileName='config.yaml'):
		load = ConLoader(fileName)
		self.configHolder = load.loadFile()

		if self.configHolder == None:
			self.configHolder = dict()
		
	##
	# Checks to see if a plugin is enabled by looking to see if it is in the plugin list in the main section
	#
	# @param pluginName - Name of the plugin
	#
	# @return true if the plugin is enabled, false otherwise
	def isPluginEnabled(self, pluginName):
		return pluginName in self.getFromConfig(self.configHolder, pluginPath)
		
	##
	# Gets the plugin specified's config data
	# 
	# @param pluginName Name of the plugin that you want to get the config data for
	#
	# @return Dictionary of the plugin's config data or None if it can't find the plugin in the config file
	def getPluginConfig(self, pluginName):
		if pluginName in self.configHolder:
			return self.configHolder[pluginName]
		else:
			return None
			
	##
	# Gets data from the Core config Dictionary
	#
	# @param key A string seperated by '.' that hold the path to the required data
	#
	# @return returns the value for the specified key or returns None if it can't find the key
	def getCoreConfig(self, key):
		try:
			value = self.getFromConfig(self.configHolder, key)

			return value
		except ValueError:
			raise ConfigManagerError('ValueError', 'configManager')
			return None

	##
	# Gets a core configuration value and if the value isn't present a default value
	# is set automatically.
	#
	# @param key - the key for retrieving the value
	# @param default - the default value
	#
	# @return returns the value for the given key
	def getCoreConfigWithDefault(self, key, default):
		value = self.getCoreConfig(key)
		if value == None:
			self.setCoreConfig(key, default)
			return default

		return value
			
	##
	# Saves the config Dictionary to a yaml file by using the unloader.py
	#
	# @param fileName FileName/path for the config file you want to write to
	def saveConfigFile(self, fileName='config.yaml'):
		dump = ConDumper(fileName)
		dump.dumpFile(self.configHolder)
	
	##
	# Sets value passed in to the key specified
	#
	# @param key A string delimented by '.' that contains the path to the key in the Dictionary.
	# @param data value you want to set to the key
	def setCoreConfig(self, key, data):
		try:
			if self.sectionSeparator in key:
				substr = key[:key.rfind(sectionSeparator)]
				valueKey = key[key.rfind(sectionSeparator):]

				section = getFromConfig(self.configHolder, substr)
				section[valueKey] = data
			else:
				self.configHolder[key] = data
		except ValueError:
			raise ConfigManagerError('ValueError', 'configManager')
	
	##
	# Sets the Plugin Dictionary passed in to the spot in the config dictionary
	#
	# @param pluginName Name of the plugin of the Dictionary you are passing in
	# @param pluginDict Dictionary containing the info for the plugin
	def setPluginConfig(self, pluginName, pluginDict):
		self.configHolder[pluginName] = pluginDict
		
	##
	# Removes plugin section and data from the config data
	#
	# @param pluginName Name of the plugin that you want to remove from the config file
	def removePluginConfig(self, pluginName):
		if pluginName in self.configHolder:
			del self.configHolder[pluginName]

			
	##
	# Removes the Plugin from the enablePlugin list
	#
	# @param pluginName Name of the plugin to delete from the list
	def removePlugin(self, pluginName):
		if ConfigManager.isPluginEnabled(pluginName):
			del self.getFromConfig(self.configHolder, pluginPath)[pluginName]
		
	##
	# Gets a section or value from the configuration file.
	#
	# @param parentSection the parent section
	# @param sectionPath the path to the section or value
	#
	# @return the configuration section/value or None if it does not exist
	def getFromConfig(self, parentSection, sectionPath):
		if not parentSection or not sectionPath:
			return None

		# Split the section path into the different sections and then iterate to the desired section.
		sections = sectionPath.split(self.sectionSeparator)
		parent = parentSection
		for sectionName in sections:
			if not sectionName in parent:
				return None

			parentSection = section = parent[sectionName]

		return section

