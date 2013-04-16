##
# This module provides a VirtualFileSystem from which data from many plugins can be accessed seemlessly and like if it was a real filesystem

from plugin.interface import IStoragePlugin
from manager import OneServerManager
from entry import Entry

##
# This class represents a virtual filesystem.  The filesystem will be composed of various plugins that are loaded in which will
# create the top level directory structure.  Below that it is up to the plugins for their own organization.  All operations on this
# class will extend to the plugin versions where appropriate automatically.
#
# In this class a data source is the name used for a IStoragePlugin class.  This makes it more clear what their purpose is in this context
#
# Each path is a standard Unix styled path aka /this/is/a/path/to/a/file.  The / is the root which consists of a list of loaded data sources
class VirtualFileSystem(object):
	
	##
	# Used for indicating a file
	FILE = 1
	
	## 
	# Used for indicating a directory
	DIR  = 2
	
	##
	# Init function for the VirtualFileSystem
	#
	# @param plugins An optional list of plugins to load at startup
	def __init__(self):
		self.dataSources = {}
		self.vfsRoot = Entry("/",OneServerManager().CONTAINER_MIME, None, [], "OneServer", "0", -1, None)
		OneServerManager().rootEntry = self.vfsRoot
		OneServerManager().uploadRoot = Entry("/upload",OneServerManager().CONTAINER_MIME, self.vfsRoot, [], "Upload", "0", -1, None)
			
		
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
		self.checkPath(path)
		
		#Handle the special case of get('/')
		if path == '/':
			raise DirectoryError("Tried to get a directory")
			
		#Get the source to call
		source = path.split('/')[1]
		
		entry = self.dataSources[source].get(path)
		
		return entry
	
	##
	# This function functions similar to ls. 
	# If a path to a directory is given, all of the entries in that directory will be returned.
	# If it is given the path to a file, it will return a list with one entry which is that file.
	# If any subdirectories are listed, their path will be prefixed with a d such as "d/path/to/dir".
	#
	# @param path The path to list
	# 
	# @return A list of strings in the directory
	#
	# @throws EntryNotFoundError If the given path does not exist
	def list(self, path):
		self.checkPath(path)
		
		#Handle the special case of list('/')
		if path == '/':
			retVal = []
			for source in self.dataSources.keys():
				retVal.append("d/{0}".format(source))
			
			return retVal
			
		#Get the source to call
		source = path.split('/')[1]
		
		return self.dataSources[source].list(path)
		
	##
	# This function takes an Entry and adds it to the given data source.
	#
	# @param entry The Entry to add
	# @param source The source to add it to
	#
	# @return A new entry
	#
	# @throws UploadNotSupportedError If uploading to the given source is not supported
	def put(self, entry, source):
		if source not in self.dataSources.keys():
			raise ValueError("Given source does not exist")
			
		return self.dataSources[source].put(entry)
		
	##
	# This function searches through all sources to find matching entries
	#
	# @param metadata A dict of metadata which consists of keys such as "artist" or "genre".  As many as possible will be matches, and each additional value will be considered an AND
	#
	# @return A list of paths to matching files
	def search(self, metadata):
		if metadata is None or len(metadata) == 0:
			raise ValueError("Invalid metadata given")
		
		matches = []
		for source in self.dataSources:
			matches.extend(self.dataSources[source].search(metadata))
			
		return matches
		
	##
	# Loads the given data source into the VirtualFileSystem
	#
	# @param source The source to add, must extend IStoragePlugin
	#
	# @throw ValueError if the sources does not extend IStoragePlugin
	def loadDataSource(self, source):
		if not isinstance(source, IStoragePlugin):
			raise ValueError("source did not extend IStoragePlugin")
		
		self.dataSources[source.name] = source
		source.tree.parent = self.vfsRoot
		self.vfsRoot.addChild(source.tree)
		
	##
	# Unloads the given data source from the VirtualFileSystem
	# 
	# @param name The name of the source to unload
	def unloadDataSource(self, name):
		if name == None or name not in self.dataSources.keys():
			raise ValueError("Invalid name")
		self.vfsRoot.removeChild(self.dataSources[name].tree)
		del self.dataSources[name]
		
		
	##
	# This function check to see if a path is valid.  
	# A valid path is a string that is not empty and starts with / or d/
	#
	# @param path The path to check
	#
	# @return Returns FILE if it is a file path and DIR if it is a directory
	@staticmethod
	def checkPath(path):
		if path is None:
			raise ValueError("Path must not be None")
		if path == "":
			raise ValueError("Path must not be empty")
		
		if path[0] == "/":
			return VirtualFileSystem.FILE
		elif path[0:2] == "d/":
			return VirtualFileSystem.DIR
		else:
			raise ValueError("Not a valid path " + path)
			



##
# Occurs when a Directory is encountered when it shouldn't be
class DirectoryError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
##
# Occurs when an Entry is not found
class EntryNotFoundError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
##
# Occurs when trying to upload to a source that doesn't support it
class UploadNotSupportedError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
