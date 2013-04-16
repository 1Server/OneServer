## @package oneserver
# This class stores persistent data that needs to be pass around to various other modules
# It is designed so it is a singleton that can store any global values that are needed but
# not have any internal dependencies
class OneServerManager(object):
	##
	# The instance of this singleton
	_instance = None

	##
	# Overides the __new__ of object to make sure we only have one instance
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(OneServerManager, cls).__new__(
					cls, *args, **kwargs)
		return cls._instance

	##
	# MIME for containers
	CONTAINER_MIME = "object.container.storageFolder"
