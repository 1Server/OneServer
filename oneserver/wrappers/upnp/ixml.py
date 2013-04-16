from manager import OneServerManager

import sys
try:
	from ctypes import cdll
	from ctypes import c_char_p,c_int,c_void_p,c_char,c_ulong,c_ushort
	from ctypes import POINTER,Structure
	from ctypes.util import find_library
except ImportError:
	OneServerManager().log.error('Library CTypes not found.')
	sys.exit()

class DOMString(c_char_p):
	pass

TRUE = 1
FALSE = 0

##
# The document object model consists of a set of objects and interfaces for acessing and manipulating
# documents. IXML does not implement all the interfaces documented in the DOM2-Core recommendations
# but defines a subset of the most useful interfaces. A description of the supported interfaces
# and methods is presented in this section.
# 
# For a copmlete discussion on the object model, the object hierarchy, etc., refer to section
# 1.1 of the DOM2-Core recommendation.
class IXML_NODE_TYPE:
	eINVALID_NODE			= 0
	eELEMENT_NODE			= 1
	eATTRIBUTE_NODE			= 2
	eTEXT_NODE			= 3
	eCDATA_SECTION_NODE		= 4
	eENTITY_REFERENCE_NODE		= 5
	eENTITY_NODE			= 6
	ePROCESSING_INSTRUCTION_NODE	= 7
	eCOMMENT_NODE			= 8
	eDOCUMENT_NODE			= 9
	eDOCUMENT_TYPE_NODE		= 10
	eDOCUMENT_FRAGMENT_NODE		= 11
	eNOTATION_NODE			= 12

class IXML_ERRORCODE:
	IXML_INDEX_SIZE_ERR			= 1
	IXML_DOMSTRING_SIZE_ERR			= 2
	IXML_HIERARCHY_REQUEST_ERR		= 3
	IXML_WRONG_DOCUMENT_ERR			= 4
	IXML_INVALID_CHARACTER_ERR		= 5
	IXML_NO_DATA_ALLOWED_ERR		= 6
	IXML_NO_MODIFICATION_ALLOWED_ERR	= 7
	IXML_NOT_FOUND_ERR			= 8
	IXML_NOT_SUPPORTED_ERR			= 9
	IXML_INUSE_ATTRIBUTE_ERR		= 10
	IXML_INVALID_STATE_ERR			= 11
	IXML_SYNTAX_ERR				= 12
	IXML_INVALID_MODIFICATION_ERR		= 13
	IXML_NAMESPACE_ERR			= 14
	IXML_INVALID_ACCESS_ERR			= 15
	IXML_SUCCESS				= 0
	IXML_NO_SUCH_FILE			= 101
	IXML_INSUFFICIENT_MEMORY		= 102
	IXML_FILE_DONE				= 104
	IXML_INVALID_PARAMETER			= 105
	IXML_FAILED				= 106
	IXML_INVALID_ITEM_NUMBER		= 107

DOCUMENTNODENAME = '#document'
TEXTNODENAME = '#text'
CDATANODENAME = '#cdata-section'

class _IXML_Node(Structure):
	pass

_IXML_Node._fields_ = [
	('nodeName', DOMString),
	('nodeValue', DOMString),
	('nodeType', c_int),
	('namespaceURI', DOMString),
	('prefix', DOMString),
	('localName', DOMString),
	('readOnly', c_int),
	('parentNode', POINTER(_IXML_Node)),
	('firstChild', POINTER(_IXML_Node)),
	('prevSibling', POINTER(_IXML_Node)),
	('nextSibling', POINTER(_IXML_Node)),
	('firstAttr', POINTER(_IXML_Node)),
	('ownerDocument', c_void_p)
]

class IXML_Node(_IXML_Node):
	pass

class Nodeptr(POINTER(_IXML_Node)):
	pass

class _IXML_Document(Structure):
	pass
_IXML_Document._fields_ = [
	('n', IXML_Node)
]
class IXML_Document(_IXML_Document):
	pass

class Docptr(POINTER(_IXML_Document)):
	pass

class _IXML_CDATASection(Structure):
	pass
_IXML_CDATASection._fields_ = [
	('n', IXML_Node)
]
class IXML_CDATASection(_IXML_CDATASection):
	pass

class _IXML_Element(Structure):
	pass
_IXML_Element._fields_ = [
	('n', IXML_Node),
	('tagName', DOMString)
]
class IXML_Element(_IXML_Element):
	pass

class _IXML_ATTR(Structure):
	pass
_IXML_ATTR._fields_ = [
	('n', IXML_Node),
	('specified', c_int),
	('ownerElement', POINTER(IXML_Element))
]
class IXML_Attr(_IXML_ATTR):
	pass

class _IXML_Text(Structure):
	pass
_IXML_Text._fields_ = [
	('n', IXML_Node)
]
class IXML_Text(_IXML_Text):
	pass

class _IXML_NodeList(Structure):
	pass
_IXML_NodeList._fields_ = [
	('nodeItem', POINTER(IXML_Node)),
	('next', POINTER(_IXML_NodeList))
]
class IXML_NodeList(_IXML_NodeList):
	pass

class _IXML_NamedNodeMap(Structure):
	pass
_IXML_NamedNodeMap._fields_ = [
	('nodeItem', POINTER(IXML_Node)),
	('next', POINTER(_IXML_NamedNodeMap))
]
class IXML_NamedNodeMap(_IXML_NamedNodeMap):
	pass

IXMLLib = cdll.LoadLibrary(find_library('ixml'))

##
# Returns the name of the {\bf Node}, depending on what type of 
# {\bf Node} it is, in a read-only string. Refer to the table in the 
# DOM2-Core for a description of the node names for various interfaces.
#
# @param nodeptr Poitner to the node
#
# @return [const DOMString] A constant {\bf DOMString} of the node name.
def ixmlNode_getNodeName(nodeptr):
	return IXMLLib.ixmlNode_getNodeName(nodeptr)

IXMLLib.ixmlNode_getNodeName.restype = DOMString
IXMLLib.ixmlNode_getNodeName.argtypes = [POINTER(IXML_Node)]

##
# Returns the value of the {\bf Node} as a string.  Note that this string 
# is not a copy and modifying it will modify the value of the {\bf Node}.
#
# @param nodeptr Poitner to the node
#
# @return [DOMString] A {\bf DOMString} of the {\bf Node} value.
def ixmlNode_getNodeValue(nodeptr):
	return IXMLLib.ixmlNode_getNodeValue(nodeptr)

IXMLLib.ixmlNode_getNodeValue.restype = DOMString
IXMLLib.ixmlNode_getNodeValue.argtypes = [POINTER(IXML_Node)]

##
# Assigns a new value to a {\bf Node}.  The {\bf newNodeValue} string is
# duplicated and stored in the {\bf Node} so that the original does not
# have to persist past this call.
#
# @param nodeptr A pointer to the node
# @param newNodeValue the new node value
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
##	\item {\tt IXML_INVALID_PARAMETER}: The {\bf Node} is not a valid 
#		   pointer.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlNode_setNodeValue(nodeptr, newNodeValue):
	return IXMLLib.ixmlNode_setNodeValue(nodeptr, newNodeValue)

IXMLLib.ixmlNode_setNodeValue.restype = c_int
IXMLLib.ixmlNode_setNodeValue.argtypes = [POINTER(IXML_Node), c_char_p]

##
# Retrieves the type of a {\bf Node}.  The defined {\bf Node} constants 
# are:
# \begin{itemize}
#   \item {\tt eATTRIBUTE_NODE} 
#   \item {\tt eCDATA_SECTION_NODE}
#   \item {\tt eCOMMENT_NODE}
#   \item {\tt eDOCUMENT_FRAGMENT_NODE} 
#   \item {\tt eDOCUMENT_NODE} 
#   \item {\tt eDOCUMENT_TYPE_NODE} 
#   \item {\tt eELEMENT_NODE} 
#   \item {\tt eENTITY_NODE}
#   \item {\tt eENTITY_REFERENCE_NODE}
#   \item {\tt eNOTATION_NODE} 
#   \item {\tt ePROCESSING_INSTRUCTION_NODE}
#   \item {\tt eTEXT_NODE}
# \end{itemize}
#
# @param nodeptr A pointer to the node
#
# @return [const unsigned short] An integer representing the type of the 
# {\bf Node}.
def ixmlNode_getNodeType(nodeptr):
	return IXMLLib.ixmlNode_getNodeType(nodeptr)

IXMLLib.ixmlNode_getNodeType.restype = c_ushort
IXMLLib.ixmlNode_getNodeType.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the parent {\bf Node} for a {\bf Node}.
#
# @param nodeptr A pointer to the node.
#
# @return [Node#] A pointer to the parent {\bf Node} or {\tt NULL} if the 
# {\bf Node} has no parent.
def ixmlNode_getParentNode(nodeptr):
	return IXMLLib.ixmlNode_getParentNode(nodeptr)

IXMLLib.ixmlNode_getParentNode.restype = POINTER(IXML_Node)
IXMLLib.ixmlNode_getParentNode.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the list of children of a {\bf Node} in a {\bf NodeList} 
# structure.  If a {\bf Node} has no children, {\bf ixmlNode_getChildNodes}
# returns a {\bf NodeList} structure that contains no {\bf Node}s.
#
# @param nodeptr A pointer to the node.
#
# @return [NodeList#] A {\bf NodeList} of the children of the {\bf Node}.
def ixmlNode_getChildNodes(nodeptr):
	return IXMLLib.ixmlNode_getChildNodes(nodeptr)

IXMLLib.ixmlNode_getChildNodes.restype = POINTER(IXML_NodeList)
IXMLLib.ixmlNode_getChildNodes.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the first child {\bf Node} of a {\bf Node}.
#
# @param nodeptr A pointer to the node.
#
# @return [Node#] A pointer to the first child {\bf Node} or {\tt NULL} 
# if the {\bf Node} does not have any children.
def ixmlNode_getFirstChild(nodeptr):
	return IXMLLib.ixmlNode_getFirstChild(nodeptr)

IXMLLib.ixmlNode_getFirstChild.restype = POINTER(IXML_Node)
IXMLLib.ixmlNode_getFirstChild.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the last child {\bf Node} of a {\bf Node}.
#
# @param nodeptr A pointer to the node.
#
# @return [Node#] A pointer to the last child {\bf Node} or {\tt NULL} if 
# the {\bf Node} does not have any children.
def ixmlNode_getLastChild(nodeptr):
	return IXMLLib.ixmlNode_getLastChild(nodeptr)

IXMLLib.ixmlNode_getLastChild.restype = POINTER(IXML_Node)
IXMLLib.ixmlNode_getLastChild.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the sibling {\bf Node} immediately preceding this {\bf Node}.
#
# @param nodeptr A pointer to the node.
#
# @return [Node#] A pointer to the previous sibling {\bf Node} or 
# {\tt NULL} if no such {\bf Node} exists.
def ixmlNode_getPreviousSibling(nodeptr):
	return IXMLLib.ixmlNode_getPreviousSibling(nodeptr)

IXMLLib.ixmlNode_getPreviousSibling.restype = POINTER(IXML_Node)
IXMLLib.ixmlNode_getPreviousSibling.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the sibling {\bf Node} immediately following this {\bf Node}.
#
# @param nodeptr A pointer to the node.
#
# @return [Node#] A pointer to the next sibling {\bf Node} or {\tt NULL} 
# if no such {\bf Node} exists.
def ixmlNode_getNextSibling(nodeptr):
	return IXMLLib.ixmlNode_getNextSibling(nodeptr)

IXMLLib.ixmlNode_getNextSibling.restype = POINTER(IXML_Node)
IXMLLib.ixmlNode_getNextSibling.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the attributes of a {\bf Node}, if it is an {\bf Element} node,
# in a {\bf NamedNodeMap} structure.
#
# @param nodeptr A pointer to the node.
#
# @return [NamedNodeMap#] A {\bf NamedNodeMap} of the attributes or 
# {\tt NULL}.
def ixmlNode_getAttributes(nodeptr):
	return IXMLLib.ixmlNode_getAttributes(nodeptr)

IXMLLib.ixmlNode_getAttributes.restype = POINTER(IXML_NamedNodeMap)
IXMLLib.ixmlNode_getAttributes.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the document object associated with this {\bf Node}.  This 
# owner document {\bf Node} allows other {\bf Node}s to be created in the 
# context of this document.  Note that {\bf Document} nodes do not have 
# an owner document.
#
# @param nodeptr A pointer to the node.
#
# @return [Document#] A pointer to the owning {\bf Document} or 
# {\tt NULL}, if the {\bf Node} does not have an owner.
def ixmlNode_getOwnerDocument(nodeptr):
	return IXMLLib.ixmlNode_getOwnerDocument(nodeptr)

IXMLLib.ixmlNode_getOwnerDocument.restype = POINTER(IXML_Document)
IXMLLib.ixmlNode_getOwnerDocument.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the namespace URI for a {\bf Node} as a {\bf DOMString}.  Only
# {\bf Node}s of type {\tt eELEMENT_NODE} or {\tt eATTRIBUTE_NODE} can 
# have a namespace URI.  {\bf Node}s created through the {\bf Document} 
# interface will only contain a namespace if created using 
# {\bf ixmlDocument_createElementNS}.
#
# @param nodeptr A pointer to the node.
#
# @return [const DOMString] A {\bf DOMString} representing the URI of the 
# namespace or {\tt NULL}.
def ixmlNode_getNamespaceURI(nodeptr):
	return IXMLLib.ixmlNode_getNamespaceURI(nodeptr)

IXMLLib.ixmlNode_getNamespaceURI.restype = DOMString
IXMLLib.ixmlNode_getNamespaceURI.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the namespace prefix, if present.  The prefix is the name
# used as an alias for the namespace URI for this element.  Only 
# {\bf Node}s of type {\tt eELEMENT_NODE} or {\tt eATTRIBUTE_NODE} can have 
# a prefix. {\bf Node}s created through the {\bf Document} interface will 
# only contain a prefix if created using {\bf ixmlDocument_createElementNS}.
#
# @param nodeptr A pointer to the node.
#
# @return [DOMString] A {\bf DOMString} representing the namespace prefix 
# or {\tt NULL}.
def ixmlNode_getPrefix(nodeptr):
	return IXMLLib.ixmlNode_getPrefix(nodeptr)

IXMLLib.ixmlNode_getPrefix.restype = DOMString
IXMLLib.ixmlNode_getPrefix.argtypes = [POINTER(IXML_Node)]

##
# Retrieves the local name of a {\bf Node}, if present.  The local name is
# the tag name without the namespace prefix.  Only {\bf Node}s of type
# {\tt eELEMENT_NODE} or {\tt eATTRIBUTE_NODE} can have a local name.
# {\Bf Node}s created through the {\bf Document} interface will only 
# contain a local name if created using {\bf ixmlDocument_createElementNS}.
#
# @param nodeptr A pointer to the node.
#
# @return [const DOMString] A {\bf DOMString} representing the local name 
# of the {\bf Element} or {\tt NULL}.
def ixmlNode_getLocalName(nodeptr):
	return IXMLLib.ixmlNode_getLocalName(nodeptr)

IXMLLib.ixmlNode_getLocalName.restype = DOMString
IXMLLib.ixmlNode_getLocalName.argtypes = [POINTER(IXML_Node)]

##
# Inserts a new child {\bf Node} before the existing child {\bf Node}.  
# {\bf refChild} can be {\tt NULL}, which inserts {\bf newChild} at the
# end of the list of children.  Note that the {\bf Node} (or {\bf Node}s) 
# in {\bf newChild} must already be owned by the owner document (or have no
# owner at all) of {\bf nodeptr} for insertion.  If not, the {\bf Node} 
# (or {\bf Node}s) must be imported into the document using 
# {\bf ixmlDocument_importNode}.  If {\bf newChild} is already in the tree,
# it is removed first.
#
# @param nodeptr A pointer to the node.
# @param newChild A pointer to the new node.
# @param refChild A pointer to the node to put the new node before.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf nodeptr} or 
#		{\bf newChild} is {\tt NULL}.
#	 \item {\tt IXML_HIERARCHY_REQUEST_ERR}: The type of the {\bf Node} 
#		does not allow children of the type of {\bf newChild}.
#	 \item {\tt IXML_WRONG_DOCUMENT_ERR}: {\bf newChild} has an owner 
#		document that does not match the owner of {\bf nodeptr}.
#	 \item {\tt IXML_NO_MODIFICATION_ALLOWED_ERR}: {\bf nodeptr} is 
#		read-only or the parent of the {\bf Node} being inserted is 
#		read-only.
#	 \item {\tt IXML_NOT_FOUND_ERR}: {\bf refChild} is not a child of 
#		{\bf nodeptr}.
#   \end{itemize}
def ixmlNode_insertBefore(nodeptr, newChild, refChild):
	return IXMLLib.ixmlNode_insertBefore(nodeptr, newChild, refChild)

IXMLLib.ixmlNode_insertBefore.restype = c_int
IXMLLib.ixmlNode_insertBefore.argtypes = [POINTER(IXML_Node), POINTER(IXML_Node), POINTER(IXML_Node)]

##
# Replaces an existing child {\bf Node} with a new child {\bf Node} in 
# the list of children of a {\bf Node}. If {\bf newChild} is already in 
# the tree, it will first be removed. {\bf returnNode} will contain the 
# {\bf oldChild} {\bf Node}, appropriately removed from the tree (i.e. it 
# will no longer have an owner document).
#
# @param nodeptr A pointer to the node.
# @param newChild A pointer to the new node.
# @param oldChild A poniter to the node to replace.
# @param returnNode Pointer to a Node to place the removed oldChild node.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMTER: Either {\bf nodeptr}, {\bf 
#		   newChild}, or {\bf oldChild} is {\tt NULL}.
#	 \item {\tt IXML_HIERARCHY_REQUEST_ERR}: The {\bf newChild} is not 
#		   a type of {\bf Node} that can be inserted into this tree or 
#		   {\bf newChild} is an ancestor of {\bf nodePtr}.
#	 \item {\tt IXML_WRONG_DOCUMENT_ERR}: {\bf newChild} was created from 
#		   a different document than {\bf nodeptr}.
#	 \item {\tt IXML_NO_MODIFICATION_ALLOWED_ERR}: {\bf nodeptr} or 
#		   its parent is read-only.
#	 \item {\tt IXML_NOT_FOUND_ERR}: {\bf oldChild} is not a child of 
#		   {\bf nodeptr}.
#   \end{itemize}
def ixmlNode_replaceChild(nodeptr, newChild, oldChild, returnNode):
	return IXMLLib.ixmlNode_replaceChild(nodeptr, newChild, oldChild, returnNode)

IXMLLib.ixmlNode_replaceChild.restype = c_int
IXMLLib.ixmlNode_replaceChild.argtypes = [POINTER(IXML_Node), POINTER(IXML_Node), POINTER(IXML_Node), POINTER(POINTER(IXML_Node))]

##
# Removes a child from the list of children of a {\bf Node}.
# {\bf returnNode} will contain the {\bf oldChild} {\bf Node}, 
# appropriately removed from the tree (i.e. it will no longer have an 
# owner document).
#
# @param nodeptr A pointer to the parent of the child to remove
# @param oldChild The child node to remove
# @param returnNode Pointer to a node to place the removed old child node
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf nodeptr} or 
#		   {\bf oldChild} is {\tt NULL}.
#	 \item {\tt IXML_NO_MODIFICATION_ALLOWED_ERR}: {\bf nodeptr} or its 
#		   parent is read-only.
#	 \item {\tt IXML_NOT_FOUND_ERR}: {\bf oldChild} is not among the 
#		   children of {\bf nodeptr}.
#   \end{itemize}
def ixmlNode_removeChild(nodeptr, oldChild, returnNode):
	return IXMLLib.ixmlNode_removeChild(nodeptr, oldChild, returnNode)

IXMLLib.ixmlNode_removeChild.restype = c_int
IXMLLib.ixmlNode_removeChild.argtypes = [POINTER(IXML_Node), POINTER(IXML_Node), POINTER(POINTER(IXML_Node))]

##
# Appends a child {\bf Node} to the list of children of a {\bf Node}.  If
# {\bf newChild} is already in the tree, it is removed first.
#
# @param nodeptr The node in which to append the new child
# @param newChild the new child to append
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf nodeptr} or 
#		   {\bf newChild} is {\tt NULL}.
#	 \item {\tt IXML_HIERARCHY_REQUEST_ERR}: {\bf newChild} is of a type 
#		   that cannot be added as a child of {\bf nodeptr} or 
#		   {\bf newChild} is an ancestor of {\bf nodeptr}.
#	 \item {\tt IXML_WRONG_DOCUMENT_ERR}: {\bf newChild} was created from 
#		   a different document than {\bf nodeptr}.
#	 \item {\tt IXML_NO_MODIFICATION_ALLOWED_ERR}: {\bf nodeptr} is a 
#		   read-only {\bf Node}.
def ixmlNode_appendChild(nodeptr, newChild):
	return IXMLLib.ixmlNode_appendChild(nodeptr, newChild)

IXMLLib.ixmlNode_appendChild.restype = c_int
IXMLLib.ixmlNode_appendChild.argtype = [POINTER(IXML_Node), POINTER(IXML_Node)]

##
# Queries whether or not a {\bf Node} has children.
#
# @param nodeptr The node to query for children
#
# @return [BOOL] {\tt TRUE} if the {\bf Node} has one or more children 
#				otherwise {\tt FALSE}.
def ixmlNode_hasChildNodes(nodeptr):
	return IXMLLib.ixmlNode_hasChildNodes(nodeptr)

IXMLLib.ixmlNode_hasChildNodes.restype = c_int
IXMLLib.ixmlNode_hasChildNodes.argtypes = [POINTER(IXML_Node)]

##
# Clones a {\bf Node}.  The new {\bf Node} does not have a parent.  The
# {\bf deep} parameter controls whether the subtree of the {\bf Node} is
# also cloned.  For details on cloning specific types of {\bf Node}s, 
# refer to the DOM2-Core recommendation.
#
# @param nodeptr The node to clone
# @param deep True to clone the subtree also or false to clone only nodeptr
#
# @return [Node*] A clone of {\bf nodeptr} or {\tt NULL}.
def ixmlNode_cloneNode(nodeptr, deep):
	return IXMLLib.ixmlNode_cloneNode(nodeptr, deep)

IXMLLib.ixmlNode_hasChildNodes.restype = POINTER(IXML_Node)
IXMLLib.ixmlNode_hasChildNodes.argtypes = [POINTER(IXML_Node), c_int]

##
# Queries whether this {\bf Node} has attributes.  Note that only 
# {\bf Element} nodes have attributes.
#
# @param nodeptr the node to query for attributes
#
# @return [BOOL] {\tt TRUE} if the {\bf Node} has attributes otherwise 
#				{\tt FALSE}.
def ixmlNode_hasAttributes(nodeptr):
	return IXMLLib.ixmlNode_hasAttributes(nodeptr)

IXMLLib.ixmlNode_hasAttributes.restype = c_int
IXMLLib.ixmlNode_hasAttributes.argtypes = [POINTER(IXML_Node)]

##
# Frees a node and all nodes in its subtree.
#
# @param nodeptr the node to free
def ixmlNode_free(nodeptr):
	IXMLLib.ixmlNode_free(nodeptr)

IXMLLib.ixmlNode_free.argtypes = [POINTER(IXML_Node)]

##
# Frees an Attr node.
#
# @param attrNode the Attr node to free.
def ixmlAttr_free(attrNode):
	IXMLLib.ixmlAttr_free(attrNode)

IXMLLib.ixmlAttr_free.argtypes = [POINTER(IXML_Attr)]

##
# Initializes a CDATASection node.
#
# @param nodeptr The CDATASection node to initalize
def ixmlCDATASection_init(nodeptr):
	IXMLLib.ixmlCDATASection_init(nodeptr)

IXMLLib.ixmlCDATASection_init.argtypes = [POINTER(IXML_CDATASection)]

##
# Frees a CDATASection node.
#
# @param nodeptr The CDATASection node to free.
def ixmlCDATASection_free(nodeptr):
	IXMLLib.ixmlCDATASection_free(nodeptr)

IXMLLib.ixmlCDATASection_free.argtypes = [POINTER(IXML_CDATASection)]

##
# Initializes a Document node.
#
# @param nodeptr The Document node to initialize.
def ixmlDocument_init(nodeptr):
	IXMLLib.ixmlDocument_init(nodeptr)

IXMLLib.ixmlDocument_init.argtypes = [POINTER(IXML_Document)]

##
# Creates a new empty {\bf Document} node.  The 
# {\bf ixmlDocument_createDocumentEx} API differs from the {\bf
# ixmlDocument_createDocument} API in that it returns an error code
# describing the reason for the failure rather than just {\tt NULL}.
#
# @param doc Pointer to a Document where the new object will be stored.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlDocument_createDocumentEx(doc):
	return IXMLLib.ixmlDocument_createDocumentEx(doc)

IXMLLib.ixmlDocument_createDocumentEx.restype = c_int
IXMLLib.ixmlDocument_createDocumentEx.argtypes = [POINTER(POINTER(IXML_Document))]

##
# Creates a new empty Document node.
#
# @return A pointer to the new Document or None on failure.
def ixmlDocument_createDocument():
	return IXMLLib.ixmlDocument_createDocument()

IXMLLib.ixmlDocument_createDocument.restype = POINTER(IXML_Document)

##
# Creates a new {\bf Element} node with the given tag name.  The new
# {\bf Element} node has a {\tt nodeName} of {\bf tagName} and
# the {\tt localName}, {\tt prefix}, and {\tt namespaceURI} set 
# to {\tt NULL}.  To create an {\bf Element} with a namespace, 
# see {\bf ixmlDocument_createElementNS}.
#
# The {\bf ixmlDocument_createElementEx} API differs from the {\bf
# ixmlDocument_createElement} API in that it returns an error code
# describing the reason for failure rather than just {\tt NULL}.
#
# @param doc The owner Document of the new node.
# @param tagName The tag name of the new Element node.
# @param rtElement Pointer to an Element where the new object will be stored.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf doc} or 
#		   {\bf tagName} is {\tt NULL}.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlDocument_createElementEx(doc, tagName, rtElement):
	return IXMLLib.ixmlDocument_createElementEx(doc, tagName, rtElement)

IXMLLib.ixmlDocument_createElementEx.restype = c_int
IXMLLib.ixmlDocument_createElementEx.argtypes = [POINTER(IXML_Document), DOMString, POINTER(POINTER(IXML_Element))]

##
# Creates a new {\bf Element} node with the given tag name.  The new
# {\bf Element} node has a {\tt nodeName} of {\bf tagName} and
# the {\tt localName}, {\tt prefix}, and {\tt namespaceURI} set 
# to {\tt NULL}.  To create an {\bf Element} with a namespace, 
# see {\bf ixmlDocument_createElementNS}.
#
# @param doc The owner Document of the new node.
# @param tagName The tag name of the new Element node.
#
# @return [Document*] A pointer to the new {\bf Element} or {\tt NULL} on 
#					 failure.
def ixmlDocument_createElement(doc, tagName):
	return IXMLLib.ixmlDocument_createElement(doc, tagName)

IXMLLib.ixmlDocument_createElement.restype = POINTER(IXML_Element)
IXMLLib.ixmlDocument_createElement.argtypes = [POINTER(IXML_Document), DOMString]

##
# Creates a new {\bf Text} node with the given data.  
# The {\bf ixmlDocument_createTextNodeEx} API differs from the {\bf
# ixmlDocument_createTextNode} API in that it returns an error code
# describing the reason for failure rather than just {\tt NULL}.
#
# @param doc The owner Document of the new node.
# @param data The data to associate with the new Text node.
# @param textNode A pointer to a Node where the new object will be stored.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf doc} or {\bf data} 
#		   is {\tt NULL}.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlDocument_createTextNodeEx(doc, data, textNode):
	return IXMLLib.ixmlDocument_createTextNodeEx(doc, data, textNode)

IXMLLib.ixmlDocument_createTextNodeEx.restype = c_int
IXMLLib.ixmlDocument_createTextNodeEx.argtypes = [POINTER(IXML_Document), DOMString, POINTER(POINTER(IXML_Node))]

##
# Creates a new {\bf Text} node with the given data.
#
# @param doc The owner Document of the new node.
# @param data The data to associate with the new Text node.
#
# @return [Node*] A pointer to the new {\bf Node} or {\tt NULL} on failure.
def ixmlDocument_createTextNode(doc, data):
	return IXMLLib.ixmlDocument_createTextNode(doc, data)

IXMLLib.ixmlDocument_createTextNode.restype = POINTER(IXML_Node)
IXMLLib.ixmlDocument_createTextNode.argtyeps = [POINTER(IXML_Document), DOMString]

##
# Creates a new {\bf CDATASection} node with given data.
#
# The {\bf ixmlDocument_createCDATASectionEx} API differs from the {\bf
# ixmlDocument_createCDATASection} API in that it returns an error code
# describing the reason for failure rather than just {\tt NULL}.
#
# @param doc The owner Document of the new node.
# @param data The data to associate with the new CDATASection node.
# @param cdNode A pointer to a Node where the new object will be stored.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf doc} or {\bd data} 
#		   is {\tt NULL}.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlDocument_createCDATASectionEx(doc, data, cdNode):
	return IXMLLib.ixmlDocument_createCDATASectionEx(doc, data, cdNode)

IXMLLib.ixmlDocument_createCDATASectionEx.restype = c_int
IXMLLib.ixmlDocument_createCDATASectionEx.argtypes = [POINTER(IXML_Document), DOMString, POINTER(POINTER(IXML_CDATASection))]

##
# Creates a new {\bf CDATASection} node with given data.
#
# @param doc The owner Document of the new node.
# @param data The data to associate with the new CDATASection node.
#
# @return [CDATASection*] A pointer to the new {\bf CDATASection} or 
#						 {\tt NULL} on failure.
def ixmlDocument_createCDATASection(doc, data):
	return IXMLLib.ixmlDocument_createCDATASection(doc, data)

IXMLLib.ixmlDocument_createCDATASection.restype = POINTER(IXML_CDATASection)
IXMLLib.ixmlDocument_createCDATASection.argtypes = [POINTER(IXML_Document), DOMString]

##
# Creates a new {\bf Attr} node with the given name.  
#
# @param doc The owner Document of the new node.
# @param name The name of the new attribute.
#
# @return [Attr*] A pointer to the new {\bf Attr} or {\tt NULL} on failure.
def ixmlDocument_createAttribute(doc, name):
	return IXMLLib.ixmlDocument_createAttribute(doc, name)

IXMLLib.ixmlDocument_createAttribute.restype = POINTER(IXML_Attr)
IXMLLib.ixmlDocument_createAttribute.argtypes = [POINTER(IXML_Document), c_char_p]

##
# Creates a new {\bf Attr} node with the given name.  
#
# The {\bf ixmlDocument_createAttributeEx} API differs from the {\bf
# ixmlDocument_createAttribute} API in that it returns an error code
# describing the reason for failure rather than just {\tt NULL}.
#
# @param doc The owner Document of the new node.
# @param name The name of the new attribute.
# @param attrnode A pointer to an Attr where the new object will be stored.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf doc} or {\bf name} 
#		   is {\tt NULL}.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlDocument_createAttributeEx(doc, name, attrNode):
	return IXMLLib.ixmlDocument_createAttributeEx(doc, name, attrNode)

IXMLLib.ixmlDocument_createAttributeEx.restype = c_int
IXMLLib.ixmlDocument_createAttributeEx.argtypes = [POINTER(IXML_Document), c_char_p, POINTER(POINTER(IXML_Attr))]

##
# Returns a {\bf NodeList} of all {\bf Elements} that match the given
# tag name in the order in which they were encountered in a preorder
# traversal of the {\bf Document} tree.  
#
# @param doc The Document to search.
# @param tagName The tag name to find.
#
# @return [NodeList*] A pointer to a {\bf NodeList} containing the 
#					 matching items or {\tt NULL} on an error.
def ixmlDocument_getElementsByTagName(doc, tagName):
	return IXMLLib.ixmlDocument_getElementsByTagName(doc, tagName)

IXMLLib.ixmlDocument_getElementsByTagName.restype = POINTER(IXML_NodeList)
IXMLLib.ixmlDocument_getElementsByTagName.argtypes = [POINTER(IXML_Document), DOMString]

##
# Creates a new {\bf Element} node in the given qualified name and
# namespace URI.
#
# The {\bf ixmlDocument_createElementNSEx} API differs from the {\bf
# ixmlDocument_createElementNS} API in that it returns an error code
# describing the reason for failure rather than just {\tt NULL}.
#
# @param doc The owner Document of the new node.
# @param namespaceURI The namespace URI for the new Element.
# @param qualifiedName The qualified name of the new Element.
# @param rtElement rtElement A pointer to an Element where the new object will be stored.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf doc}, 
#		   {\bf namespaceURI}, or {\bf qualifiedName} is {\tt NULL}.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlDocument_createElementNSEx(doc, namespaceURI, qualifiedName, rtElement):
	return IXMLLib.ixmlDocument_createElementNSEx(doc, namespaceURI, qualifiedName, rtElement)

IXMLLib.ixmlDocument_createElementNSEx.restype = c_int
IXMLLib.ixmlDocument_createElementNSEx.argtypes = [POINTER(IXML_Document), DOMString, DOMString, POINTER(POINTER(IXML_Element))]

##
# Creates a new {\bf Element} node in the given qualified name and
# namespace URI.
#
# @param doc The owner Document of the new node.
# @param namespaceURI The namespace URI for the new Element.
# @param qualifiedName The qualified name of the new Element.
#
# @return [Element*] A pointer to the new {\bf Element} or {\tt NULL} on 
#					failure.
def ixmlDocument_createElementNS(doc, namespaceURI, qualifiedName):
	return IXMLLib.ixmlDocument_createElementNS(doc, namespaceURI, qualifiedName)

IXMLLib.ixmlDocument_createElementNS.restype = POINTER(IXML_Element)
IXMLLib.ixmlDocument_createElementNS.argtypes = [POINTER(IXML_Document), DOMString, DOMString]

##
# Returns a {\bf NodeList} of {\bf Elements} that match the given
# local name and namespace URI in the order they are encountered
# in a preorder traversal of the {\bf Document} tree.  Either 
# {\bf namespaceURI} or {\bf localName} can be the special {\tt "*"}
# character, which matches any namespace or any local name respectively.
#
# @param doc The document to search
# @param namespaceURI The namespace of the elements to find or "*" to match any namespace.
# @param localName The local name of the elements to find or "*" to match any local name.
#
# @return [NodeList*] A pointer to a {\bf NodeList} containing the 
#					 matching items or {\tt NULL} on an error.
def ixmlDocument_getElementsByTagNameNS(doc, namespaceURI, localName):
	return IXMLLib.ixmlDocument_getElementsByTagNameNS(doc, namespaceURI, localName)

IXMLLib.ixmlDocument_getElementsByTagNameNS.restype = POINTER(IXML_NodeList)
IXMLLib.ixmlDocument_getElementsByTagNameNS.argtypes = [POINTER(IXML_Document), DOMString, DOMString]

##
# Returns the {\bf Element} whose {\tt ID} matches that given id.
#
# @param doc The owner Document of the Element.
# @param tagName The name of the Element.
#
# @return [Element*] A pointer to the matching {\bf Element} or 
#					{\tt NULL} on an error.
def ixmlDocument_getElementbyId(doc, tagName):
	return IXMLLib.ixmlDocument_getElementById(doc, tagName)

IXMLLib.ixmlDocument_getElementById.restype = POINTER(IXML_Element)
IXMLLib.ixmlDocument_getElementById.argtypes = [POINTER(IXML_Document), DOMString]

##
# Frees a {\bf Document} object and all {\bf Node}s associated with it.  
# Any {\bf Node}s extracted via any other interface function, e.g. 
# {\bf ixmlDocument_GetElementById}, become invalid after this call unless
# explicitly cloned.
#
# @param doc The Document to free.
#
# @return [void] This function does not return a value.
def ixmlDocument_free(doc):
	IXMLLib.ixmlDocument_free(doc)

IXMLLib.ixmlDocument_free.argtypes = [POINTER(IXML_Document)]

##
# Imports a {\bf Node} from another {\bf Document} into this 
# {\bf Document}.  The new {\bf Node} does not a have parent node: it is a 
# clone of the original {\bf Node} with the {\tt ownerDocument} set to 
# {\bf doc}.  The {\bf deep} parameter controls whether all the children 
# of the {\bf Node} are imported.  Refer to the DOM2-Core recommendation 
# for details on importing specific node types.
#
# @param doc The Document into which to import.
# @param importNode The node to import.
# @param deep True to import all children of importNode or False to import only the root node.
# @param rtNode A pointer to a new Node owned by doc.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf doc} or 
#		   {\bf importNode} is not a valid pointer.
#	 \item {\tt IXML_NOT_SUPPORTED_ERR}: {\bf importNode} is a 
#		   {\bf Document}, which cannot be imported.
#	 \item {\tt IXML_FAILED}: The import operation failed because the 
#		   {\bf Node} to be imported could not be cloned.
#   \end{itemize}
def ixmlDocument_importNode(doc, importNode, deep, rtNode):
	return IXMLLib.ixmlDocument_importNode(doc, importNode, deep, rtNode)

IXMLLib.ixmlDocument_importNode.restype = c_int
IXMLLib.ixmlDocument_importNode.argtypes = [POINTER(IXML_Document), POINTER(IXML_Node), c_int, POINTER(POINTER(IXML_Node))]

##
# Initializes a {\bf IXML_Element} node.
#
# @param element The element to initialize.
#
# @return [void] This function does not return a value.
def ixmlElement_init(element):
	IXMLLib.ixmlElement_init(element)

IXMLLib.ixmlElement_init.argtypes = [POINTER(IXML_Element)]

##
# Returns the name of the tag as a constant string.
#
# @param element The element from which to retrieve the name.
#
# @return [const DOMString] A {\bf DOMString} representing the name of the 
#						   {\bf Element}.
def ixmlElement_getTagName(element):
	return IXMLLib.ixmlElement_getTagName(element)

IXMLLib.ixmlElement_getTagName.restype = DOMString
IXMLLib.ixmlElement_getTagName.argtypes = [POINTER(IXML_Element)]

##
# Retrieves an attribute of an {\bf Element} by name.  
#
# @param element The element from which to retrieve the attribute.
# @param name The name of the attribute to retrieve.
#
# @return [DOMString] A {\bf DOMString} representing the value of the 
#					 attribute.
def ixmlElement_getAttribute(element, name):
	return IXMLLib.ixmlElement_getTagName(element, name)

IXMLLib.ixmlElement_getTagName.restype = DOMString
IXMLLib.ixmlElement_getTagName.argtypes = [POINTER(IXML_Element), DOMString]

##
# Adds a new attribute to an {\bf Element}.  If an attribute with the same
# name already exists, the attribute value will be updated with the
# new value in {\bf value}.  
#
# @param element The element on which to set the attribute.
# @param name The name of the attribute.
# @param value The value of the attribute. Note that this is a non-parsed string and any markup must
# be escaped.
#
# @return [int] An integer representing of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf element}, 
#		   {\bf name}, or {\bf value} is {\tt NULL}.
#	 \item {\tt IXML_INVALID_CHARACTER_ERR}: {\bf name} contains an 
#		   illegal character.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete the operation.
#   \end{itemize}
def ixmlElement_setAttribute(element, name, value):
	return IXMLLib.ixmlElement_setAttribute(element, name, value)

IXMLLib.ixmlElement_setAttribute.restype = c_int
IXMLLib.ixmlElement_setAttribute.argtypes = [POINTER(IXML_Element), DOMString, DOMString]

##
# Removes an attribute by name.  
#
# @param element The element from which to remove the attribute.
# @param name The name of the attribute to remove.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf element} or 
#		   {\bf name} is {\tt NULL}.
#   \end{itemize}
def ixmlElement_removeAttribute(element, name):
	return IXMLLib.ixmlElement_removeAttribute(element, name)

IXMLLib.ixmlElement_removeAttribute.restype = c_int
IXMLLib.ixmlElement_removeAttribute.argtypes = [POINTER(IXML_Element), DOMString]

##
# Retrieves an attribute node by name.  See 
# {\bf ixmlElement_getAttributeNodeNS} to retrieve an attribute node using
# a qualified name or namespace URI.
#
# @param element The element from which to get the attribute node.
# @param name The name of the attribute node to find.
#
# @return [Attr*] A pointer to the attribute matching {\bf name} or 
#				 {\tt NULL} on an error.
def ixmlElement_getAttributeNode(element, name):
	return IXMLLib.ixmlElement_getAttributeNode(element, name)

IXMLLib.ixmlElement_getAttributeNode.restype = POINTER(IXML_Attr)
IXMLLib.ixmlElement_getAttributeNode.argtypes = [POINTER(IXML_Element), DOMString]

##
# Adds a new attribute node to an {\bf Element}.  If an attribute already
# exists with {\bf newAttr} as a name, it will be replaced with the
# new one and the old one will be returned in {\bf rtAttr}.
#
# @param element The element in which to add the new attribute.
# @param newAttr The new Attr to add.
# @param rtAttr A pointer to an Attr where the old Attr will be stored. This will have a None
# if no prior node existed.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf element} or 
#		   {\bf newAttr} is {\tt NULL}.
#	 \item {\tt IXML_WRONG_DOCUMENT_ERR}: {\bf newAttr} does not belong 
#		   to the same one as {\bf element}.
#	 \item {\tt IXML_INUSE_ATTRIBUTE_ERR}: {\bf newAttr} is already 
#		   an attribute of another {\bf Element}.
#   \end{itemize}
def ixmlElement_setAttributeNode(element, newAttr, rtAttr):
	return IXMLLib.ixmlElement_setAttributeNode(element, newAttr, rtAttr)

IXMLLib.ixmlElement_setAttributeNode.restype = c_int
IXMLLib.ixmlElement_setAttributeNode.argtypes = [POINTER(IXML_Element), POINTER(IXML_Attr), POINTER(POINTER(IXML_Attr))]

##
# Removes the specified attribute node from an {\bf Element}.  
#
# @param element The element from which to remove the attribute.
# @param oldAttr The attribute to remove from the element.
# @param rtAttr A pointer to an attribute in which to place the removed attribute.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf element} or 
#		   {\bf oldAttr} is {\tt NULL}.
#	 \item {\tt IXML_NOT_FOUND_ERR}: {\bf oldAttr} is not among the list 
#		   attributes of {\bf element}.
#   \end{itemize}
def ixmlElement_removeAttributeNode(element, oldAttr, rtAttr):
	return IXMLLib.ixmlElement_removeAttributeNode(element, oldAttr, rtAttr)

IXMLLib.ixmlElement_removeAttributeNode.restype = c_int
IXMLLib.ixmlElement_removeAttributeNode.argtypes = [POINTER(IXML_Element), POINTER(IXML_Attr), POINTER(POINTER(IXML_Attr))]

##
# Returns a {\bf NodeList} of all {\it descendant} {\bf Elements} with
# a given tag name, in the order in which they are encountered in a
# pre-order traversal of this {\bf Element} tree.
#
# @param element The element from which to start the search.
# @param tagName The name of the tag for which to search.
#
# @return [NodeList*] A {\bf NodeList} of the matching {\bf Element}s or 
#					 {\tt NULL} on an error.
def ixmlElement_getElementsByTagName(element, tagName):
	return IXMLLib.ixmlElement_getElementsByTagName(element, tagName)

IXMLLib.ixmlElement_getElementsByTagName.restype = POINTER(IXML_NodeList)
IXMLLib.ixmlElement_getElementsByTagName.argtypes = [POINTER(IXML_Element), DOMString]

##
# Retrieves an attribute value using the local name and namespace URI.
#
# @param element The element from which to get teh attribute value.
# @param namespaceURI The namespace URI of teh attribute.
# @param localname The local name of teh attribute.
#
# @return [DOMString] A {\bf DOMString} representing the value of the 
#					 matching attribute.
def ixmlElement_getAttributeNS(element, namespaceURI, localname):
	return IXMLLib.ixmlElement_getAttributeNS(element, namespaceURI, localname)

IXMLLib.ixmlElement_getAttributeNS.restype = DOMString
IXMLLib.ixmlElement_getAttributeNS.argtypes = [POINTER(IXML_Element), DOMString, DOMString]

##
# Adds a new attribute to an {\bf Element} using the local name and 
# namespace URI.  If another attribute matches the same local name and 
# namespace, the prefix is changed to be the prefix part of the 
# {\tt qualifiedName} and the value is changed to {\bf value}.
#
# @param element The element on which to set the attribute.
# @param namespaceURI The namespace URI of the new attribute.
# @param qualifiedName The qualified name of the attribute.
# @param value The new value for the attribute.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf element}, 
#		   {\bf namespaceURI}, {\bf qualifiedName}, or {\bf value} is 
#		   {\tt NULL}.
#	 \item {\tt IXML_INVALID_CHARACTER_ERR}: {\bf qualifiedName} contains 
#		   an invalid character.
#	 \item {\tt IXML_NAMESPACE_ERR}: Either the {\bf qualifiedName} or 
#		   {\bf namespaceURI} is malformed.  Refer to the DOM2-Core for 
#		   possible reasons.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exist 
#		   to complete the operation.
#	 \item {\tt IXML_FAILED}: The operation could not be completed.
#   \end{itemize}
def ixmlElement_setAttributeNS(element, namespaceURI, qualifiedName, value):
	return IXMLLib.ixmlElement_setAttributeNS(element, namespaceURI, qualifiedName, value)

IXMLLib.ixmlElement_setAttributeNS.restype = c_int
IXMLLib.ixmlElement_setAttributeNS.argtypes = [POINTER(IXML_Element), DOMString, DOMString, DOMString]

##
# Removes an attribute using the namespace URI and local name.
#
# @param element The element from which to remove the attribute.
# @param namespaceURI The namespace URI of the attribute.
# @param localName The local name of the attribute.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf element}, 
#		   {\bf namespaceURI}, or {\bf localName} is {\tt NULL}.
#   \end{itemize}
def ixmlElement_removeAttributeNS(element, namespaceURI, localName):
	return IXMLLib.ixmlElement_removeAttributeNS(element, namespaceURI, localName)

IXMLLib.ixmlElement_removeAttributeNS.restype = c_int
IXMLLib.ixmlElement_removeAttributeNS.argtypes = [POINTER(IXML_Element), DOMString, DOMString]

##
# Retrieves an {\bf Attr} node by local name and namespace URI.
#
# @param element The element from which to get the attribute.
# @param namespaceURI The namespace URI of the attribute.
# @param localName The local name of the attribute.
#
# @return [Attr*] A pointer to an {\bf Attr} or {\tt NULL} on an error.
def ixmlElement_getAttributeNodeNS(element, namespaceURI, localName):
	return IXMLLib.ixmlElement_getAttributeNodeNS(element, namespaceURI, localName)

IXMLLib.ixmlElement_getAttributeNodeNS.restype = POINTER(IXML_Attr)
IXMLLib.ixmlElement_getAttributeNodeNS.argtypes = [POINTER(IXML_Element), DOMString, DOMString]

##
# Adds a new attribute node.  If an attribute with the same local name
# and namespace URI already exists in the {\bf Element}, the existing 
# attribute node is replaced with {\bf newAttr} and the old returned in 
# {\bf rcAttr}.
#
# @param element The element in which to add the attribute node.
# @param newAttr The new Attr to add.
# @param rcAttr A pointer to the replaced Attr, if it exists.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: Either {\bf element} or 
#		   {\bf newAttr} is {\tt NULL}.
#	 \item {\tt IXML_WRONG_DOCUMENT_ERR}: {\bf newAttr} does not belong 
#		   to the same document as {\bf element}.
#	 \item {\tt IXML_INUSE_ATTRIBUTE_ERR}: {\bf newAttr} already is an 
#		   attribute of another {\bf Element}.
#   \end{itemize}
def ixmlElement_setAttributeNodeNS(element, newAttr, rcAttr):
	return IXMLLib.ixmlElement_setAttributeNodeNS(element, newAttr, rcAttr)

IXMLLib.ixmlElement_setAttributeNodeNS.restype = c_int
IXMLLib.ixmlElement_setAttributeNodeNS.argtypes = [POINTER(IXML_Element), POINTER(IXML_Attr), POINTER(POINTER(IXML_Attr))]

##
# Returns a {\bf NodeList} of all {\it descendant} {\bf Elements} with a
# given tag name, in the order in which they are encountered in the
# pre-order traversal of the {\bf Element} tree.
#
# @param element The element form which to start the search.
# @param namespaceURI The namespace URi of the elements to find.
# @param localName The local name of the Elements to find.
#
# @return [NodeList*] A {\bf NodeList} of matching {\bf Element}s or 
#					 {\tt NULL} on an error.
def ixmlElement_getElementsByTagNameNS(element, namespaceURI, localName):
	return IXMLLib.ixmlElement_getElementsByTagNameNS(element, namespaceURI, localName)

IXMLLib.ixmlElement_getElementsByTagNameNS.restype = POINTER(IXML_NodeList)
IXMLLib.ixmlElement_getElementsByTagNameNS.argtypes = [POINTER(IXML_Element), DOMString, DOMString]

##
# Queries whether the {\bf Element} has an attribute with the given name
# or a default value.
#
# @param element The element on which to check for the attribute.
# @param name The name of the attribute for which to check.
#
# @return [BOOL] {\tt TRUE} if the {\bf Element} has an attribute with 
#				this name or has a default value for that attribute, 
#				otherwise {\tt FALSE}.
def ixmlElement_hasAttribute(element, name):
	return IXMLLib.ixmlElement_hasAttribute(element, name)

IXMLLib.ixmlElement_hasAttribute.restype = c_int
IXMLLib.ixmlElement_hasAttribute.argtypes = [POINTER(IXML_Element), DOMString]

##
# Queries whether the {\bf Element} has an attribute with the given
# local name and namespace URI or has a default value for that attribute.
#
# @param element The element on which to check for the attribute.
# @param namespaceURI The namespace URI of the attribute.
# @param localName The local name of the attribute.
#
# @return [BOOL] {\tt TRUE} if the {\bf Element} has an attribute with 
#				the given namespace and local name or has a default 
#				value for that attribute, otherwise {\tt FALSE}.
def ixmlElement_hasAttributeNS(element, namespaceURI, localName):
	return IXMLLib.ixmlElement_hasAttributeNS(element, namespaceURI, localName)

IXMLLib.ixmlElement_hasAttributeNS.restype = c_int
IXMLLib.ixmlElement_hasAttributeNS.argtypes = [POINTER(IXML_Element), DOMString, DOMString]

##
# Frees the given {\bf Element} and any subtree of the {\bf Element}.
#
# @param element The element to free.
#
# @return [void] This function does not return a value.
def ixmlElement_free(element):
	return IXMLLib.ixmlElement_free(element)

IXMLLib.ixmlElement_free.argtypes = [POINTER(IXML_Element)]

##
# Returns the number of items contained in this {\bf NamedNodeMap}.
#
# @param nnMap The NamedNodeMap from which to retrieve the size.
#
# @return [unsigned long] The number of nodes in this map.
def ixmlNamedNodeMap_getLength(nnMap):
	return IXMLLib.ixmlNamedNodeMap_getLength(nnMap)

IXMLLib.ixmlNamedNodeMap_getLength.restype = c_ulong
IXMLLib.ixmlNamedNodeMap_getLength.argtypes = [POINTER(IXML_NamedNodeMap)]

##
# Retrieves a {\bf Node} from the {\bf NamedNodeMap} by name.
#
# @param nnMap The NamedNodeMap to search.
# @param name The name of the node to find.
#
# @return [Node*] A {\bf Node} or {\tt NULL} if there is an error.
def ixmlNamedNodeMap_getNamedItem(nnMap, name):
	return IXMLLib.ixmlNamedNodeMap_getNamedItem(nnMap, name)

IXMLLib.ixmlNamedNodeMap_getNamedItem.restype = POINTER(IXML_Node)
IXMLLib.ixmlNamedNodeMap_getNamedItem.argtypes = [POINTER(IXML_NamedNodeMap), DOMString]

##
# Retrieves a {\bf Node} from a {\bf NamedNodeMap} specified by a
# numerical index.
#
# @param nnMap The NamedNodeMap from which to remove the Node.
# @param index The index into the map to remove.
#
# @return [Node*] A pointer to the {\bf Node}, if found, or {\tt NULL} if 
#				 it wasn't.
def ixmlNamedNodeMap_item(nnMap, index):
	return IXMLLib.ixmlNamedNodeMap_item(nnMap, index)

IXMLLib.ixmlNamedNodeMap_item.restype = POINTER(IXML_Node)
IXMLLib.ixmlNamedNodeMap_item.argtypes = [POINTER(IXML_NamedNodeMap), c_ulong]

##
# Frees a {\bf NamedNodeMap}.  The {\bf Node}s inside the map are not
# freed, just the {\bf NamedNodeMap} object.
#
# @param nnMap The NamedNodeMap to free.
#
# @return [void] This function does not return a value.
def ixmlNamedNodeMap_free(nnMap):
	IXMLLib.ixmlNamedNodeMap_free(nnMap)

IXMLLib.ixmlNamedNodeMap_free.argtypes = [POINTER(IXML_NamedNodeMap)]

##
# Retrieves a {\bf Node} from a {\bf NodeList} specified by a 
# numerical index.
#
# @param nList The NodeList from which to retrieve the Node.
# @param index The index into the NodeList to retrieve.
#
# @return [Node*] A pointer to a {\bf Node} or {\tt NULL} if there was an 
#				 error.
def ixmlNodeList_item(nList, index):
	return IXMLLib.ixmlNodeList_item(nList, index)

IXMLLib.ixmlNodeList_item.restype = POINTER(IXML_Node)
IXMLLib.ixmlNodeList_item.argtypes = [POINTER(IXML_NodeList), c_ulong]

##
# Returns the number of {\bf Nodes} in a {\bf NodeList}.
#
# @param nList The NodeList for which to retrieve the number of Nodes.
#
# @return [unsigned long] The number of {\bf Nodes} in the {\bf NodeList}.
def ixmlNodeList_length(nList):
	return IXMLLib.ixmlNodeList_length(nList)

IXMLLib.ixmlNodeList_length.restype = c_ulong
IXMLLib.ixmlNodeList_length.argtypes = [POINTER(IXML_NodeList)]

##
# Frees a {\bf NodeList} object.  Since the underlying {\bf Nodes} are
# references, they are not freed using this operating.  This only
# frees the {\bf NodeList} object.
#
# @param nList The NodeList to free.
#
# @return [void] This function does not return a value.
def ixmlNodeList_free(nList):
	return IXMLLib.ixmlNodeList_free(nList)

IXMLLib.ixmlNodeList_free.argtypes = [POINTER(IXML_NodeList)]

##
# Renders a {\bf Node} and all sub-elements into an XML document
# representation.  The caller is required to free the {\bf DOMString}
# returned from this function using {\bf ixmlFreeDOMString} when it
# is no longer required.
#
# Note that this function can be used for any {\bf Node}-derived
# interface.  The difference between {\bf ixmlPrintDocument} and
# {\bf ixmlPrintNode} is {\bf ixmlPrintDocument} includes the XML prolog
# while {\bf ixmlPrintNode} only produces XML elements. An XML
# document is not well formed unless it includes the prolog
# and at least one element.
#
# This function  introduces lots of white space to print the
# {\bf DOMString} in readable  format.
#
# @return [DOMString] A {\bf DOMString} with the XML document representation 
#					 of the DOM tree or {\tt NULL} on an error.
def ixmlPrintDocument(doc):
	return IXMLLib.ixmlPrintDocument(doc)

IXMLLib.ixmlPrintDocument.restype = DOMString
IXMLLib.ixmlPrintDocument.argtypes = [POINTER(IXML_Document)]

##
# Renders a {\bf Node} and all sub-elements into an XML text
# representation.  The caller is required to free the {\bf DOMString}
# returned from this function using {\bf ixmlFreeDOMString} when it
# is no longer required.
#
# Note that this function can be used for any {\bf Node}-derived
# interface.  A similar {\bf ixmlPrintDocument} function is defined
# to avoid casting when printing whole documents. This function
# introduces lots of white space to print the {\bf DOMString} in readable
# format.
#
# @param doc The root of the Node tree to render to XML text.
#
# @return [DOMString] A {\bf DOMString} with the XML text representation 
#					 of the DOM tree or {\tt NULL} on an error.
def ixmlPrintNode(doc):
	return IXMLLib.ixmlPrintNode(doc)

IXMLLib.ixmlPrintNode.restype = DOMString
IXMLLib.ixmlPrintNode.argtypes = [POINTER(IXML_Node)]

##
# Renders a {\bf Node} and all sub-elements into an XML document
# representation.  The caller is required to free the {\bf DOMString}
# returned from this function using {\bf ixmlFreeDOMString} when it
# is no longer required.
#
# Note that this function can be used for any {\bf Node}-derived
# interface.  The difference between {\bf ixmlDocumenttoString} and
# {\bf ixmlNodetoString} is {\bf ixmlDocumenttoString} includes the XML
# prolog while {\bf ixmlNodetoString} only produces XML elements. An XML
# document is not well formed unless it includes the prolog
# and at least one element.
#
# @return [DOMString] A {\bf DOMString} with the XML text representation 
#					 of the DOM tree or {\tt NULL} on an error.
def ixmlDocumenttoString(doc):
	return IXMLLib.ixmlDocumenttoString(doc)

IXMLLib.ixmlDocumenttoString.restype = DOMString
IXMLLib.ixmlDocumenttoString.argtypes = [POINTER(IXML_Document)]

##
# Renders a {\bf Node} and all sub-elements into an XML text
# representation.  The caller is required to free the {\bf DOMString}
# returned from this function using {\bf ixmlFreeDOMString} when it
# is no longer required.
#
# Note that this function can be used for any {\bf Node}-derived
# interface.  The difference between {\bf ixmlNodetoString} and
# {\bf ixmlDocumenttoString} is {\bf ixmlNodetoString} does not include
# the XML prolog, it only produces XML elements.
#
# @param doc The root of the Node tree to render to XML text.
#
# @return [DOMString] A {\bf DOMString} with the XML text representation 
#					 of the DOM tree or {\tt NULL} on an error.
def ixmlNodetoString(doc):
	return IXMLLib.ixmlNodetoString(doc)

IXMLLib.ixmlNodetoString.restype = DOMString
IXMLLib.ixmlNodetoString.argtypes = [POINTER(IXML_Node)]

##
# Makes the XML parser more tolerant to malformed text.
#	  
# If {\bf errorChar} is 0 (default), the parser is strict about XML 
# encoding : invalid UTF-8 sequences or "&" entities are rejected, and 
# the parsing aborts.
# If {\bf errorChar} is not 0, the parser is relaxed : invalid UTF-8 
# characters are replaced by the {\bf errorChar}, and invalid "&" entities 
# are left untranslated. The parsing is then allowed to continue.
def ixmlRelaxParser(errorChar):
	IXMLLib.ixmlRelaxParser(errorChar)

IXMLLib.ixmlRelaxParser.argtypes = [c_char]

##
# Parses an XML text buffer converting it into an IXML DOM representation.
#
# @param bufferStr The buffer that contains the XML text to convert to a Document.
#
# @return [Document*] A {\bf Document} if the buffer correctly parses or 
#					 {\tt NULL} on an error.
def ixmlParseBuffer(bufferStr):
	return IXMLLib.ixmlParseBuffer(bufferStr)

IXMLLib.ixmlParseBuffer.restype = POINTER(IXML_Document)
IXMLLib.ixmlParseBuffer.argtypes = [c_char_p]

##
# Parses an XML text buffer converting it into an IXML DOM representation.
#
# The {\bf ixmlParseBufferEx} API differs from the {\bf ixmlParseBuffer}
# API in that it returns an error code representing the actual failure
# rather than just {\tt NULL}.
#
# @param bufferStr The buffer that contains the XML text to convert to a Document.
# @param doc A pointer to store the Document if file correctly parses or None on an error.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: The {\bf buffer} is not a valid 
#		   pointer.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlParseBufferEx(bufferStr, doc):
	return IXMLLib.ixmlParseBufferEx(bufferStr, doc)

IXMLLib.ixmlParseBufferEx.restype = c_int
IXMLLib.ixmlParseBufferEx.argtypes = [c_char_p, POINTER(POINTER(IXML_Document))]

##
# Parses an XML text file converting it into an IXML DOM representation.
#
# @param xmlFile The filename of the XML text to convert to a document.
#
# @return [Document*] A {\bf Document} if the file correctly parses or 
#					 {\tt NULL} on an error.
def ixmlLoadDocument(xmlFile):
	return IXMLLib.ixmlLoadDocument(xmlFile)

IXMLLib.ixmlLoadDocument.restype = POINTER(IXML_Document)
IXMLLib.ixmlLoadDocument.argtypes = [c_char_p]

##
# Parses an XML text file converting it into an IXML DOM representation.
#
# The {\bf ixmlLoadDocumentEx} API differs from the {\bf ixmlLoadDocument}
# API in that it returns a an error code representing the actual failure
# rather than just {\tt NULL}.
#
# @param xmlFile The filename of the XML text to convert to a Document.
# @param doc A pointer to the Document if the file correctly parses or None on an error.
#
# @return [int] An integer representing one of the following:
#   \begin{itemize}
#	 \item {\tt IXML_SUCCESS}: The operation completed successfully.
#	 \item {\tt IXML_INVALID_PARAMETER}: The {\bf xmlFile} is not a valid 
#		   pointer.
#	 \item {\tt IXML_INSUFFICIENT_MEMORY}: Not enough free memory exists 
#		   to complete this operation.
#   \end{itemize}
def ixmlLoadDocumentEx(xmlFile, doc):
	return IXMLLib.ixmlLoadDocumentEx(xmlFile, doc)

IXMLLib.ixmlLoadDocumentEx.restype = c_int
IXMLLib.ixmlLoadDocumentEx.argtypes = [c_char_p, POINTER(POINTER(IXML_Document))]

##
# Clones an existing {\bf DOMString}.
#
# @param src The source DOMString to clone.
#
# @return [DOMString] A new {\bf DOMString} that is a duplicate of the 
#					 original or {\tt NULL} if the operation could not 
#					 be completed.
def ixmlCloneDOMString(src):
	return IXMLLib.ixmlCloneDOMString(src)

IXMLLib.ixmlCloneDOMString.restype = DOMString
IXMLLib.ixmlCloneDOMString.argtypes = [DOMString]

##
# Frees a DOMString.
#
# @param buf The DOMString to free.
def ixmlFreeDOMString(buf):
	IXMLLib.ixmlFreeDOMString(buf)

IXMLLib.ixmlFreeDOMString.argtypes = [DOMString]
