##
# @author Benjamin Ebert
# @date 11-5-12
# @version 1.0
from configuration.configManager import ConfigManager
from plugin.interface import IAdministrationPlugin
from plugin.interface import IStoragePlugin
from plugin.interface import IUtilityPlugin
from pkg_resources import find_distributions
from manager import OneServerManager
import sys


try:
	from pyutilib.component.core import ExtensionPoint,PluginEnvironment,PluginFactory,CreatePluginFactory
	from pyutilib.component.loader import PluginGlobals
except ImportError:
	print 'PyUtilib.component.core or PyUtilib.component.loader not found'
	sys.exit()

##
# This class controls and manages plugins that are added to the server
class PluginManager(object):

	##
	# The instance of this singleton
	_instance = None
	
	##
	# Overides the __new__ of PluginManager to make sure we only have one instance
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(PluginManager, cls).__new__(cls, *args, **kwargs)
		return cls._instance
	
	##
	# Initializes PluginManager when it is created
	def __init__(self):
		self.enabledPluginList = None
		self.env = PluginEnvironment("OneServer")
		PluginGlobals.push_env(self.env)

		
		self.eggLoader = PluginFactory("EggLoader",namespace="project1",env='pca')
	#	PluginGlobals.env().load_services(path='./plugin/p',auto_disable=False) #Needs to be changed after this works
		PluginGlobals.env().load_services(path=sys.path,auto_disable=False) #Needs to be changed after this works
		
		self.administratorPlugins = ExtensionPoint(IAdministrationPlugin)
		self.storagePlugins = ExtensionPoint(IStoragePlugin)
		self.utilityPlugins = ExtensionPoint(IUtilityPlugin)
	
	##
	# Loads Plugin List from configManager
	#
	# @param configManager ConfigurationManager object
	def loadEnablePluginList(self, configManager):
		OneServerManager().log.debug('Loaded Enabled Plugin List...')
		self.enabledPluginList = configManager.getCoreConfig('Plugins')
		
	##
	# Enables Plugin in the config file
	#
	# @param pluginName Plugin's Name
	# @param configManager ConfigurationManager object
	def enablePluginInConfig(self, pluginName, configManager):
		key = 'Plugins.'+pluginName
		configManager.setCoreConfig(key, pluginName)
		
	##
	# Disables Plugin in config file
	#
	# @param pluginName Plugin's Name
	# @param configManager ConfigurationManager object
	def disablePluginInConfig(self, pluginName, configManager):
		if pluginName in self.enabledPluginList:
			del self.enabledPluginList[pluginName]
			configManager.removePlugin(pluginName)
			
	##
	# Enables Admin Plugins that are supposed to be enabled
	def enableAdminPlugins(self):
		if(self.enabledPluginList!=None):
			for enabledPlugin in self.enabledPluginList:
				self.enableAdminPlugin(enabledPlugin)
	
	##
	# Enables the specified admin Plugin
	#
	# @param pluginName Name of plugin to enable
	def enableAdminPlugin(self, pluginName):
		if(self.enabledPluginList!=None):
			if self.administratorPlugins(pluginName):
				self.env.activate(self.administratorPlugins(pluginName))
				self.administratorPlugins(pluginName).enable()
	
	##
	# Enables Storage Plugins that are suppose to be enabled
	def enableStoragePlugins(self):
		if(self.enabledPluginList!=None):
			for enabledPlugin in self.enabledPluginList:
				self.enableStoragePlugin(enabledPlugin)
	
	##
	# Enables the specified storage Plugin
	#
	# @param pluginName Name of plugin to enable
	def enableStoragePlugin(self, pluginName):
		if(self.enabledPluginList!=None):
			if self.storagePlugins(pluginName):
				OneServerManager().log.debug('enable storage plugin...')
				self.env.activate(self.storagePlugins(pluginName))
				self.storagePlugins(pluginName).enable()
	
	##
	# Enables Utility Plugins that are supposed to be enabled
	def enableUtilityPlugins(self):
		if(self.enabledPluginList!=None):
			for enabledPlugin in self.enabledPluginList:
				self.enableUtilityPlugin(enabledPlugin)
	
	##
	# Enables the specified utility Plugin
	#
	# @param pluginName Name of plugin to enable
	def enableUtilityPlugin(self, pluginName):
		if(self.enabledPluginList!=None):
			if self.utilityPlugins(pluginName):
				self.env.activate(self.utilityPlugins(pluginName))
				self.utilityPlugins(pluginName).enable()
	
	##
	# Disables the specified Admin Plugin
	#
	# @param pluginName Name of plugin to be disabled
	def disableAdminPlugin(self, pluginName):
		if self.administratorPlugins(pluginName):
			self.administratorPlugins(pluginName).disable()
			self.env.deactivate(self.administratorPlugins(pluginName))
	
	##
	# Disables the specified Utility Plugin
	#
	# @param pluginName Name of plugin to be disabled
	def disableUtilityPlugin(self, pluginName):
		if self.utilityPlugins(pluginName):
			self.utilityPlugins(pluginName).disable()
			self.env.deactivate(self.utilityPlugins(pluginName))
	
	##
	# Disables the specified Storage Plugin
	#
	# @param pluginName Name of plugin to be disabled
	def disableStoragePlugin(self, pluginName):
		if self.storagePlugins(pluginName):
			self.storagePlugins(pluginName).disable()
			self.env.deactivate(self.storagePlugins(pluginName))
	
	##
	# Returns a true or false depending if the plugin is enabled
	#
	# @param pluginName Name of plugin
	def isPluginEnabled(self, pluginName):
		if self.administratorPlugins(pluginName):
			return self.env.active_services(self.administratorPlugins(pluginName))
		elif self.storagePlugins(pluginName):
			return self.env.active_services(self.storagePlugins(pluginName))
		elif self.utilityPlugins(pluginName):
			return self.env.active_services(self.utilityPlugins(pluginName))
	
	
	##
	# Reloads the plugin specified
	#
	# @param pluginName Name of plugin to be reloaded
	def reloadPlugin(self, pluginName):
		plugin = None
		if self.administratorPlugins(pluginName):
			plugin = self.administratorPlugins(pluginName)
		elif self.storagePlugins(pluginName):
			plugin = self.storagePlugins(pluginName)
		elif self.utilityPlugins(pluginName):
			plugin = self.utilityPlugins(pluginName)
		
		if plugin != None:
			plugin.unload()
			plugin.load()
		else:
			raise ValueError("{0} not found!".format(pluginName))
	
	##
	# Calls the load method in the plugin
	#
	# @param pluginName Name of plugin
	def loadPlugin(self, pluginName):
		plugin = None
		OneServerManager().log.debug('Loading Plugin...')
		if self.administratorPlugins(pluginName):
			plugin = self.administratorPlugins(pluginName)
			OneServerManager().log.debug('Loaded Administration Plugin...')
		elif self.storagePlugins(pluginName):
			plugin = self.storagePlugins(pluginName)
			OneServerManager().log.debug('Loaded Storage Plugin...')
		elif self.utilityPlugins(pluginName):
			plugin = self.utilityPlugins(pluginName)
			OneServerManager().log.debug('Loaded Utility Plugin...')
		
		if plugin != None:
			plugin.load()
		else:
			raise ValueError("{0} not found!".format(pluginName))
	
	##
	# Calls the unload method in the plugin and removed it from the holder
	#
	# @param pluginName Name of plugin
	def unloadPlugin(self, pluginName):
		plugin = None
		if self.administratorPlugins(pluginName):
			plugin = self.administratorPlugins(pluginName)
		elif self.storagePlugins(pluginName):
			plugin = self.storagePlugins(pluginName)
		elif self.utilityPlugins(pluginName):
			plugin = self.utilityPlugins(pluginName)
		
		if plugin != None:
			plugin.unload()
		else:
			raise ValueError("{0} not found!".format(pluginName))
			
	##
	# Loads in all plugins
	def loadPlugins(self):
		for plugin in find_distributions('./plugin/p'):
			sys.path.append(plugin.location)
	#		OneServerManager().log.debug(plugin)
		OneServerManager().log.debug('Loading Plugins...')
	#	self.eggLoader.load(PluginGlobals.env(),'./plugin/p',disable_re=False,name_re="*")
		
		
	##
	# Return Admin plugins
	def getAdminPlugins(self):
		return self.administratorPlugins
	##
	# Return Storage plugins
	def getStoragePlugins(self):
	#	OneServerManager().log.debug('Getting Storage Plugins')
		OneServerManager().log.debug(PluginGlobals.pprint())
	#	OneServerManager().log.debug(self.storagePlugins())
		for plugin in self.storagePlugins:
			OneServerManager().log.debug(plugin)
			plugin.load()
		return self.storagePlugins
	##
	# Return Utility plugins
	def getUtilityPlugins(self):
		return self.utilityPlugins
