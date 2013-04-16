from service import Service
from manager import OneServerManager
from wrappers import libDLNA
from wrappers.libDLNA import DLNAInterface
from xml.dom.minidom import parseString

##
# Handles the ContentDirectory service for the UPNP handler
class CDSService(Service):

	CDS_DESCRIPTION = """<?xml version="1.0" encoding="utf-8"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
	<specVersion>
		<major>1</major>
		<minor>0</minor>
	</specVersion>
	<actionList>
		<action>
			<name>Browse</name>
			<argumentList>
				<argument>
					<name>ObjectID</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_ObjectID</relatedStateVariable>
				</argument>
				<argument>
					<name>BrowseFlag</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_BrowseFlag</relatedStateVariable>
				</argument>
				<argument>
					<name>Filter</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_Filter</relatedStateVariable>
				</argument>
				<argument>
					<name>StartingIndex</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_Index</relatedStateVariable>
				</argument>
				<argument>
					<name>RequestedCount</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable>
				</argument>
				<argument>
					<name>SortCriteria</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_SortCriteria</relatedStateVariable>
				</argument>
				<argument>
					<name>Result</name>
					<direction>out</direction>
					<relatedStateVariable>A_ARG_TYPE_Result</relatedStateVariable>
				</argument>
				<argument>
					<name>NumberReturned</name>
					<direction>out</direction>
					<relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable>
				</argument>
				<argument>
					<name>TotalMatches</name>
					<direction>out</direction>
					<relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable>
				</argument>
				<argument>
					<name>UpdateID</name>
					<direction>out</direction>
					<relatedStateVariable>A_ARG_TYPE_UpdateID</relatedStateVariable>
				</argument>
			</argumentList>
		</action>
		<action>
			<name>DestroyObject</name>
			<argumentList>
				<argument>
					<name>ObjectID</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_ObjectID</relatedStateVariable>
				</argument>
			</argumentList>
		</action>
		<action>
			<name>CreateObject</name>
			<argumentList>
				<argument>
					<name>ContainerID</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_ObjectID</relatedStateVariable>
				</argument>
				<argument>
					<name>Elements</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_Result</relatedStateVariable>
				</argument>
				<argument>
					<name>ObjectID</name>
					<direction>out</direction>
					<relatedStateVariable>A_ARG_TYPE_ObjectID</relatedStateVariable>
				</argument>
				<argument>
					<name>Result</name>
					<direction>out</direction>
					<relatedStateVariable>A_ARG_TYPE_Result</relatedStateVariable>
				</argument>
			</argumentList>
		</action>
		<action>
			<name>GetSystemUpdateID</name>
			<argumentList>
				<argument>
					<name>Id</name>
					<direction>out</direction>
					<relatedStateVariable>SystemUpdateID</relatedStateVariable>
				</argument>
			</argumentList>
		</action>
		<action>
			<name>GetSearchCapabilities</name>
			<argumentList>
				<argument>
					<name>SearchCaps</name>
					<direction>out</direction>
					<relatedStateVariable>SearchCapabilities</relatedStateVariable>
				</argument>
			</argumentList>
		</action>
		<action>
			<name>GetSortCapabilities</name>
			<argumentList>
				<argument>
					<name>SortCaps</name>
					<direction>out</direction>
					<relatedStateVariable>SortCapabilities</relatedStateVariable>
				</argument>
			</argumentList>
		</action>
		<action>
			<name>UpdateObject</name>
			<argumentList>
				<argument>
					<name>ObjectID</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_ObjectID</relatedStateVariable>
				</argument>
				<argument>
					<name>CurrentTagValue</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_TagValueList</relatedStateVariable>
				</argument>
				<argument>
					<name>NewTagValue</name>
					<direction>in</direction>
					<relatedStateVariable>A_ARG_TYPE_TagValueList</relatedStateVariable>
				</argument>
			</argumentList>
		</action>
	</actionList>
	<serviceStateTable>
		<stateVariable>
			<Optional/>
			<name>A_ARG_TYPE_URI</name>
			<sendEventsAttribute>no</sendEventsAttribute>
			<dataType>uri</dataType>
		</stateVariable>
		<stateVariable>
			<Optional/>
			<name>A_ARG_TYPE_TransferID</name>
			<sendEventsAttribute>no</sendEventsAttribute>
			<dataType>ui4</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_BrowseFlag</name>
			<dataType>string</dataType>
			<allowedValueList>
				<allowedValue>BrowseMetadata</allowedValue>
				<allowedValue>BrowseDirectChildren</allowedValue>
			</allowedValueList>
		</stateVariable>
		<stateVariable sendEvents="yes">
			<name>SystemUpdateID</name>
			<dataType>ui4</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_Count</name>
			<dataType>ui4</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_SortCriteria</name>
			<dataType>string</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>SortCapabilities</name>
			<dataType>string</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_Index</name>
			<dataType>ui4</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_ObjectID</name>
			<dataType>string</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_UpdateID</name>
			<dataType>ui4</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_TagValueList</name>
			<dataType>string</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_Result</name>
			<dataType>string</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>SearchCapabilities</name>
			<dataType>string</dataType>
		</stateVariable>
		<stateVariable sendEvents="no">
			<name>A_ARG_TYPE_Filter</name>
			<dataType>string</dataType>
		</stateVariable>
	</serviceStateTable>
</scpd>

"""

	CDS_LOCATION = "cds.xml"

	CDS_SERVICE_ID = "urn:upnp-org:serviceId:ContentDirectory"
	CDS_SERVICE_TYPE = "urn:schemas-upnp-org:service:ContentDirectory:1"

	# Represent the CDS GetSearchCapabilities action. 
	SERVICE_CDS_ACTION_SEARCH_CAPS = "GetSearchCapabilities"

	# Represent the CDS GetSortCapabilities action. 
	SERVICE_CDS_ACTION_SORT_CAPS = "GetSortCapabilities"

	# Represent the CDS GetSystemUpdateID action. 
	SERVICE_CDS_ACTION_UPDATE_ID = "GetSystemUpdateID"

	# Represent the CDS Browse action. 
	SERVICE_CDS_ACTION_BROWSE = "Browse"

	# Represent the CDS Search action. 
	SERVICE_CDS_ACTION_SEARCH = "Search"
	
	# Represents the CDS CreatObject action
	SERVICE_CDS_ACTION_CREATE_OBJECT = "CreateObject"

	# Represent the CDS SearchCaps argument. 
	SERVICE_CDS_ARG_SEARCH_CAPS = "SearchCaps"

	# Represent the CDS SortCaps argument. 
	SERVICE_CDS_ARG_SORT_CAPS = "SortCaps"

	# Represent the CDS UpdateId argument. 
	SERVICE_CDS_ARG_UPDATE_ID = "Id"

	# Represent the CDS StartingIndex argument. 
	SERVICE_CDS_ARG_START_INDEX = "StartingIndex"

	# Represent the CDS RequestedCount argument. 
	SERVICE_CDS_ARG_REQUEST_COUNT = "RequestedCount"

	# Represent the CDS ObjectID argument. 
	SERVICE_CDS_ARG_OBJECT_ID = "ObjectID"

	# Represent the CDS Filter argument. 
	SERVICE_CDS_ARG_FILTER = "Filter"

	# Represent the CDS BrowseFlag argument. 
	SERVICE_CDS_ARG_BROWSE_FLAG = "BrowseFlag"

	# Represent the CDS SortCriteria argument. 
	SERVICE_CDS_ARG_SORT_CRIT = "SortCriteria"

	# Represent the CDS SearchCriteria argument. 
	SERVICE_CDS_ARG_SEARCH_CRIT = "SearchCriteria"

	# Represent the CDS Root Object ID argument. 
	SERVICE_CDS_ROOT_OBJECT_ID = "0"

	# Represent the CDS DIDL Message Metadata Browse flag argument. 
	SERVICE_CDS_BROWSE_METADATA = "BrowseMetadata"

	# Represent the CDS DIDL Message DirectChildren Browse flag argument. 
	SERVICE_CDS_BROWSE_CHILDREN = "BrowseDirectChildren"

	# Represent the CDS DIDL Message Result argument. 
	SERVICE_CDS_DIDL_RESULT = "Result"

	# Represent the CDS DIDL Message NumberReturned argument. 
	SERVICE_CDS_DIDL_NUM_RETURNED = "NumberReturned"

	# Represent the CDS DIDL Message TotalMatches argument. 
	SERVICE_CDS_DIDL_TOTAL_MATCH = "TotalMatches"

	# Represent the CDS DIDL Message UpdateID argument. 
	SERVICE_CDS_DIDL_UPDATE_ID = "UpdateID"
	
	# Represent the CDS DIDL Message TransferID argument
	SERVICE_CDS_DIDL_TRANSFER_ID = "TransferID"

	# DIDL parameters 
	# Represent the CDS DIDL Message Header Namespace. 
	DIDL_NAMESPACE = """xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" """

	# Represent the CDS DIDL Message Header Tag. 
	DIDL_LITE = "DIDL-Lite"

	# Represent the CDS DIDL Message Item value. 
	DIDL_ITEM = "item"

	# Represent the CDS DIDL Message Item ID value. 
	DIDL_ITEM_ID = "id"

	# Represent the CDS DIDL Message Item Parent ID value. 
	DIDL_ITEM_PARENT_ID = "parentID"

	# Represent the CDS DIDL Message Item Restricted value. 
	DIDL_ITEM_RESTRICTED = "restricted"

	# Represent the CDS DIDL Message Item UPnP Class value. 
	DIDL_ITEM_CLASS = "upnp:class"

	# Represent the CDS DIDL Message Item Title value. 
	DIDL_ITEM_TITLE = "dc:title"

	# Represent the CDS DIDL Message Item Resource value. 
	DIDL_RES = "res"

	# Represent the CDS DIDL Message Item Protocol Info value. 
	DIDL_RES_INFO = "protocolInfo"
	
	# Represent the CDS DIDL Message Item Import URI value
	DIDL_RES_IMPORT_URI = "importUri"

	# Represent the CDS DIDL Message Item Resource Size value. 
	DIDL_RES_SIZE = "size"

	# Represent the CDS DIDL Message Container value. 
	DIDL_CONTAINER = "container"

	# Represent the CDS DIDL Message Container ID value. 
	DIDL_CONTAINER_ID = "id"

	# Represent the CDS DIDL Message Container Parent ID value. 
	DIDL_CONTAINER_PARENT_ID = "parentID"

	# Represent the CDS DIDL Message Container number of children value. 
	DIDL_CONTAINER_CHILDS = "childCount"

	# Represent the CDS DIDL Message Container Restricted value. 
	DIDL_CONTAINER_RESTRICTED = "restricted"

	# Represent the CDS DIDL Message Container Searchable value. 
	DIDL_CONTAINER_SEARCH = "searchable"

	# Represent the CDS DIDL Message Container UPnP Class value. 
	DIDL_CONTAINER_CLASS = "upnp:class"

	# Represent the CDS DIDL Message Container Title value. 
	DIDL_CONTAINER_TITLE = "dc:title"

	# Represent the = "upnp:class" reserved keyword for Search action 
	SEARCH_CLASS_MATCH_KEYWORD = "(upnp:class = \""

	# Represent the = "upnp:class derived from" reserved keyword 
	SEARCH_CLASS_DERIVED_KEYWORD = "(upnp:class derivedfrom \""

	# Represent the = "res@protocolInfo contains" reserved keyword 
	SEARCH_PROTOCOL_CONTAINS_KEYWORD = "(res@protocolInfo contains \""

	# Represent the Search default keyword 
	SEARCH_OBJECT_KEYWORD = "object"

	# Represent the Search 'AND' connector keyword 
	SEARCH_AND = ") and ("

	#The MIME type for a container
	CONTAINER_MIME = "object.container.storageFolder"

	##
	# Creates the CDS Service
	def __init__(self):
		self.id_t    = self.CDS_SERVICE_ID 
		self.type_t  = self.CDS_SERVICE_TYPE
		actions = dict()
		actions['GetSearchCapabilities'] = CDSService.getSearchCapabilities
		actions['GetSortCapabilities']   = CDSService.getSortCapabilities
		actions['GetSystemUpdateID']     = CDSService.getSystemUpdateId
		actions['Browse']				 = CDSService.browse
		actions['Search']				 = CDSService.search
		actions['CreateObject']			 = CDSService.createObject
		self.actions = actions

	##
	# Gets the search capabilities
	@staticmethod
	def getSearchCapabilities(event):
		manager = OneServerManager()
		manager.log.debug("getSearchCapabilities event=%s" % event)
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_ARG_SEARCH_CAPS, "")
		manager.log.debug("left addResponse")
		return event['status']

	##
	# Gets the sort capabilties
	@staticmethod
	def getSortCapabilities(event):
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_ARG_SORT_CAPS, "")
		return event['status']

	##
	# Gets the system update id
	@staticmethod
	def getSystemUpdateId(event):
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_ARG_UPDATE_ID, CDSService.SERVICE_CDS_ROOT_OBJECT_ID)
		return event['status']

	##
	# Browses for content.
	@staticmethod
	def browse(event):
		if not event:
			return False

		if not event['status']:
			return False

		metadata = False

		index         = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_START_INDEX)
		count         = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_REQUEST_COUNT)
		_id           = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_OBJECT_ID)
		flag          = Service.upnpGetString(event['request'], CDSService.SERVICE_CDS_ARG_BROWSE_FLAG)
		_filter       = Service.upnpGetString(event['request'], CDSService.SERVICE_CDS_ARG_FILTER)
		sort_criteria = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_SORT_CRIT)
		manager = OneServerManager()
		manager.log.debug("index=%s, count=%s, _id=%s, flag=%s, _filter=%s, sort_criteria=%s" % (index,count, _id, flag,_filter, sort_criteria))
		if not flag or not _filter:
			return False

		# Validation checking.
		if flag == CDSService.SERVICE_CDS_BROWSE_METADATA:
			if index != 0:
				return False

			metadata = True
		elif flag == CDSService.SERVICE_CDS_BROWSE_CHILDREN:
			metadata = False
		else:
			return False
		
		entry = manager.rootEntry.getChild(_id)

		if not entry and _id < 0:
			manager.error("Invalid id {0}, defaulting to root".format(_id))
			entry = manager.rootEntry

		if not entry:
			return False

		out = ""

		result_count = 0
		if metadata:
			result_count,out = CDSService.cdsBrowseMetadata(event, out, index, count, entry, _filter) 
		else:
			result_count,out = CDSService.cdsBrowseDirectChildren(event, out, index, count, entry, _filter)

		if result_count < 0:
			return False

		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_UPDATE_ID, CDSService.SERVICE_CDS_ROOT_OBJECT_ID)

		return event['status']

	##
	# Handles searches.
	@staticmethod
	def search(event):
		if not event:
			return False

		if not event['status']:
			return False

		index = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_START_INDEX)
		count = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_REQUEST_COUNT)
		_id = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_OBJECT_ID)
		search_criteria = Service.upnpGetString(event['request'], CDSService.SERVICE_CDS_ARG_SEARCH_CRIT)
		_filter = Service.upnpGetString(event['request'], CDSService.SERVICE_CDS_ARG_FILTER)
		sort_criteria = Service.upnpGetUI4(event['request'], CDSService.SERVICE_CDS_ARG_SORT_CRIT)

		if not search_criteria or not _filter:
			return False

		_core = OneServerManager()
		entry = _core.rootEntry.getChild(_id)

		if not entry and _id < 0:
			entry = _core.rootEntry

		if not entry:
			return False

		out = ""

		result_count,out = CDSService.cdsSearchDirectChildren(event, out, index, count, entry, _filter, search_criteria)

		if result_count < 0:
			return False

		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_UPDATE_ID)

		return event['status']
	
	##
	# Handles requests to create new files on the server.
	@staticmethod
	def createObject(event):
		if not event:
			return False

		if not event['status']:
			return False
				
		#Get args
		containerId = Service.upnpGetUI4(event['request'], "ContainerID")
		elements = Service.upnpGetString(event['request'], "Elements")
		elements = parseString(elements)
		
		#Get information out of elements
		item = elements.getElementsByTagName("item")[0]
		title = (item.getElementsByTagName("dc:title")[0]).childNodes
		mediaClass = (item.getElementsByTagName("upnp:class")[0]).childNodes
		
		#Create Entry Object
		entry = Entry("/upload/"+title, mediaClass, OneServerManager().uploadRoot, None, title, "", -1, None)
		
		#Create Response
		response = ""
		CDSService.didlAddHeader(response)
		CDSService.didlAddItem(response, entry._id, entry.parent._id, "false", entry.dlnaProfile, entry.title, "*:*:*:*", "0", entry.url, "")
		CDSService.didlAddFooter(response)
		
		Service.upnpAddResponse(event, CDSService.SERVICE_DIDL_RESULT, response)
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_ARG_OBJECT_ID, entry._id)
		
		return event["status"]

	##
	# Adds metadata for the entry to the response
	@staticmethod
	def addMetadata(entry,response):
		#TODO:
		return response
		
	##
	# Checks if the filter has the value
	@staticmethod
	def filterHasVal(_filter, val):
		if _filter is "*":
			return True
		
		if _filter is not None:
			tokens = _filter.split(",")
			if val in tokens:
				return True
		return False

	@staticmethod
	def didlAddHeader(buf):
		return buf + ("<{0} {1}>".format(CDSService.DIDL_LITE, CDSService.DIDL_NAMESPACE))

	@staticmethod
	def didlAddFooter(buf):
		return buf + ("</{0}>".format(CDSService.DIDL_LITE))

	@staticmethod
	def didlAddTag(buf, tag, value):
		if value is not None:
			buf = buf + ("<{0}>{1}</{0}>".format(tag,value))
		return buf

	@staticmethod
	def didlAddParam(buf,param,value):
		if value is not None:
			buf = buf + (" {0}=\"{1}\"".format(param,value))
		return buf
	
	@staticmethod
	def didlAddValue(buf,param,value):
		return buf + (" {0}=\"{1!s}\"".format(param,value))

	@staticmethod
	def didlAddItem(buf, itemId, parentId, restricted, _class, title, protocolInfo, size, url, _filter):
		buf = buf + ("<{0}".format(CDSService.DIDL_ITEM))
		buf = CDSService.didlAddValue(buf, CDSService.DIDL_ITEM_ID, itemId)
		buf = CDSService.didlAddValue(buf, CDSService.DIDL_ITEM_PARENT_ID, parentId)
		buf = CDSService.didlAddParam(buf, CDSService.DIDL_ITEM_RESTRICTED, restricted)
		buf = buf + (">")

		buf = CDSService.didlAddTag(buf, CDSService.DIDL_ITEM_CLASS, _class)
		buf = CDSService.didlAddTag(buf, CDSService.DIDL_ITEM_TITLE, title)

		if CDSService.filterHasVal(_filter, CDSService.DIDL_RES) :
			buf = buf + ("<{0}".format(CDSService.DIDL_RES))
			buf = CDSService.didlAddParam(buf, CDSService.DIDL_RES_INFO, protocolInfo)

			if CDSService.filterHasVal(_filter, "@{0}".format(CDSService.DIDL_RES_SIZE)):
				buf = CDSService.didlAddValue(buf, CDSService.DIDL_RES_SIZE, size)

			buf = buf + (">")

			if url is not None:
				_core = OneServerManager()
				buf = buf + ("http://{0}:{1!s}{2}{3}".format(_core.hostIp,
									    _core.port,
									    _core.webRoot,
									    url))
			buf = buf + ("</{0}>".format(CDSService.DIDL_RES))
		buf = buf + ("</{0}>".format(CDSService.DIDL_ITEM))
		return buf

	@staticmethod
	def didlAddContainer(buf, containerId, parentId, childCount, restricted, searchable, title, _class):
		buf = buf + ("<{0}".format(CDSService.DIDL_CONTAINER))
		
		buf = CDSService.didlAddValue(buf, CDSService.DIDL_CONTAINER_ID, containerId)
		buf = CDSService.didlAddValue(buf, CDSService.DIDL_CONTAINER_PARENT_ID, parentId)
		if childCount >=0:
			buf = CDSService.didlAddValue(buf, CDSService.DIDL_CONTAINER_CHILDS, childCount)
		buf = CDSService.didlAddParam(buf, CDSService.DIDL_CONTAINER_RESTRICTED, restricted)
		buf = CDSService.didlAddParam(buf, CDSService.DIDL_CONTAINER_SEARCH, searchable)
		
		buf = buf + (">")

		buf = CDSService.didlAddTag(buf, CDSService.DIDL_CONTAINER_CLASS, _class)
		buf = CDSService.didlAddTag(buf, CDSService.DIDL_CONTAINER_TITLE, title)

		buf = buf + ("</{0}>".format(CDSService.DIDL_CONTAINER))
		return buf

	##
	# Browsees the metadata
	# Returns a tuple of the number of results and buf with the metadata appended
	@staticmethod
	def cdsBrowseMetadata(event, buf, index, count, entry, _filter):
		if entry is None:
			return 0,buf
		
		resultCount = 0
		if entry.children is None: # File
			protocol = ""
			dlna = DLNAInterface()
			protocol = dlna.dlna_write_protocol_info(dlna.dlna_protocol_info_type_t['DLNA_PROTOCOL_INFO_TYPE_HTTP'],
							    dlna.dlna_org_play_speed_t['DLNA_ORG_PLAY_SPEED_NORMAL'],
							    dlna.dlna_org_conversion_t['DLNA_ORG_CONVERSION_NONE'],
							    dlna.dlna_org_operation_t['DLNA_ORG_OPERATION_RANGE'],
							    dlna.flags,
							    entry.dlnaProfile)
			
			buf = CDSService.didlAddHeader(buf)
			
			buf = CDSService.didlAddItem(buf,
					  entry._id,
					  entry.parent._id if entry.parent is not None else -1,
					  "false",
					  dlna.dlna_profile_upnp_object_item(entry.dlnaProfile),
					  entry.title,
					  protocol,
					  entry.size,
					  entry.url,
					  _filter)
			
			buf = CDSService.didlAddFooter(buf)
			for a in range(index, min(index+count, -1)):
					resultCount += 1

		else: #Directory
			buf = CDSService.didlAddHeader(buf)
			buf = CDSService.didlAddContainer(buf,
					       entry._id,
					       entry.parent._id if entry.parent is not None else -1,
					       len(entry.children),
					       "true",
					       "true",
					       entry.title,
					       CDSService.CONTAINER_MIME)
			buf = CDSService.didlAddFooter(buf)

			resultCount = 1

		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_RESULT, buf)
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_NUM_RETURNED, "1")
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_TOTAL_MATCH, "1")

		return resultCount,buf

	##
	# Pulls information on the direct children
	# Returns of tuple of the result count and the information appended to buf
	@staticmethod
	def cdsBrowseDirectChildren(event, buf, index, count, entry, _filter):
		resultCount = 0
		if entry.children is None: #Its a file
			return -1,buf

		buf = CDSService.didlAddHeader(buf)

		#If index = 0 and count = 0 then all children must be returned
		if (index is 0) and (count is 0):
			count = len(entry.children)
		
		for child in entry.children:
			if (count is 0) or (resultCount < count):
				if child.children is not None: #Container
					buf = CDSService.didlAddContainer(buf, child._id,
							       child.parent._id if child.parent is not None else -1,
							       len(child.children), "true", None,
							       child.title,
							       CDSService.CONTAINER_MIME)
				else: #Item 
					manager = OneServerManager()
					manager.log.debug("child=%s, child.children=%s" % (child,child.children))
					manager.log.debug("child.fullpath=%s" % child.fullPath)
					manager.log.debug("child.dlnaProfile=%s" % child.dlnaProfile.contents.mime)
					dlna = DLNAInterface()
					protocol = dlna.dlna_write_protocol_info(dlna.dlna_protocol_info_type_t['DLNA_PROTOCOL_INFO_TYPE_HTTP'],
								            dlna.dlna_org_play_speed_t['DLNA_ORG_PLAY_SPEED_NORMAL'],
								            dlna.dlna_org_conversion_t['DLNA_ORG_CONVERSION_NONE'],
								            dlna.dlna_org_operation_t['DLNA_ORG_OPERATION_RANGE'],
									    dlna.flags,
									    child.dlnaProfile)
					buf = CDSService.didlAddItem(buf, child._id,
							  child.parent._id if child.parent is not None else -1,
							  "true", dlna.dlna_profile_upnp_object_item(child.dlnaProfile),
							  child.title, protocol,
							  child.size, child.url, _filter)

				resultCount = resultCount + 1
		buf = CDSService.didlAddFooter(buf)

		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_RESULT, buf)
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_NUM_RETURNED, str(resultCount))
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_TOTAL_MATCH, str(len(entry.children)))

		return resultCount, buf

	@staticmethod
	def cdsSearchDirectChildren(event, buf, index, count, entry, _filter, searchCriteria):
		if entry.children is None:
			return -1,buf
		resultCount = 0

		buf = CDSService.didlAddHeader(buf)

		if (index is 0) and (count is 0):
			count = len(entry.children)

		for child in entry.children:
			if(count is 0) or (resultCount < count):
				if child.children is not None: #Container
					temp,buf = CDSService.cdsSearchDirectChildrenRecursive(buf,
							    0 if count is 0 else count - resultCount,
							    child, _filter, searchCriteria)
					resultCount += temp
				else: #File
					if CDSService.matchesSearch(searchCriteria, child):
						dlna = libDLNA.DLNAInterface()
						protocol = dlna.dlna_write_protocol_info(dlna.dlna_protocol_info_type_t['DLNA_PROTOCOL_INFO_TYPE_HTTP'],
									            dlna.dlna_org_play_speed_t['DLNA_ORG_PLAY_SPEED_NORMAL'],
									            dlna.dlna_org_conversion_t['DLNA_ORG_CONVERSION_NONE'],
									            dlna.dlna_org_operation_t['DLNA_ORG_OPERATION_RANGE'],
										    dlna.flags,
										    entry.dlnaProfile)
						buf = CDSService.didlAddItem(buf, child._id,
								  child.parent._id if child.parent is not None else -1,
								  "true", dlna.dlna_profile_upnp_object_item(child.dlnaProfile),
								  child.title, protocol,
								  child.size, child.url, _filter)
						
						resultCount += 1
		buf = CDSService.didlAddFooter(buf)
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_RESULT, buf)
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_NUM_RETURNED, str(resultCount))
		Service.upnpAddResponse(event, CDSService.SERVICE_CDS_DIDL_TOTAL_MATCH,  str(resultCount))

		return resultCount,buf

	@staticmethod
	def cdsSearchDirectChildrenRecursive(buf, count, entry, _filter, searchCriteria):
		if entry.children is None:
			return -1

		resultCount = 0

		for child in entry.children:
			if (count is 0) or (resultCount < count):
				if child.children is not None: #Container
					newCount,buf = CDSService.cdsSearchDirectChildrenRecursive(buf,
							0 if count is 0 else count - resultCount,
							child, _filter, searchCriteria)
					resultCount += newCount
				else: #File
					if CDSService.matchesSearch(searchCriteria, child):
						dlna = DLNAInterface()
						protocol = dlna.dlna_write_protocol_info(dlna.dlna_protocol_info_type_t['DLNA_PROTOCOL_INFO_TYPE_HTTP'],
									            dlna.dlna_org_play_speed_t['DLNA_ORG_PLAY_SPEED_NORMAL'],
									            dlna.dlna_org_conversion_t['DLNA_ORG_CONVERSION_NONE'],
									            dlna.dlna_org_operation_t['DLNA_ORG_OPERATION_RANGE'],
										    dlna.flags,
										    entry.dlnaProfile)
						buf = CDSService.didlAddItem(buf, child._id,
								  child.parent._id if child.parent is not None else -1,
								  "true", dlna.dlna_profile_upnp_object_item(child.dlnaProfile),
								  child.title, protocol,
								  child.size, child.url, _filter)
						resultCount += 1
		return resultCount, buf

	@staticmethod
	def matchesSearch(searchCriteria, entry):
		dlna = DLNAInterface()
		protocol = dlna.dlna_write_protocol_info(dlna.dlna_protocol_info_type_t['DLNA_PROTOCOL_INFO_TYPE_HTTP'],
					            dlna.dlna_org_play_speed_t['DLNA_ORG_PLAY_SPEED_NORMAL'],
					            dlna.dlna_org_conversion_t['DLNA_ORG_CONVERSION_NONE'],
					            dlna.dlna_org_operation_t['DLNA_ORG_OPERATION_RANGE'],
						    dlna.flags,
						    entry.dlnaProfile)
			
		keyword = CDSService.SEARCH_OBJECT_KEYWORD #Defaults
		derivedFrom = False
		protocolContains = False
		result = False

		if searchCriteria is CDSService.SEARCH_CLASS_MATCH_KEYWORD:
			keyword = CDSService.SEARCH_CLASS_MATCH_KEYWORD
		elif searchCriteria is CDSService.SEARCH_CLASS_DERIVED_KEYWORD:
			derivedFrom = True
			keyword = CDSService.SEARCH_CLASS_DERIVED_KEYWORD
		elif searchCriteria is CDSService.SEARCH_PROTOCOL_CONTAINS_KEYWORD:
			protocolContains = True
			keyword = CDSService.SEARCH_PROTOCOL_CONTAINS_KEYWORD
		
		if (protocolContains) and (protocol.find(keyword) >= 0):
			result = True

		andClause = searchCriteria.find(CDSService.SEARCH_AND)
		if andClause >= 0:
			result = result and CDSService.matchesSearch(searchCriteria[andClause],entry)

		return result
