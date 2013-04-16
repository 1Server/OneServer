##
# @author Benjamin Ebert
# @date 10-15-12
# @version 1.0

##
# Default Error Class
class ConfigError(Exception):
	##
	# Generates an error string.
	def __str__(self):
		lines = []
		if self.point is not None:
			lines.append(self.point)
		lines.append(' had an error occur: ')
		if self.value is not None:
			lines.append(self.value)
		return repr('\n'.join(lines))

##
# This class is for all the errors that deal with loading a Yaml file
class LoadingError(ConfigError):
	
	##
	# Constructs a LoadingError with value and point
	def __init__(self, value, point):
		self.point = point
		self.value = value

##
# This class is for all the errors that deal with dumping a Yaml file
class DumpingError(ConfigError):

	##
	# Constructs a DumpingError with value and point
	def __init__(self, value, point):
		self.point = point
		self.value = value
		
##
# This class is for all the errors that deal with the config manager		
class ConfigManagerError(ConfigError):
	
	##
	# Constructs a ConfigManagerError with value and point
	def __init__(self, value, point):
		self.point = point
		self.value = value
