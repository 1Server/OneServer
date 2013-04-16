from manager import OneServerManager

import sys
try:
	from ctypes import cdll
	from ctypes import c_long,c_int,c_void_p
	from ctypes import POINTER,Structure,CFUNCTYPE
	from ctypes.util import find_library
except ImportError:
	OneServerManager().log.error('Library CTypes not found.')
	sys.exit()

from FreeList import FreeList

EOUTOFMEM = -7 & 1 << 29

FREELISTSIZE = 100

LIST_SUCCESS = 1

LIST_FAIL = 0

##
# Function for freeing list items.
free_function = CFUNCTYPE(None, c_void_p)

##
# Function for comparing list items.
#
# @return 1 if itemA == itemB
cmp_routine = CFUNCTYPE(c_int, c_void_p, c_void_p)

##
# Linked list node. Stores generic item and pointers to next and prev.
class LISTNODE(Structure):
	pass
LISTNODE._fields_ = [
	('prev', POINTER(LISTNODE)),
	('next', POINTER(LISTNODE)),
	('item', c_void_p)
]

class ListNode(LISTNODE):
	pass

##
# Linked list (no protection). Because this is for internal use, parameters are NOT
# checked for validity. The first item of the list is stored at node: head->next.
# The last item of the list is stored at node: tail->prev. If head->next = tail,
# then list is empty.
class LINKEDLIST(Structure):
	pass

LINKEDLIST._fields_ = [
	('head', ListNode),
	('tail', ListNode),
	('size', c_long),
	('freeNodeList', FreeList),
	('free_func', free_function),
	('cmp_func', cmp_routine)
]

class LinkedList(LINKEDLIST):
	pass

LinkedListLib = cdll.LoadLibrary(find_library('upnp'))

LinkedListLib.ListInit.restype = c_int
LinkedListLib.ListInit.argtypes = [POINTER(LinkedList), cmp_routine, free_function]

LinkedListLib.ListAddHead.restype = POINTER(ListNode)
LinkedListLib.ListAddHead.argtypes = [POINTER(LinkedList), c_void_p]

LinkedListLib.ListAddTail.restype = POINTER(ListNode)
LinkedListLib.ListAddTail.argtypes = [POINTER(LinkedList), c_void_p]

LinkedListLib.ListAddAfter.restype = POINTER(ListNode)
LinkedListLib.ListAddAfter.argtypes = [POINTER(LinkedList), c_void_p, POINTER(ListNode)]

LinkedListLib.ListAddBefore.restype = POINTER(ListNode)
LinkedListLib.ListAddBefore.argtypes = [POINTER(LinkedList), c_void_p, POINTER(ListNode)]

LinkedListLib.ListDelNode.restype = c_void_p
LinkedListLib.ListDelNode.argtypes = [POINTER(LinkedList), POINTER(ListNode), c_int]

LinkedListLib.ListDestroy.restype = c_int
LinkedListLib.ListDestroy.argtypes = [POINTER(LinkedList), c_int]

LinkedListLib.ListHead.restype = POINTER(ListNode)
LinkedListLib.ListHead.argstyeps = [POINTER(LinkedList)]

LinkedListLib.ListTail.restype = POINTER(ListNode)
LinkedListLib.ListTail.argtypes = [POINTER(LinkedList)]

LinkedListLib.ListNext.restype = POINTER(ListNode)
LinkedListLib.ListNext.argtypes = [POINTER(LinkedList), POINTER(ListNode)]

LinkedListLib.ListPrev.restype = POINTER(ListNode)
LinkedListLib.ListPrev.argtypes = [POINTER(LinkedList), POINTER(ListNode)]

LinkedListLib.ListFind.restype = POINTER(ListNode)
LinkedListLib.ListFind.argtypes = [POINTER(LinkedList), POINTER(ListNode), c_void_p]

LinkedListLib.ListSize.restype = c_int
LinkedListLib.ListSize.argtypes = [POINTER(LinkedList)]

##
# Initializes LinkedList. Must be called first. And only once per list.
#
# @param llist must be valid, non none pointer to a linked list
# @param cmp_func function used to compare items
# @param free_func function used to free items
#
# @return 0 on success, EOUTOFMEM on failure
def ListInit(llist, cmp_func, free_func):
	return LinkedListLib.ListInit(llist, cmp_func, free_func)

##
# Adds a node to the head of the list. Node gets immediately after list.head.
#
# @param llist must be valid, non none, pointer to a linked list.
# @param item item to be added.
#
# @return the pointer to the list node on success, none on failure.
def ListAddHead(llist, item):
	return LinkedListLib.ListAddHead(llist, item)

##
# Adds a node to the tail of the list. Node gets added immediately before list.tail.
#
# @param llist must be valid, non none, pointer to a linked list.
# @param item item to be added
#
# @return the pointer to the list node on success, none on failure
def ListAddTail(llist, item):
	return LinkedListLib.ListAddtail(llist, item)

##
# Adds a node after the specified node. Node gets added immediately after bnode.
#
# @param llist must be valid, non none, pointer to a linked list.
# @param item item to be added.
#
# @return The pointer to the list node on success, none on failure
def ListAddAfter(llist, item, bnode):
	return LinkedListLib.ListAddAfter(llist, item, bnode)

##
# Adds a node before the specified node. Node gets added immediately before anode.
#
# @param llist must be valid, non none, pointer to a linked list.
# @param anode node to be add the item in front of.
# @param item item to be added.
#
# @return the pointer to the item stored in the node or none if the item is freed.
def ListAddBefore(llist, item, anode):
	return LinkedListLib.ListAddBefore(llist, item, anode)

##
# Removes a node from the list. The memory for the node is freed.
#
# @param llist must be valid, non none, pointer to a linked list
# @param dnode node to delete
# @param freeitem if ! 0 then item is freed using free function. if 0 or
# free function is none then item is not freed.
def ListDelNode(llist, dnode, freeItem):
	return LinkedListLib.ListDelNode(llist, dnode, freeItem)

##
# Removes all memory associated with list node. Does not free linked list.
#
# @param list must be valid, non none, pointer to a linked list.
# @param freeitem if ! 0 then item is freed using free function. if 0 or
# free function is none then item is not freed.
#
# @return 0 on success. Always returns 0.
def ListDestroy(llist, freeItem):
	return LinkedListLib.ListDelNode(llist, freeItem)

##
# Returns the head of the list.
#
# @param llist must be valid, non none, pointer to a linked list.
#
# @return the head of the list. None if list is empty.
def ListHead(llist):
	return LinkedListLib.ListHead(llist)

##
# Returns the tail of the list.
#
# @param llist must be valid, non none, pointer to a linked list.
#
# @return The tail of the list. None if the list is empty.
def ListTail(llist):
	return LinkedListLib.ListTail(llist)

##
# Returns the next item in the list.
#
# @param llist must be valid, non none, pointer to a linked list.
#
# @return The next item in the list. None if there are no more items in the list.
def ListNext(llist, node):
	return LinkedListLib.ListNext(llist)

##
# Returns the previous item in the list.
#
# @param llist must be valid, non none, pointer to a linked list.
#
# @return the previous item in the list. None if there are no more items in the list.
def ListPrev(llist, node):
	return LinkedListLib.ListPrev(llist, node)

##
# Finds the specified item in the list. Uses the compare function specified in ListInit.
# If compare function is None then compares items as pointers.
#
# @param llist must be valid, non none, pointer to a linked list
# @param start the node to start from. None if to start from beginning.
# @param item the item to search for
#
# @return The node containing the item. None if no node contains the item.
def ListFind(llist, start, item):
	return LinkedListLib.ListFind(llist, start, item)

##
# Returns the size of the list.
#
# @param llist must be valid, non none, pointer to a linked list.
#
# @return The number of items in the list.
def ListSize(llist):
	return LinkedListLib.ListSize(llist)
