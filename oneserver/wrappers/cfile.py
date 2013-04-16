from manager import OneServerManager

import sys
try:
    from ctypes import pythonapi,py_object
    from ctypes import c_char_p,c_int
    from ctypes import POINTER,Structure,CFUNCTYPE
except ImportError:
        OneServerManager().log.error('Library CTypes not found.')
        sys.exit()

try:
    class FILE(Structure):
        pass
    FILE_ptr = POINTER(FILE)

    PyFile_FromFile = pythonapi.PyFile_FromFile
    PyFile_FromFile.restype = py_object
    PyFile_FromFile.argtypes = [FILE_ptr,
                                c_char_p,
                                c_char_p,
                                CFUNCTYPE(c_int, FILE_ptr)]

    PyFile_AsFile = pythonapi.PyFile_AsFile
    PyFile_AsFile.restype = FILE_ptr
    PyFile_AsFile.argtypes = [py_object]
except AttributeError:
    del FILE_ptr

