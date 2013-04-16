from wrappers.upnp.upnp import close_prototype,get_info_prototype,read_prototype,seek_prototype,open_prototype,write_prototype
from wrappers.upnp.upnp import UPnP,Upnp_Action_Request,Upnp_DescType_e,Upnp_EventType_e,Upnp_FunPtr,UpnpDevice_Handle,UpnpOpenFileMode,UpnpVirtualDirCallbacks
from wrappers.upnp.upnp import UPNP_E_SUCCESS,UPNP_SOAP_E_INVALID_ACTION
from wrappers.upnp.ixml import ixmlCloneDOMString
from ctypes import cast,create_string_buffer,memmove,pointer,POINTER
from wrappers.libDLNA import DLNAInterface
from services.service import Service
from services.cms import CMSService
from services.cds import CDSService
from services.msr import MSRService
from metadata import WebFile
from manager import OneServerManager
import os
import uuid

##
# Provides an interface for working with the UPnP and DLNA libraries.
class DLNAService:
	##
	# The dictionary of all the open web file handles. It maps ID's to handles.
	fileHandles = dict()

	##
	# The dictionary of services. It maps service names to service objects.
	services = dict()

	##
	# Constructs the DLNA service interface based on the configuration file.
	#
	# @param config The configuration file details.
	def __init__(self, config):
		if config is None:
			raise ValueError("No ConfigManager was given!")
		
		self.config = config

		self.upnp = UPnP()
		self.idlna = DLNAInterface()
		self.dlnaDescription = None
		
		self.dlna = self.idlna.dlna_init()
		self.idlna.dlna_set_verbosity(self.dlna, 1)
		self.idlna.dlna_set_extension_check(self.dlna, 1)
		self.idlna.dlna_register_all_media_profiles(self.dlna)
		
		self.rootDev = UpnpDevice_Handle()
		
		self.manager         = OneServerManager()
		self.manager.idlna   = self.idlna
		self.manager.dlna    = self.dlna
		self.manager.webRoot = '/web/'
		self.manager.hostIp  = config.getCoreConfigWithDefault('ip', None)
		self.manager.port    = config.getCoreConfigWithDefault('port', 0)
		self.manager.log.debug("hostIp=%s, port=%s" % (self.manager.hostIp, self.manager.port))
		
		self.vdc = VirtualDirCallbackHandler(self.manager)
		self.virtualDirCallback			 = UpnpVirtualDirCallbacks()
		self.virtualDirCallback.get_info = get_info_prototype(self.vdc.httpGetInfo)
		self.virtualDirCallback.open	 = open_prototype(self.vdc.httpOpen)
		self.virtualDirCallback.read	 = read_prototype(self.vdc.httpRead)
		self.virtualDirCallback.write	 = write_prototype(self.vdc.httpWrite)
		self.virtualDirCallback.seek	 = seek_prototype(self.vdc.httpSeek)
		self.virtualDirCallback.close	 = close_prototype(self.vdc.httpClose)

		cds = CDSService()
		DLNAService.services[0] = {"id_t"   : cds.id_t, 
					   "type_t" : cds.type_t,
					   "actions": cds.actions}

		cms = CMSService()
		DLNAService.services[1] = {"id_t"   : cms.id_t,
					   "type_t" : cms.type_t,
					   "actions": cms.actions}

		msr = MSRService()
		DLNAService.services[2] = {"id_t"   : msr.id_t,
					   "type_t" : msr.type_t,
					   "actions":msr.actions}

	##
	# Starts the service.
	def start(self):
		# Setup and configure UPnP.
		result = self.upnp.UpnpInit(self.manager.hostIp, self.manager.port)
		if result != UPNP_E_SUCCESS:
			self.manager.log.error('An error occured when starting UPnP. Error code: {0}'.format(result))
			raise RuntimeError('An error occured when starting UPnP. Error code: {0}'.format(result))

		self.manager.hostIp = self.upnp.UpnpGetServerIpAddress()
		self.manager.port = self.upnp.UpnpGetServerPort()
		
		self.upnp.UpnpSetMaxContentLength(4096)

		"""
		self.dlnaDescription = self.idlna.dlna_dms_description_get('OneServer',
									   'OneServer Team',
									   'https://msoe.fogbugz.com',
									   'OneServer DLNA Media Server',
									   'OneServer',
									   'OneServer-01',
									   'https://msoe.fogbugz.com',
									   'OneServer-01',
									   'abeede57-f7f7-4e96-86bd-33b621625903',
									   self.manager.webRoot + 'oneserver.html',
									   self.manager.webRoot + CMSService.CMS_LOCATION,
									   self.manager.webRoot + 'cms_control',
									   self.manager.webRoot + 'cms_event',
									   self.manager.webRoot + CDSService.CDS_LOCATION,
									   self.manager.webRoot + 'cds_control',
									   self.manager.webRoot + 'cds_event')
"""
		self.dlnaDescription = self.getDlnaDescription('OneServer',
								'OneServer Team',
								'https://msoe.fogbugz.com',
								'OneServer DLNA Media Server',
								'OneServer',
								'OneServer-01',
								'https://msoe.fogbugz.com',
								'OneServer-01',
								'abeede57-f7f7-4e96-86bd-33b621625903',
								self.manager.webRoot + 'oneserver.html',
								self.manager.webRoot + CMSService.CMS_LOCATION,
								self.manager.webRoot + 'cms_control',
								self.manager.webRoot + 'cms_event',
								self.manager.webRoot + CDSService.CDS_LOCATION,
								self.manager.webRoot + 'cds_control',
								self.manager.webRoot + 'cds_event')

		# Start up UPnP
		self.upnp.UpnpEnableWebserver(True)
		self.upnp.UpnpSetVirtualDirCallbacks(self.virtualDirCallback)
		self.upnp.UpnpAddVirtualDir(self.manager.webRoot)
		self.devicehandler = Upnp_FunPtr(DLNAService.deviceEventHandler)
		result = self.upnp.UpnpRegisterRootDevice2(Upnp_DescType_e.UPNPREG_BUF_DESC,
							  self.dlnaDescription,
							  0, 1,
							  self.devicehandler,
							  None,
							  pointer(self.rootDev))

		if result != UPNP_E_SUCCESS:
			self.manager.log.error('An error occured when starting UPnP. Error code: {0}'.format(result))
			raise RuntimeError('An error occured when starting UPnP. Error code: {0}'.format(result))

		self.upnp.UpnpSendAdvertisement(self.rootDev, 1800)

	##
	# Stops the service.
	def stop(self):
		self.upnp.UpnpUnRegisterRootDevice(self.rootDev)

		self.upnp.UpnpRemoveAllVirtualDirs()
		self.upnp.UpnpEnableWebserver(False)

		self.idlna.dlna_uninit(self.dlna)
		self.dlna = None

		self.upnp.UpnpFinish()

	##
	# Handles device callbacks for the server
	@staticmethod
	def deviceEventHandler(eventType, event, cookie):
		if eventType == Upnp_EventType_e.UPNP_CONTROL_ACTION_REQUEST:
			DLNAService.handleActionRequest(cast(event, POINTER(Upnp_Action_Request)).contents)
		else:
			pass
		
		OneServerManager().log.debug("Ending device event handler")
		return UPNP_E_SUCCESS
	
	##
	# Handles action requests
	@staticmethod
	def handleActionRequest(request):
		if request.ErrCode != UPNP_E_SUCCESS:
			return

		#TODO: Check DevUDN
		manager = OneServerManager()
		manager.log.debug("DevUDN=%s, ServiceID=%s" % (request.DevUDN, request.ServiceID))
		action,service = DLNAService.findServiceAction(request)

		if service is not None and action is not None:
			event = dict()
			event['request'] = request
			event['status']  = True
			event['service'] = service

			manager.log.debug("Lauching action %s" % action)
			if action(event) and event['status']:
				request.ErrCode = UPNP_E_SUCCESS
			return

		if service is not None: #Invalid service action
			request.ErrStr = "Unknown Service Action"
		else:
			request.ErrStr = "Unknown Service ID"

		request.ActionResult = None
		request.ErrCode = UPNP_SOAP_E_INVALID_ACTION

	##
	# Finds the service and action for the request
	@staticmethod
	def findServiceAction(request):
		service = None
		action  = None

		if request is None and request.ActionName.isEmpty():
			return None,None

		for s in DLNAService.services:
			service = DLNAService.services[s]
			if service['id_t'] == request.ServiceID:
				for a in service['actions'].keys():
					if a == request.ActionName:
						action = (service['actions'])[a]
						return action,service
				return None,None
		return None,None

	@staticmethod
	def getDlnaDescription(fname, manufacturer, manufacturer_url, mdescription, mname, mnumber, murl, serial, uuid, presentationUrl, cmsScpd, cmsControl, cmsEvent, cdsScpd, cdsControl, cdsEvent):
		descriptionFmtStr = """
<?xml version="1.0"?>
<root xmlns="urn:schemas-upnp-org:device-1-0" >
	<specVersion>
		<major>1</major>
		<minor>0</minor>
	</specVersion>
	<device>
		<deviceType>urn:schemas-upnp-org:device:MediaServer:1</deviceType>
		<friendlyName>{0}</friendlyName>
		<manufacturer>{1}</manufacturer>
		<manufacturerURL>{2}</manufacturerURL>
		<modelDescription>{3}</modelDescription>
		<modelName>{4}</modelName>
		<modelNumber>{5}</modelNumber>
		<modelURL>{6}</modelURL>
		<serialNumber>{7}</serialNumber>
		<UDN>{8}</UDN>
		<presentationURL>{9}</presentationURL>
		<dlna:X_DLNADOC xmlns:dlna="urn:schemas-dlna-org:device-1-0">DMS-1.00</dlna:X_DLNADOC>
		<serviceList>
			<service>
				<serviceType>urn:schemas-upnp-org:service:ConnectionManager:1</serviceType>
				<serviceId>urn:upnp-org:serviceId:ConnectionManager</serviceId>
				<SCPDURL>{10}</SCPDURL>
				<controlURL>{11}</controlURL>
				<eventSubURL>{12}</eventSubURL>
			</service>
			<service>
				<serviceType>urn:schemas-upnp-org:service:ContentDirectory:1</serviceType>
				<serviceId>urn:upnp-org:serviceId:ContentDirectory</serviceId>
				<SCPDURL>{13}</SCPDURL>
				<controlURL>{14}</controlURL>
				<eventSubURL>{15}</eventSubURL>
			</service>
		</serviceList>
	</device>
</root>
"""
		return descriptionFmtStr.format(fname, manufacturer, manufacturer_url, mdescription, mname, mnumber, murl, serial, uuid, presentationUrl, cmsScpd, cmsControl, cmsEvent, cdsScpd, cdsControl, cdsEvent)

##
# Handles the Virtual Directory Callbacks
class VirtualDirCallbackHandler():
	##
	# Creates a new virtual directory callback handler with the given
	# manager instance.
	#
	# @param manager - an instance of the OneServerManager class
	def __init__(self, manager):
		self.manager = manager

	##
	# Sets the file information for the given file descriptor.
	# 
	# @param info - the file descriptor
	# @param length - the length of the file
	# @param contentType - the MIME type of the file
	def setInfoFile(self, info, length, contentType):
		info.contents.file_length = length
		info.contents.last_modified = 0
		info.contents.is_directory = 0
		info.contents.is_readable = 1
		info.contents.content_type = ixmlCloneDOMString(contentType)

	##
	# Handles any requests for file information.
	#
	# @param filename - the name of the file
	# @param fileInfo - the file descriptor
	#
	# @return 0 on success
	def httpGetInfo(self, filename, fileInfo):
		self.manager.log.debug('httpGetInfo: ' + filename)

		if not filename or not fileInfo:
			return -1

		# We need to remove the web handle part of the filename. So for example the
		# filename that was passed in could be '/web/cds.xml'. We need to make that
		# be just 'cds.xml'. If the file that was requested is '/web/movies/awesome.mp4'
		# this should be made into 'movies/awesome.mp4'.
		filename = filename.lstrip(self.manager.webRoot)

		if filename == CDSService.CDS_LOCATION:
			self.setInfoFile(fileInfo, len(CDSService.CDS_DESCRIPTION), 'text/xml')
			return 0

		if filename == CMSService.CMS_LOCATION:
			self.setInfoFile(fileInfo, len(CMSService.CMS_DESCRIPTION), 'text/xml')
			return 0

		if filename == MSRService.MSR_LOCATION:
			self.setInfoFile(fileInfo, len(MSRService.MSR_DESCRIPTION), 'text/xml')
			return 0

		upnpID = int(filename[filename.rfind('/') + 1:filename.rfind('.')])
		self.manager.log.debug('GetInfo for ' + str(upnpID))
		
		entry = self.manager.rootEntry.getChild(upnpID)
		if not entry:
			return -1

		if not entry.fullPath:
			return -1

		fileInfo.contents.is_readable = 1;
		fileInfo.contents.file_length = entry.size
		fileInfo.contents.last_modified = 1 #TODO: Modify entry to have a last_modified attribute
		fileInfo.contents.is_directory = 0 if entry.children is None else len(entry.children) + 1

		self.manager.log.debug("is_readable: {0}, file_length: {1}, last_modified {2}, is_directory {3}".format(fileInfo.contents.is_readable, fileInfo.contents.file_length, fileInfo.contents.last_modified, fileInfo.contents.is_directory))
		
		protocol = self.manager.idlna.dlna_write_protocol_info(
									 DLNAInterface.dlna_protocol_info_type_t['DLNA_PROTOCOL_INFO_TYPE_HTTP'],
									 DLNAInterface.dlna_org_play_speed_t['DLNA_ORG_PLAY_SPEED_NORMAL'],
									 DLNAInterface.dlna_org_conversion_t['DLNA_ORG_CONVERSION_NONE'],
									 DLNAInterface.dlna_org_operation_t['DLNA_ORG_OPERATION_RANGE'],
									 DLNAInterface.flags,
									 entry.dlnaProfile)


		content_type = protocol.split(':')[2]
		
		ct = ixmlCloneDOMString(content_type)
		self.manager.log.debug("Content Type :{0}".format(content_type))
		fileInfo.contents.content_type = ct
		return 0

	##
	# Handles requests for open a file handle for a specific file.
	#
	# @param filename - the name of the file
	# @param mode - the mode that the file should be opened in. Usually just read only
	#
	# @return a file handle to the file or None if the handle couldn't be created
	def httpOpen(self, filename, mode):
		self.manager.log.debug('httpOpen: ' + filename + ' ' + hex(mode))

		if not filename:
			self.manager.log.error('DLNA:HTTPOPEN:filename is None')
			return None

		if mode is not UpnpOpenFileMode.UPNP_READ:
			self.manager.log.error('DLNA:HTTPOPEN:mode is not UpnpOpenFileMode.upnp_read')
			return None

		# We need to remove the web handle part of the filename. So for example the
		# filename that was passed in could be '/web/cds.xml'. We need to make that
		# be just 'cds.xml'. If the file that was requested is '/web/movies/awesome.mp4'
		# this should be made into 'movies/awesome.mp4'.
		filename = filename.lstrip(self.manager.webRoot)

		_file = None

		if filename == CDSService.CDS_LOCATION:
			_file = Service.getFileMemory(self.manager.webRoot + CDSService.CDS_LOCATION,
							  CDSService.CDS_DESCRIPTION)
		elif filename == CMSService.CMS_LOCATION:
			_file = Service.getFileMemory(self.manager.webRoot + CMSService.CMS_LOCATION,
							  CMSService.CMS_DESCRIPTION)
		elif filename == MSRService.MSR_LOCATION:
			_file = Service.getFileMemory(self.manager.webRoot + MSRService.MSR_LOCATION,
							  MSRService.MSR_DESCRIPTION)
		else:
			upnpId = int( filename[filename.rfind('/') + 1:filename.rfind('.')])
			serverManager = OneServerManager()
			entry = serverManager.rootEntry.getChild(upnpId)
			if entry == None:
				self.manager.log.error('DLNA:HTTPOPEN:Entry is None')
				return None

			if entry.fullPath == None:
				self.manager.log.error('DLNA:HTTPOPEN:Entry.fullPath is None')
				return None

			fh = entry.generateFileHandle()
			_file = WebFile(entry.fullPath, 0, fh, entry)

		# Find a GUID for a handle and add it to the map.
		handle = uuid.uuid4().int >> 64
		DLNAService.fileHandles[handle] = _file

		return handle

	##
	# Reads some data from an open file.
	#
	# @param fh - the file handle
	# @param buf - the buffer to store data in
	# @param buflen - the length of the buffer
	#
	# @return the number of bytes that was read
	def httpRead(self, fh, buf, buflen):
		self.manager.log.debug('httpRead: ' + str(fh))

		if fh == None:
			self.manager.log.error('DLNA:HTTPREAD:fh is None')
			return -1
		
		_file = DLNAService.fileHandles[fh]
		if _file == None:
			self.manager.log.error('Invalid file handle.')
			return -1

		self.manager.log.debug('fileRead:' + str(_file.path))
		_len = -1
		

		temp = _file.fh.read(buflen)
		_len = len(temp)
		tempbuf = create_string_buffer(temp)
		memmove(buf,tempbuf,_len)

		if _len >= 0:
			_file.pos += _len
		return _len

	##
	# Handles attempts to write data to an open file.
	#
	# @param fh - the file handle
	# @param buf - the buffer to read data from
	# @param buflen - the length of the buffer
	#
	# @return 0 on success
	def httpWrite(self, fh, buf, buflen):
		self.manager.log.debug('httpWrite: ' + str(fh))

		# We are not implementint this functionality yet.

		return 0

	##
	# Handles requests to jump to a specific point in a file.
	#
	# @param fh - the file handle
	# @param offset - the offset in the file
	# @param origin - TODO
	#
	# @return 0 on success
	def httpSeek(self, fh, offset, origin):
		self.manager.log.debug('httpSeek: ' + str(fh))

		if fh == None:
			self.manager.log.debug('DLNA:HTTPSEEK:fh is None')
			return -1

		_file = DLNAService.fileHandles[fh]
		if _file == None:
			self.manager.log.debug('Invalid file handle.')
			return -1

		newpos = -1
		if origin is os.SEEK_SET:
			newpos = offset
		elif origin is os.SEEK_CUR:
			newpos = _file.pos + offset
		elif origin is os.SEEK_END:
			try:
				filesize = os.fstat(_file.fh.fileno()).st_size
				newpos = filesize + offset
			except os.error as e:
				self.manager.log.exception(e)
				return -1

		if newpos < 0:
			return -1
		
		if origin is os.SEEK_SET:
			_file.fh.seek(offset, os.SEEK_SET)
		elif origin is os.SEEK_CUR:
			_file.fh.seek(offset, os.SEEK_CUR)
		elif origin is os.SEEK_END:
			_file.fh.seek(offset, os.SEEK_END)
		_file.pos = _file.fh.tell() #Update using the real new position
		
		if newpos != _file.pos:
			self.manager.log.error("DLNA:HTTPSEEK:Nonequal positions" + _file.pos + " " + newpos)
		return 0
	
	##
	# Handles requests to close an open file.
	#
	# @param fh - the open file handle
	#
	# @return 0 on success
	def httpClose(self, fh):
		self.manager.log.debug('httpClose: ' + str(fh))

		if fh == None:
			self.manager.log.error('httpClose: fh is None')
			return -1

		_file = DLNAService.fileHandles[fh]
		if _file == None:
			self.manager.log.error('Invalid file handle.')
			return -1
		
		_file.fh.close()
		return 0

