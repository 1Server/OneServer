

from wrappers.libDLNA import DLNAInterface
from manager import OneServerManager

##
# A MIME type is a content type.
class MIMEType:
	##
	# Creates a new mime type.
	def __init__(self, extension, mime_class, mime_protocol):
		if(extension is None or mime_class is None or mime_protocol is None):
			raise TypeError("All arguments must not be None")
		self.extension = extension
		self.mime_class = mime_class
		self.mime_protocol = mime_protocol

UPNP_VIDEO    = 'object.item.videoItem'
UPNP_AUDIO    = 'object.item.audioItem.musicTrack'
UPNP_PHOTO    = 'object.item.imageItem.photo'
UPNP_PLAYLIST = 'object.item.playlistItem'
UPNP_TEXT     = 'object.item.textItem'

##
# All the supported MIME types.
mimeTypeList = [
	MIMEType('asf',   UPNP_VIDEO, 'http-get:*:video/x-ms-asf:'),
	MIMEType('avc',   UPNP_VIDEO, 'http-get:*:video/avi:'),
	MIMEType('avi',   UPNP_VIDEO, 'http-get:*:video/avi:'),
	MIMEType('dv',    UPNP_VIDEO, 'http-get:*:video/x-dv:'),
	MIMEType('divx',  UPNP_VIDEO, 'http-get:*:video/avi:'),
	MIMEType('wmv',   UPNP_VIDEO, 'http-get:*:video/x-ms-wmv:'),
	MIMEType('mjpg',  UPNP_VIDEO, 'http-get:*:video/x-motion-jpeg:'),
	MIMEType('mjpeg', UPNP_VIDEO, 'http-get:*:video/x-motion-jpeg:'),
	MIMEType('mpeg',  UPNP_VIDEO, 'http-get:*:video/mpeg:'),
	MIMEType('mpg',   UPNP_VIDEO, 'http-get:*:video/mpeg:'),
	MIMEType('mpe',   UPNP_VIDEO, 'http-get:*:video/mpeg:'),
	MIMEType('mp2p',  UPNP_VIDEO, 'http-get:*:video/mp2p:'),
	MIMEType('vob',   UPNP_VIDEO, 'http-get:*:video/mp2p:'),
	MIMEType('mp2t',  UPNP_VIDEO, 'http-get:*:video/mp2t:'),
	MIMEType('m1v',   UPNP_VIDEO, 'http-get:*:video/mpeg:'),
	MIMEType('m2v',   UPNP_VIDEO, 'http-get:*:video/mpeg2:'),
	MIMEType('mpg2',  UPNP_VIDEO, 'http-get:*:video/mpeg2:'),
	MIMEType('mpeg2', UPNP_VIDEO, 'http-get:*:video/mpeg2:'),
	MIMEType('m4v',   UPNP_VIDEO, 'http-get:*:video/mp4:'),
	MIMEType('m4p',   UPNP_VIDEO, 'http-get:*:video/mp4:'),
	MIMEType('mp4ps', UPNP_VIDEO, 'http-get:*:video/x-nerodigital-ps:'),
	MIMEType('ts',    UPNP_VIDEO, 'http-get:*:video/mpeg2:'),
	MIMEType('ogm',   UPNP_VIDEO, 'http-get:*:video/mpeg:'),
	MIMEType('mkv',   UPNP_VIDEO, 'http-get:*:video/mpeg:'),
	MIMEType('rmvb',  UPNP_VIDEO, 'http-get:*:video/mpeg:'),
	MIMEType('mov',   UPNP_VIDEO, 'http-get:*:video/quicktime:'),
	MIMEType('hdmov', UPNP_VIDEO, 'http-get:*:video/quicktime:'),
	MIMEType('qt',    UPNP_VIDEO, 'http-get:*:video/quicktime:'),
	MIMEType('bin',   UPNP_VIDEO, 'http-get:*:video/mpeg2:'),
	MIMEType('iso',   UPNP_VIDEO, 'http-get:*:video/mpeg2:'),
	MIMEType('3gp',  UPNP_AUDIO, 'http-get:*:audio/3gpp:'),
	MIMEType('aac',  UPNP_AUDIO, 'http-get:*:audio/x-aac:'),
	MIMEType('ac3',  UPNP_AUDIO, 'http-get:*:audio/x-ac3:'),
	MIMEType('aif',  UPNP_AUDIO, 'http-get:*:audio/aiff:'),
	MIMEType('aiff', UPNP_AUDIO, 'http-get:*:audio/aiff:'),
	MIMEType('at3p', UPNP_AUDIO, 'http-get:*:audio/x-atrac3:'),
	MIMEType('au',   UPNP_AUDIO, 'http-get:*:audio/basic:'),
	MIMEType('snd',  UPNP_AUDIO, 'http-get:*:audio/basic:'),
	MIMEType('dts',  UPNP_AUDIO, 'http-get:*:audio/x-dts:'),
	MIMEType('rmi',  UPNP_AUDIO, 'http-get:*:audio/midi:'),
	MIMEType('mid',  UPNP_AUDIO, 'http-get:*:audio/midi:'),
	MIMEType('mp1',  UPNP_AUDIO, 'http-get:*:audio/mp1:'),
	MIMEType('mp2',  UPNP_AUDIO, 'http-get:*:audio/mp2:'),
	MIMEType('mp3',  UPNP_AUDIO, 'http-get:*:audio/mpeg:'),
	MIMEType('mp4',  UPNP_AUDIO, 'http-get:*:audio/mp4:'),
	MIMEType('m4a',  UPNP_AUDIO, 'http-get:*:audio/mp4:'),
	MIMEType('ogg',  UPNP_AUDIO, 'http-get:*:audio/x-ogg:'),
	MIMEType('wav',  UPNP_AUDIO, 'http-get:*:audio/wav:'),
	MIMEType('pcm',  UPNP_AUDIO, 'http-get:*:audio/l16:'),
	MIMEType('lpcm', UPNP_AUDIO, 'http-get:*:audio/l16:'),
	MIMEType('l16',  UPNP_AUDIO, 'http-get:*:audio/l16:'),
	MIMEType('wma',  UPNP_AUDIO, 'http-get:*:audio/x-ms-wma:'),
	MIMEType('mka',  UPNP_AUDIO, 'http-get:*:audio/mpeg:'),
	MIMEType('ra',   UPNP_AUDIO, 'http-get:*:audio/x-pn-realaudio:'),
	MIMEType('rm',   UPNP_AUDIO, 'http-get:*:audio/x-pn-realaudio:'),
	MIMEType('ram',  UPNP_AUDIO, 'http-get:*:audio/x-pn-realaudio:'),
	MIMEType('flac', UPNP_AUDIO, 'http-get:*:audio/x-flac:'),
	MIMEType('bmp',  UPNP_PHOTO, 'http-get:*:image/bmp:'),
	MIMEType('ico',  UPNP_PHOTO, 'http-get:*:image/x-icon:'),
	MIMEType('gif',  UPNP_PHOTO, 'http-get:*:image/gif:'),
	MIMEType('jpeg', UPNP_PHOTO, 'http-get:*:image/jpeg:'),
	MIMEType('jpg',  UPNP_PHOTO, 'http-get:*:image/jpeg:'),
	MIMEType('jpe',  UPNP_PHOTO, 'http-get:*:image/jpeg:'),
	MIMEType('pcd',  UPNP_PHOTO, 'http-get:*:image/x-ms-bmp:'),
	MIMEType('png',  UPNP_PHOTO, 'http-get:*:image/png:'),
	MIMEType('pnm',  UPNP_PHOTO, 'http-get:*:image/x-portable-anymap:'),
	MIMEType('ppm',  UPNP_PHOTO, 'http-get:*:image/x-portable-pixmap:'),
	MIMEType('qti',  UPNP_PHOTO, 'http-get:*:image/x-quicktime:'),
	MIMEType('qtf',  UPNP_PHOTO, 'http-get:*:image/x-quicktime:'),
	MIMEType('qtif', UPNP_PHOTO, 'http-get:*:image/x-quicktime:'),
	MIMEType('tif',  UPNP_PHOTO, 'http-get:*:image/tiff:'),
	MIMEType('tiff', UPNP_PHOTO, 'http-get:*:image/tiff:'),
	MIMEType('pls', UPNP_PLAYLIST, 'http-get:*:audio/x-scpls:'),
	MIMEType('m3u', UPNP_PLAYLIST, 'http-get:*:audio/mpegurl:'),
	MIMEType('asx', UPNP_PLAYLIST, 'http-get:*:video/x-ms-asf:'),
	MIMEType('srt', UPNP_TEXT, 'http-get:*:text/srt:'),
	MIMEType('ssa', UPNP_TEXT, 'http-get:*:text/ssa:'),
	MIMEType('stl', UPNP_TEXT, 'http-get:*:text/srt:'),
	MIMEType('psb', UPNP_TEXT, 'http-get:*:text/psb:'),
	MIMEType('pjs', UPNP_TEXT, 'http-get:*:text/pjs:'),
	MIMEType('sub', UPNP_TEXT, 'http-get:*:text/sub:'),
	MIMEType('idx', UPNP_TEXT, 'http-get:*:text/idx:'),
	MIMEType('dks', UPNP_TEXT, 'http-get:*:text/dks:'),
	MIMEType('scr', UPNP_TEXT, 'http-get:*:text/scr:'),
	MIMEType('tts', UPNP_TEXT, 'http-get:*:text/tts:'),
	MIMEType('vsf', UPNP_TEXT, 'http-get:*:text/vsf:'),
	MIMEType('zeg', UPNP_TEXT, 'http-get:*:text/zeg:'),
	MIMEType('mpl', UPNP_TEXT, 'http-get:*:text/mpl:'),
	MIMEType('bup', UPNP_TEXT, 'http-get:*:text/bup:'),
	MIMEType('ifo', UPNP_TEXT, 'http-get:*:text/ifo:')
]

##
# Gets the extension for the filename.
#
# @param filename the name of the file
#
# @return a string with the file extension
def getExtension(filename):
	return filename[filename.rfind('.') + 1:]

##
# Gets the MIME type for the extension.
#
# @param extension the extension of the file type
#
# @return a mime type object or None
def getMIMEType(extension):
	if not extension:
		return None

	for mime in mimeTypeList:
		if mime.extension.lower() == extension.lower():
			return mime

	return None

##
# Checks if the extension is a valid DLNA extension.
#
# @param filename the name of the file
#
# @return checks if the file is a supported DLNA type.
def isValidExtension(filename):
	if not filename:
		return False

	return DLNAInterface().dlna_guess_media_profile(OneServerManager().dlna, filename)

##
# Represents a file
class WebFile(object):
	##
	# fh is a python filehandle
	def __init__(self, path, pos, fh, entry):
		self.path  = path
		self.pos   = pos
		self.fh    = fh
		self.entry = entry

