#!/usr/bin/env python

## @package oneserver
# This is the core part of the server. Start up and normal runtime functions
# get handled here.

from configuration.configManager import ConfigManager
from pluginManager import PluginManager
from dlna import DLNAService
import tcs
from vfs import VirtualFileSystem
from manager import OneServerManager
from scheduler import TaskScheduler

import logging

## Core class for the server.
class OneServer(object):
	instance = None

	## Creates a OneServer object.
	def __init__(self):
		#Create a manager for different instances.
		self.manager = OneServerManager()
		
		# Load the configurations.
		self.config = ConfigManager()
		self.config.loadConfigFile()
		self.manager.config = self.config

		# Start logging.
		self.log = logging.getLogger('oneserver')
		logHandler = logging.StreamHandler()
		logHandler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
		self.log.addHandler(logHandler)
		self.log.setLevel(logging.DEBUG)
		# TODO: Add file handler for writing to a file.
		self.manager.log = self.log

		self.log.info('Preparing the OneServer media server to start...')
		
		# Start plugin loader.
		self.pluginManager = PluginManager()
		self.manager.pluginManager = self.pluginManager
		self.pluginManager.loadEnablePluginList(self.config)
		self.pluginManager.loadPlugins()
		self.pluginManager.enableAdminPlugins()
		self.pluginManager.enableStoragePlugins()
		self.pluginManager.enableUtilityPlugins()

		self.storagePlugins = self.pluginManager.getStoragePlugins()
		self.adminPlugins = self.pluginManager.getAdminPlugins()
		self.utilityPlugins = self.pluginManager.getUtilityPlugins()
		
		# Start scheduler.
		self.log.debug('Starting task scheduler...')

		self.scheduler = TaskScheduler()
		self.manager.scheduler = self.scheduler
		self.scheduler.startScheduler()

		self.log.debug('Task scheduler started.')
		
		# Start VFS
		self.log.debug('Starting virtual file system...')

		#TODO: Load loaded Storage plugins into vfs
		self.vfs = VirtualFileSystem()
		plugins = self.storagePlugins
		
		for plugin in plugins:
			if plugin != None:
				self.log.debug("Loading Storage Plugin : " + plugin)
			self.vfs.loadDataSource(plugin)

		self.log.debug('Virtual file system started.')
		
		# Start DLNA
		self.log.debug('Preparing DLNA service...')

		self.dlna = DLNAService(self.config)
		self.manager.dlna = self.dlna.dlna

		self.log.debug('DLNA service ready.')
		
		#Temporary Content Store
		self.log.debug('Creating temporary content store...')

		tcsRoot = tcs.populate(["samples/sample.mp4","samples/sample.mp3", "samples/movie.mp4", "samples/sample.jpg"])
		self.manager.rootEntry.addChild(tcsRoot)
		tcsRoot.parent = self.manager.rootEntry

		self.log.debug('Temporary content store ready.')

		# Set the singleton instance.
		OneServer.instance = self

	##
	# Starts the server.
	def start(self):
		self.log.info('Starting DLNA service...')
		self.dlna.start()
		self.log.info('DLNA service started.')

	##
	# Stops the server.
	def stop(self):
		self.log.info('Saving configuration...')
		self.config.saveConfigFile()

		self.log.info('Stopping DLNA service...')
		self.dlna.stop()
		self.scheduler.stopScheduler()
		self.log.info('DLNA service stopped.')

if __name__ == '__main__':
	server = OneServer()
	server.start()
	run = True
	while(run):
		cmd = raw_input("What do you want to do? ")
		
		if ("stop" or "Stop") in cmd:
			run = False
		else:
			server.log.info('Unknown command')

	server.stop()

