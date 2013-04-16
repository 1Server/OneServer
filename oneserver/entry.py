##
# This class represents an object in the directory tree
# It can be either a Directory or a File, Directories have children is not None
# Files have children is None
class Entry:

    nextId = 0

    ##
    # This is the ctor for the entry
    # @param fullPath The full path to the file on the local file system
    # @param dlnaProfile The valid DLNA profile that matches the file
    # @param parent The parent object for the entry, only the root entry can have this be None
    # @param children A List of children, should only be None for Files, Directories need at least an empty list
    # @param title The title of the entry
    # @param url The url that this file can be played from, should be id.(extension) ala id.mp4
    # @param size The size of the file
    # @param fh A function to generate file handles for the entry.  This takes 1 argument which is an Entry
    def __init__(self, fullPath, dlnaProfile, parent, children, title, url, size, fhFunction):
        if (dlnaProfile == None):
            raise TypeError("Invalid DLNA Profile")
        
        self._id     = Entry.nextId
        Entry.nextId     = Entry.nextId + 1

        self.fullPath     = fullPath
        self.dlnaProfile= dlnaProfile
        self.parent     = parent
        self.children     = children
        self.title     = title
        self.url     = url if url != "" else str(self._id) + ".mp4"
        self.size     = size
        self.fhFunction     = fhFunction

    ##
    # Creates a new file handle for the entry
    def generateFileHandle(self):
        return self.fhFunction(self)
    ##
    # Adds a child to the Entry
    # @raise TypeError if child is None or children is None
    # @param child The child to add
    def addChild(self, child):
        if (child == None):
            raise TypeError("Invalid child to add")
        if (self.children == None):
            raise TypeError("Tried adding a child to a file entry")
        self.children.append(child)

    ##
    # Removes a child from the Entry
    # @raise TypeError if child is None or children is None
    # @param child the child to remove
    def removeChild(self,child):
        if (child == None):
            raise TypeError("Invalid child to remove")
        if (self.children == None):
            raise TypeError("Tried removing child from file entry")
        self.children.remove(child)
        
    ##
    # Tries to find the child with the given id in the current Entries child or below
    # @param _id The id to look for
    def getChild(self, _id):
        if _id == 0:
            if self.parent == None:
                return self #we are looking for the root and we are it
            else:
                return None #We are being stupid and looking to low for the root
        elif _id is self._id:
            return self #Looking for ourselves

        if self.children == None:
            return None
        for child in self.children:
            if _id == child._id:
                return child
        #None of the direct children was the desired entry, go recursive
        for child in self.children:
            entry = child.getChild(_id)
            if entry != None:
                return entry
        #Still haven't found the entry, return None
        return None