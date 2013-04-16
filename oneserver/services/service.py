from manager import OneServerManager
from metadata import WebFile
import wrappers.upnp.upnptools
from wrappers.upnp.ixml import ixmlNode_getNextSibling,ixmlNode_getFirstChild,ixmlNode_getNodeName,ixmlNode_getNodeValue

from StringIO import StringIO

##
# A service provides handling for actions. Each service implementation
# handles different actions.
class Service:
	##
	# Represents the ObjectID argument.
	ARG_OBJECT_ID = 'ObjectID'

	##
	# Represents the ContainerID argument.
	ARG_CONTAINER_ID = 'ContainerID'

	##
	# Constructs a service with the givenid, type, and supported actions.
	def __init__(self,id_t,type_t,actions):
		self.id_t = id_t
		self.type_t = type_t
		self.actions = actions

	##
	# Handles creating a WebFile for things in memory
	#
	# @param fullpath - the full path to the file
	# @param description - the file description
	#
	# @return the file reference
	@staticmethod
	def getFileMemory(fullpath, description):
		_file = WebFile(fullpath, 0, StringIO(description), None)
		OneServerManager().log.debug('Allocated: ' + str(_file.path))

		return _file

	##
	# Adds a key value pair to an action response.
	#
	# @return true on success
	@staticmethod
	def upnpAddResponse(event, key, value):
		if event is None or event['status'] is False or key is None or value is None:
			return False
		
		res = wrappers.upnp.upnptools.UpnpAddToActionResponse(event['request'].ActionResult,
							event['request'].ActionName,
							event['service']['type_t'],
							key,
							value)

		return res == wrappers.upnp.upnp.UPNP_E_SUCCESS

	##
	# Gets a string for the given key.
	#
	# @param request A request object
	# @param key A key to value
	#
	# @return a string
	@staticmethod
	def upnpGetString(request, key):
		if not request or not request.ActionRequest or not key:
			return None

		manager = OneServerManager()
		node = request.ActionRequest.contents.n
		if not node:
			manager.log.error('Invalid action request document.')
			return None

		node = ixmlNode_getFirstChild(node)
		if not node:
			manager.log.error('Invalid action request document.')
			return None

		node = ixmlNode_getFirstChild(node)
		while node:
			if key == ixmlNode_getNodeName(node).value:
				node = ixmlNode_getFirstChild(node)
				return ixmlNode_getNodeValue(node).value if node else ''

			node = ixmlNode_getNextSibling(node)

		manager.log.error('Missing action request argument {1}'.format(None, key))
		return None

	##
	# Gets a 4 byte unsigned integer for the given key.
	#
	# @param request A request object
	# @param key A key to a value
	#
	# @return A 32bit unsigned integer
	@staticmethod
	def upnpGetUI4(request, key):
		if not request or not key:
			return 0

		value = Service.upnpGetString(request, key)
		if not value and key == Service.ARG_OBJECT_ID:
			value = Service.upnpGetString(request, Service.ARG_CONTAINER_ID)

		return int(value) if value else 0
	
	##
	# Gets the protocol for the mime type.
	@staticmethod
	def mimeGetProtocol(mimeType):
		if not mimeType:
			return None
		
		return mimeType.mime_protocol + '*'

