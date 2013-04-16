import unittest

from collections import defaultdict

from plugin.interface import IStoragePlugin
from vfs import VirtualFileSystem,DirectoryError,EntryNotFoundError
from entry import Entry
from manager import OneServerManager

class TestVirtualFileSystem(unittest.TestCase):
	
	##
	# Basic setup that happens before every test.
	def setUp(self):
		self.vfs = VirtualFileSystem()
		self.plugin = testPlugin()
		self.vfs.loadDataSource(self.plugin)
	
	##
	# Tests __init__
	def test_Init(self):
		#Try the normal constructor
		vfs = VirtualFileSystem()
		
	##
	# Tests checkPath
	def test_checkPath(self):
		with self.assertRaises(ValueError):
			self.vfs.checkPath(None)
		with self.assertRaises(ValueError):
			self.vfs.checkPath("")
		with self.assertRaises(ValueError):
			self.vfs.checkPath("NotAPath")
		self.assertEquals(VirtualFileSystem.FILE, self.vfs.checkPath("/path/to/file"))
		self.assertEquals(VirtualFileSystem.DIR , self.vfs.checkPath("d/path/to/directory"))
			
	##
	# Tests get
	def test_get(self):
		#Check special case outside of plugins
		with self.assertRaises(DirectoryError):
			self.vfs.get("/")
			
		self.vfs.get("/TestPlugin/file1")
		self.assertEquals(self.plugin.getPaths["/TestPlugin/file1"], 1)
		
		with self.assertRaises(EntryNotFoundError):
			self.vfs.get("/TestPlugin/NotHere")
			
		entry = self.vfs.get("/TestPlugin/file1")
		self.assertEquals(self.plugin.files["file1"], entry)
		
	##
	# Tests list
	def test_list(self):
		#Only VFS specific case is listing /
		dirs = self.vfs.list("/")
		self.assertEquals(1, len(dirs))
		self.assertEquals("d/TestPlugin", dirs[0])
		
		#Check it calls the plugin's list
		self.vfs.list("/TestPlugin/dir1")
		self.assertEquals(1, self.plugin.listPaths["/TestPlugin/dir1"])
		
	##
	# Tests put
	def test_put(self):
		with self.assertRaises(ValueError):
			self.vfs.put("ASDASDAS", "NotLoadedPlugin")
			
		self.vfs.put("ASDAS", "TestPlugin")
		self.assertEquals("ASDAS", self.plugin.putItem)
		
	##
	# Tests search
	def test_search(self):
		with self.assertRaises(ValueError):
			self.vfs.search(None)
		with self.assertRaises(ValueError):
			self.vfs.search({})
		
		results = self.vfs.search({"genre": "testData"})
		self.assertEquals(1, len(results))
		self.assertEquals("FOUNDIT", results[0])
	
	##
	# Tests Loading and unloading of data sources
	def test_loadUnload(self):
		#Test unloading our default plugin
		self.vfs.unloadDataSource("TestPlugin")
		self.assertEquals(0, len(self.vfs.dataSources))
		#Test loading a random object
		with self.assertRaises(ValueError):
			self.vfs.loadDataSource("I'm not a plugin!")
		#Test loading our old plugin
		self.vfs.loadDataSource(self.plugin)
		self.assertEquals(1, len(self.vfs.dataSources))
		self.assertEquals(self.plugin, self.vfs.dataSources["TestPlugin"])
		#Load one more plugin
		p = testPlugin()
		p.name = "TotallyDifferentPlugin"
		p.tree = Entry("/"+p.name, "object.container.storageFolder", OneServerManager().rootEntry, [], p.name, "", -1, None)
		self.vfs.loadDataSource(p)
		self.assertEquals(2, len(self.vfs.dataSources))
		self.assertEquals(p, self.vfs.dataSources["TotallyDifferentPlugin"])
		
		
class testPlugin(IStoragePlugin):
	
	Name = "TestPlugin"
	
	files = {"file1": Entry("/file1", "" , None, None, None, "", 123, None),
			 "file2": Entry("/file1", "" , None, None, None, "", 123, None)
			}
	dirs  = {"dir1": None,
			 "dir2": ("test","test2", "test3")
			}
			
	def __init__(self):
		super(testPlugin, self).__init__('TestPlugin')
		self.name = "TestPlugin"
		self.tree = Entry("/"+self.name, "object.container.storageFolder", OneServerManager().rootEntry, [], self.name, "", -1, None)
		self.getPaths = defaultdict(int)
		self.listPaths = defaultdict(int)
		
	def get(self,path):
		tokens = path.split('/')
		if tokens[2] in self.files:
			self.getPaths[path] = self.getPaths[path] + 1
			return self.files[tokens[2]]
		elif tokens[2] in self.dirs:
			raise DirectoryError("No dir file")
		else:
			raise EntryNotFoundError("Not here " + path)
			
	def list(self,path):
		self.listPaths[path] += 1
		return "Empty"
		
	def put(self, entry):
		self.putItem = entry
		
	def search(self, metadata):
		return ("FOUNDIT",)
		
		
if __name__ is "__main__":
	unittest.main()
