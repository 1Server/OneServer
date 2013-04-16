from manager import OneServerManager
from entry import Entry

import sys

try:
	from pyutilib.component.core import Interface
except ImportError:
	OneServerManager().log.error('pyutilib.component.core not found')
	sys.exit()

##
# 
class OneServerPlugin(Interface):
	##
	# This function is called when the plugin is enabled by the plugin manager and does 
	# any initialization the plugin needs.
	def enable(self):
		raise NotImplementedError( "Should have implemented this" )
	
	##
	# This function is called when the plugin is disabled by the plugin manager and does
	# any cleanup the plugin needs
	def disable(self):
		raise NotImplementedError( "Should have implemented this" )
	
	##
	# This function is called when the plugin is loaded and does any immediate initialization
	# needed
	def load(self):
		raise NotImplementedError( "Should have implemented this" )
	
	##
	# This function is called when the plugin is loaded and does any remaining cleanup
	# needed
	def unload(self):
		raise NotImplementedError( "Should have implemented this" )

##
# The Interface for the Administration Plugins
# These plugins aid the user in administering their OneServer
class IAdministrationPlugin(OneServerPlugin):
	
	##
	# Constructs a IAdministrationPlugin
	def __init__(self):
		pass

##
# The Interface for the Storage Plugins
# These plugins provide a new source of media to the VFS
class IStoragePlugin(OneServerPlugin):
	CONTAINER_MIME = "object.container.storageFolder"
	##
	# Constructs an IStoragePlugin
	# Plugins MUST call this __init__ and have a tree attribute with its root Entry
	# The plugin should also construct its tree here
	#
	# @param name The Human-Read
	def __init__(self, name):
		self.name = name
	
	
	##
	# Gets the Entry given by the path.  Raises a DirectoryException if a directory is given
	#
	# @param path The path to the wanted Entry
	#
	# @return The Entry at the path given
	#
	# @throws DirectoryError If a directory path is given
	# @throws EntryNotFoundError If the path does not lead to an Entry
	def get(self, path):
		raise NotImplementedError( "Should have implemented this" )
		
	##
	# This function functions similar to ls. 
	# If a path to a directory is given, all of the entries in that directory will be returned.
	# If it is given the path to a file, it will return a list with one entry which is that file.
	# If any subdirectories are listed, their path will be prefixed with a d such as "d/path/to/dir".
	#
	# @param path The path to list
	#
	# @throws EntryNotFoundError If the given path does not exist
	def list(self, path):
		raise NotImplementedError( "Should have implemented this" )
		
	##
	# This function takes an Entry and adds the entity to the given data source.
	#
	# @param entry The Entry to add
	#
	# @throws UploadNotSupportedError If uploading to the given source is not supported
	def put(self, entry):
		raise NotImplementedError( "Should have implemented this" )
		
	##
	# This function searches through all sources to find matching entries
	#
	# @param metadata A dictionary of metadata which consists of keys such as "artist" or "genre". As many as possible will be matches, and each additional value will be considered an AND
	def search(self, metadata):
		raise NotImplementedError( "Should have implemented this" )

##
# The Interface for the Utility Plugins
# This is for plugins that do not fall under the category of Storage or Administration plugins
class IUtilityPlugin(OneServerPlugin):
	
	##
	# Constructs a IUtilityPlugin
	def __init__(self):
		pass

