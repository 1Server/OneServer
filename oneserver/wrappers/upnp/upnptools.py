from manager import OneServerManager

import sys
try:
	from ctypes import cdll
	from ctypes import c_char_p,c_int
	from ctypes import POINTER
	from ctypes.util import find_library
except ImportError:
	OneServerManager().log.error('Library CTypes not found.')
	sys.exit()

from wrappers.upnp.ixml import IXML_Document

ToolsLib = cdll.LoadLibrary(find_library('upnp'))

ToolsLib.UpnpResolveURL.restype = c_int
ToolsLib.UpnpResolveURL.argtypes = [c_char_p, c_char_p, c_char_p]

ToolsLib.UpnpMakeAction.restype = POINTER(IXML_Document)
ToolsLib.UpnpMakeAction.argtypes = [c_char_p, c_char_p, c_int, c_char_p]

ToolsLib.UpnpAddToAction.restype = c_int
ToolsLib.UpnpAddToAction.argtypes = [POINTER(POINTER(IXML_Document)), c_char_p, c_char_p, c_char_p, c_char_p]

ToolsLib.UpnpMakeActionResponse.restype = POINTER(IXML_Document)
ToolsLib.UpnpMakeActionResponse.argtypes = [c_char_p, c_char_p, c_int, c_char_p]

ToolsLib.UpnpAddToActionResponse.restype = c_int
ToolsLib.UpnpAddToActionResponse.argtypes = [POINTER(POINTER(IXML_Document)), c_char_p, c_char_p, c_char_p, c_char_p]

ToolsLib.UpnpAddToPropertySet.restype = c_int
ToolsLib.UpnpAddToPropertySet.argtypes = [POINTER(POINTER(IXML_Document)), c_char_p, c_char_p]

ToolsLib.UpnpCreatePropertySet.restype = POINTER(IXML_Document)
ToolsLib.UpnpCreatePropertySet.argtypes = [c_int, c_char_p]

ToolsLib.UpnpGetErrorMessage.restype = c_char_p
ToolsLib.UpnpGetErrorMessage.argtypes = [c_int]

##
# Combines a base URL and a relative URL into a single absolute URL. The memory for
# AbsURL needs to be allocated by the caller and must be large enough to hold the BaseURL and RelURL
# combined.
#
# @param BaseURL the base URL to combine
# @param RelURL the relative URL to BaseURL
# @param AbsURL A pointer to a buffer to store the absolute URL.
#
# @return An integer representing one of the following: UPNP_E_SUCCESS, UPNP_E_INVALID_PARAM,
# UPNP_E_INVALID_URL, UPNP_E_OUTOF_MEMORY
def UpnpResolveURL(BaseURL, RelURL, AbsURL):
	return ToolsLib.UpnpResolveURL(BaseURL, RelURL, AbsURL)

##
# Creates an action request packet based on its input parameters (status variable name and value
# pair). Any number of input parameters can be passed to this function but ever input variable
# name should have a matching value argument.
#
# @param ActionName The action name.
# @param ServType The service type.
# @param NumArg The number of argument pairs to be passed.
# @param Status Arg Status variable and value pair.
# @param ... Other status variable name and value pairs.
def UpnpMakeAction(ActionName, ServType, NumArg, Arg, *Args):
	return ToolsLib.UpnpMakeAction(ActionName, ServType, NumArg, Arg, Args)

##
# Creates an action request packet based on its input parameters (status variable name and value
# pair). This API is specially suitable inside a loop to add any number input parameters into an
# existing action. If no action document exists in the beginning then a Upnp_Document variable
# initialized with None should be passed as a parameter.
#
# @param ActionDoc A pointer to store the action document node.
# @param ActionName The action name.
# @param ServType The service type.
# @param ArgName The status variable name.
# @param ArgVal The status variable value.
#
# @return An integer representing one of the following: UPNP_E_SUCCESS, UPNP_E_INVALID_PARAM,
# UPNP_E_OUTOF_MEMORY.
def UpnpAddToAction(ActionDoc, ActionName, ServType, ArgName, ArgVal):
	return ToolsLib.UpnpAddToAction(ActionDoc, ActionName, ServType, ArgName, ArgVal)

##
# Creates an action response packet based on its output parameters (status variable name
# and value pair). Any number of input parameters can be passed to this function but
# every output variable name should have a matching value argument.
#
# @param ActionName The action name.
# @param ServType The service type.
# @param NumArg The number of argument pairs passed.
# @param Arg The status variable name and value pair.
# @param ... Other status variable name and value pairs.
#
# @return The action node of Upnp_Document type or None if the operation failed.
def UpnpMakeActionResponse(ActionName, ServType, NumArg, Arg, *Args):
	return ToolsLib.UpnpAddToAction(ActionName, ServType, NumArg, Arg, Args)

##
# Creates an action response packet based on its output parameters (status variable name
# and value pair). This API is especially suitable inside a loop to add any number of input
# parameters into an existing action response. If no action document exists in the beginning,
# a Upnp_Document variable initialized with None should be passed as a parameter.
#
# @param ActionResponse Pointer to a document to store the action document node.
# @param ActionName The action name.
# @param ServType The service type.
# @param ArgName The status variable name.
# @param ArgVal The status variable value.
#
# @return An integer representing one of the following: UPNP_E_SUCCESS, UPNP_E_INVALID_PARAM,
# UPNP_E_OUTOF_MEMORY.
def UpnpAddToActionResponse(ActionResponse, ActionName, ServType, ArgName, ArgVal):
	return ToolsLib.UpnpAddToActionResponse(ActionResponse, ActionName, ServType, ArgName, ArgVal)

##
# Can be used when application needs to transfer the status of many variables at once. It can be
# used (inside a loop) to add some extra status variables into an existing property set. If the
# application does not already have a property set document, the application should create a
# variable initialized with None and pass that as a first parameter.
#
# @param PropSet A pointer to the document containing the property set document node.
# @param ArgName The status variable name.
# @param ArgVal The status variable value.
#
# @return An integer representing one of the following: UPNP_E_SUCCESS, UPNP_E_INVALID_PARAM,
# UPNP_OUTOF_MEMORY.
def UpnpAddToPropertySet(PropSet, ArgName, ArgVal):
	return ToolsLib.UpnpAddToPropertySet(PropSet, ArgName, ArgVal)

##
# Creates a property set message packet. Any number of input parameters can be passed to this
# function but every input variable name should have a matching value input argument.
#
# @param NumArg A pointer to the document containing the property set document node.
# @param ArgName The status variable name.
# @param Args
#
# @return None on failure or the property set document node.
def UpnpCreatePropertySet(NumArg, Arg, *Args):
	return ToolsLib.UpnpCreatePropertySet(NumArg, Arg, Args)

##
# Converts an SDK error code into a string error message suitable for display. The memory returned
# from this function should NOT be freed.
#
# @param errorcode The SDK error code to convert.
#
# @return An ASCII text string representing of the error message associated with the error code.
def UpnpGetErrorMessage(errorcode):
	return ToolsLib.UpnpGetErrorMessage(errorcode)
