import unittest


from oneserver import metadata
from manager import OneServerManager
from wrappers.libDLNA import DLNAInterface

##
# Tests the MIMEType Class of the Metadata python file
class TestMIMEType(unittest.TestCase):

	def setUp(self):
		pass
		
	def test_MIMETypeCreation(self):
		with self.assertRaises(TypeError):
			metadata.MIMEType()
		with self.assertRaises(TypeError):
			metadata.MIMEType(None)
		with self.assertRaises(TypeError):
			metadata.MIMEType(None,None)
		with self.assertRaises(TypeError):
			metadata.MIMEType(None,None,None)

class TestMetadata(unittest.TestCase):

	def setUp(self):
		pass

	def test_getExtension(self):
		self.assertEquals('asf', metadata.getExtension('test.asf'))
		self.assertEquals('mp4', metadata.getExtension('test.mp4'))
		self.assertEquals('mov', metadata.getExtension('test.mov'))
		
		
	def test_getMIMEType(self):
		mimemp4 = metadata.MIMEType('mp4', 'object.item.audioItem.musicTrack', 'http-get:*:audio/mp4:')
		self.assertEquals(mimemp4.extension, metadata.getMIMEType('mp4').extension)
		self.assertEquals(mimemp4.mime_class, metadata.getMIMEType('mp4').mime_class)
		self.assertEquals(mimemp4.mime_protocol, metadata.getMIMEType('mp4').mime_protocol)
		mimemov = metadata.MIMEType('mov', 'object.item.videoItem', 'http-get:*:video/quicktime:')
		self.assertEquals(mimemov.extension, metadata.getMIMEType('mov').extension)
		self.assertEquals(mimemov.mime_class, metadata.getMIMEType('mov').mime_class)
		self.assertEquals(mimemov.mime_protocol, metadata.getMIMEType('mov').mime_protocol)
		
if __name__ == '__main__':
	unittest.main()
