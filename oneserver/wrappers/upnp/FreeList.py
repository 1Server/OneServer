from manager import OneServerManager

import sys
try:
	from ctypes import cdll
	from ctypes import c_int,c_void_p,c_long
	from ctypes import POINTER,Structure
	from ctypes.util import find_library
except ImportError:
	OneServerManager().log.error('Library CTypes not found.')
	sys.exit()

##
# Free list node. Points to next free item. Memory for node
# is borrowed from allocated items.
class FREELISTNODE(Structure):
	pass

FREELISTNODE._fields_ = [('next', POINTER(FREELISTNODE))]

class FreeListNode(FREELISTNODE):
	pass

##
# Stores head and size of free list, as well as mutex for protection.
class FREELIST(Structure):
	pass

FREELIST._fields_ = [
	('head', POINTER(FreeListNode)),
	('element_size', c_long),
	('maxFreeListLength', c_int),
	('freeListLength', c_int)
]

class FreeList(FREELIST):
	pass

FreeListLib = cdll.LoadLibrary(find_library('upnp'))

FreeListLib.FreeListInit.restype = c_int
FreeListLib.FreeListInit.argtypes = [POINTER(FreeList), c_long, c_int]

FreeListLib.FreeListAlloc.restype = c_void_p
FreeListLib.FreeListAlloc.argtypes = [POINTER(FreeList)]

FreeListLib.FreeListFree.restype = c_int
FreeListLib.FreeListFree.argtypes = [POINTER(FreeList), c_void_p]

FreeListLib.FreeListDestroy.restype = c_int
FreeListLib.FreeListDestroy.argtypes = [POINTER(FreeList)]

##
# Initializes Free List. Must be called first. And only once for
# FreeList.
#
# @param free_list must be valid, non null, pointer to a linked list.
# @param elementSize size of elements to store in free list.
# @param maxFreeListSize max size that the free list can grow
# to before returning memory to 0.5.
#
# @return 0 on success. Nonzero on failure. Always returns 0.
def FreeListInit(free_list, elementSize, maxFreeListSize):
	return FreeListLib.FreeListInit(free_list, elementSize, maxFreeListSize)

##
# Allocates chunk of set size. If a free item is available in the list, returns the stored item.
# Otherwise calls the O.S. to allocate memory.
#
# @param free_list must be valid, non null, pointer to a linked list.
#
# @return Non None on success. None of failure.
def FreeListAlloc(free_list):
	return FreeListLib.FreeListAlloc(free_list)

##
# Returns an item to the Free List. If the free list is smaller than the max size then
# adds the item to the free list. Otherwise returns the item to the O.S.
#
# @param free_list must be valid, non None, pointer to a linked list.
#
# @return 0 on success. Nonzero on failure. Always returns 0.
def FreeListFree(free_list, element):
	return FreeListLib.FreeListFree(free_list, element)

##
# Releases the resources stored with the free list.
#
# @param free_list must be valid, non None, pointer to a linked list.
#
# @returns 0 on success, nonzero on failure
def FreeListDestroy(free_list):
	return FreeListLib.FreeListDestroy(free_list)
