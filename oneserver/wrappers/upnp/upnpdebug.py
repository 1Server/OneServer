from manager import OneServerManager

import sys
try:
	from ctypes import cdll
	from ctypes import c_char_p,c_int,c_long
	from ctypes import POINTER
	from ctypes.util import find_library
except ImportError:
	OneServerManager().log.error('Library CTypes not found.')
	sys.exit()

from upnp import UPNP_E_SUCCESS
from wrappers.cfile import FILE

##
# The user has the option to select 4 different types of debugging levels, see UpnpSetLevel.
# The critical level will show only those messages which can halt the normal processing of
# the library, like memory allocation errors. The remaining three levels are just for debugging
# purposes. Packet level will display all incoming and outgoing packets that are flowing between
# the control point and the device. Info Level displays the other important operational information
# regarding the working of the library. If the user selects All, then the library displays
# all the debugging information that it has.
class Upnp_Module:
	SSDP  = 0
	SOAP  = 1
	GENA  = 2
	TPOOL = 3
	MSERV = 4
	DOM   = 5
	API   = 6
	HTTP  = 7

class Dbg_Module(Upnp_Module):
	pass

class Upnp_LogLevel_e:
	UPNP_CRITICAL = 0
	UPNP_PACKET   = 1
	UPNP_INFO	 = 2
	UPNP_ALL	  = 3

class Upnp_LogLevel(Upnp_LogLevel_e):
	pass

DEBUG = 0

UPNP_DEFAULT_LOG_LEVEL = Upnp_LogLevel.UPNP_ALL

DebugLib = cdll.LoadLibrary(find_library('upnp'))

DebugLib.UpnpInitLog.restype = c_int

DebugLib.UpnpSetLogLevel.argtypes = [Upnp_LogLevel]

DebugLib.UpnpSetLogFileNames.argtypes = [c_char_p, c_char_p]

DebugLib.UpnpGetDebugFile.restype = POINTER(FILE)
DebugLib.UpnpGetDebugFile.argtypes = [Upnp_LogLevel, Dbg_Module]

DebugLib.DebugAtThisLevel.restype = c_int
DebugLib.DebugAtThisLevel.argtypes = [Upnp_LogLevel, Dbg_Module]

DebugLib.UpnpPrintf.restype = c_int
DebugLib.UpnpPrintf.argtypes = [Upnp_LogLevel, Dbg_Module, c_char_p, c_int, c_char_p]

DebugLib.UpnpDisplayBanner.argtypes = [POINTER(FILE), POINTER(c_char_p), c_long, c_int]

DebugLib.UpnpDisplayFileAndLine.argtypes = [POINTER(FILE), c_char_p, c_int]

##
# This function initializes the log files.
#
# @return -1 if fails, UPNP_E_SUCCESS if success.
def UpnpInitLog():
	if DEBUG == 1:
		return DebugLib.UpnpInitLog()
	else:
		return UPNP_E_SUCCESS

##
# This function sets the log level.
#
# @param log_level the log level
def UpnpSetLogLevel(log_level):
	if DEBUG == 1:
		DebugLib.UpnpSetLogLevel(log_level)

##
# This function closes the log files.
def UpnpCloseLog():
	if DEBUG == 1:
		DebugLib.UpnpCloseLog()

##
# This function takes the buffer and writes the buffer in the file as per the requested banner.
def UpnpSetLogFileNames(ErrFileName, InfoFileName):
	if DEBUG == 1:
		DebugLib.UpnpSetLogFileNames(ErrFileName, InfoFileName)

##
# This function checks if the module is turned on for debug and returns the file descriptor
# corresponding to the debug level.
#
# @param level The level of the debug logging. It will decide whether debug statements will
# go to standard output, or any of the log files.
# @param module Debug will go in the name of this module.
#
# @return None if the module is turned off for debug and a file desciptor otherwise
def UpnpGetDebugFile(level, module):
	return DebugLib.UpnpGetDebugFile(level, module) if DEBUG == 1 else None

##
# This function returns true if debug output should be done in this module.
#
# @param DLevel The level of the debug logging.
# @param Module Debug will go in the name of this module.
#
# @return int
def UpnpPrintf(DLevel, Module, DbgFileName, DbgLineNo, FmtStr, *args):
	if DEBUG == 1:
		DebugLib.UpnpPrintf(DLevel, Module, DbgFileName, DbgLineNo, FmtStr, *args)

##
# This function takes the buffer and writes the buffer in the file as per the requested banner.
#
# @param fd the file descriptor where the banner will be written
# @param lines the buffer that will be written
# @param size size of the buffer
# @param starLength this parameter provides the width of the banner
def UpnpDisplayBanner(fd, lines, size, starLength):
	if DEBUG == 1:
		UpnpDisplayBanner(fd, lines, size, starLength)

##
# This function writes the file name and file number from where debug statement is coming to the log file.
#
# @param fd File descriptor where line number and file name will be written
# @param DbgFileName name of the file
# @param DbgLineNo line number of the file
def UpnpDisplayFileAndLine(fd, DbgFileName, DbgLineNo):
	if DEBUG == 1:
		UpnpDisplayFileAndLine(fd, DbgFileName, DbgLineNo)
