from metadata import mimeTypeList
from service import Service

##
# The connection management service.
class CMSService(Service):
	CMS_DESCRIPTION = """<?xml version="1.0" encoding="utf-8"?>
			         <scpd xmlns="urn:schemas-upnp-org:service-1-0"> 
 			          <specVersion> 
 			            <major>1</major> 
 			            <minor>0</minor> 
 			          </specVersion> 
 			          <actionList> 
 			            <action> 
 			              <name>GetCurrentConnectionInfo</name> 
 			              <argumentList> 
 			                <argument> 
 			                  <name>ConnectionID</name> 
 			                  <direction>in</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_ConnectionID</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>RcsID</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_RcsID</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>AVTransportID</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_AVTransportID</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>ProtocolInfo</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_ProtocolInfo</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>PeerConnectionManager</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_ConnectionManager</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>PeerConnectionID</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_ConnectionID</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>Direction</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_Direction</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>Status</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>A_ARG_TYPE_ConnectionStatus</relatedStateVariable> 
 			                </argument> 
 			              </argumentList> 
 			            </action> 
 			            <action> 
 			              <name>GetProtocolInfo</name> 
 			              <argumentList> 
 			                <argument> 
 			                  <name>Source</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>SourceProtocolInfo</relatedStateVariable> 
 			                </argument> 
 			                <argument> 
 			                  <name>Sink</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>SinkProtocolInfo</relatedStateVariable> 
 			                </argument> 
 			              </argumentList> 
 			            </action> 
 			            <action> 
 			              <name>GetCurrentConnectionIDs</name> 
 			              <argumentList> 
 			                <argument> 
 			                  <name>ConnectionIDs</name> 
 			                  <direction>out</direction> 
 			                  <relatedStateVariable>CurrentConnectionIDs</relatedStateVariable> 
 			                </argument> 
 			              </argumentList> 
 			            </action> 
 			          </actionList> 
 			          <serviceStateTable> 
 			            <stateVariable sendEvents="no"> 
 			              <name>A_ARG_TYPE_ProtocolInfo</name> 
 			              <dataType>string</dataType> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="no"> 
 			              <name>A_ARG_TYPE_ConnectionStatus</name> 
 			             <dataType>string</dataType> 
 			              <allowedValueList> 
 			                <allowedValue>OK</allowedValue> 
 			                <allowedValue>ContentFormatMismatch</allowedValue> 
 			                <allowedValue>InsufficientBandwidth</allowedValue> 
 			                <allowedValue>UnreliableChannel</allowedValue> 
 			                <allowedValue>Unknown</allowedValue> 
 			              </allowedValueList> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="no"> 
 			              <name>A_ARG_TYPE_AVTransportID</name> 
 			              <dataType>i4</dataType> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="no"> 
 			              <name>A_ARG_TYPE_RcsID</name> 
 			              <dataType>i4</dataType> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="no"> 
 			              <name>A_ARG_TYPE_ConnectionID</name> 
 			              <dataType>i4</dataType> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="no"> 
 			              <name>A_ARG_TYPE_ConnectionManager</name> 
 			              <dataType>string</dataType> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="yes"> 
 			              <name>SourceProtocolInfo</name> 
 			              <dataType>string</dataType> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="yes"> 
 			              <name>SinkProtocolInfo</name> 
 			              <dataType>string</dataType> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="no"> 
 			              <name>A_ARG_TYPE_Direction</name> 
 			              <dataType>string</dataType> 
 			              <allowedValueList> 
 			                <allowedValue>Input</allowedValue> 
 			                <allowedValue>Output</allowedValue> 
 			              </allowedValueList> 
 			            </stateVariable> 
 			            <stateVariable sendEvents="yes"> 
 			              <name>CurrentConnectionIDs</name> 
 			              <dataType>string</dataType> 
 			            </stateVariable> 
 			          </serviceStateTable> 
			     </scpd>"""

	##
	# The web address for the cms service.
	CMS_LOCATION = 'cms.xml'

	##
	# Represents the CMS SOURCE argument.
	SERVICE_CMS_ARG_SOURCE = 'Source'

	##
	# Represents the CMS SINK argument.
	SERVICE_CMS_ARG_SINK = 'Sink'

	##
	# Represents the CMS CONNECTION IDs argument.
	SERVICE_CMS_ARG_CONNECTION_IDS = 'ConnectionIDs'

	##
	# Represents the CMS CONNECTION ID argument.
	SERVICE_CMS_ARG_CONNECTION_ID = 'ConnectionID'

	##
	# Represents the CMS RcsID argument.
	SERVICE_CMS_ARG_RCS_ID = 'RcsID'

	##
	# Represents the CMS AVTransportID argument.
	SERVICE_CMS_ARG_TRANSPORT_ID = 'AVTransportID'

	##
	# Represents the CMS ProtocolInfo argument.
	SERVICE_CMS_ARG_PROT_INFO = 'ProtocolInfo'

	##
	# Represents the CMS PeerConnectionmanager argument.
	SERVICE_CMS_ARG_PEER_CON_MANAGER = 'PeerConnectionmanager'

	##
	# Represents the CMS PeerConnectionID argument.
	SERVICE_CMS_ARG_PEER_CON_ID = 'PeerConnectionID'

	##
	# Represents the CMS DIRECTION argument.
	SERVICE_CMS_ARG_DIRECTION = 'Direction'

	##
	# Represents the CMS status argument.
	SERVICE_CMS_ARG_STATUS = 'Status'

	##
	# Represents the CMS default connection ID value.
	SERVICE_CMS_DEFAULT_CON_ID = '0'

	##
	# Represents the CMS unknown connection id value.
	SERVICE_CMS_UNKNOWN_ID = '-1'

	##
	# Represents the CMS Output value.
	SERVICE_CMS_OUTPUT = 'Output'

	##
	# Represents the CMS Success status.
	SERVICE_CMS_STATUS_OK = 'OK'
	
	##
	# Constructs the connection management service.
	def __init__(self):
		self.id_t = 'urn:upnp-org:serviceId:ConnectionManager'
		self.type_t = 'urn:schemas-upnp-org:service:ConnectionManager:1'

		actions = dict()
		actions['GetProtocolInfo'] = CMSService.cmsGetProtocolInfo
		actions['GetCurrentConnectionIDs'] = CMSService.cmsGetCurrentConnectionIDs
		actions['GetCurrentConnectionInfo'] = CMSService.cmsGetCurrentConnectionInfo

		self.actions = actions


	@staticmethod
	def cmsGetProtocolInfo(event):
		if not event:
			return False

		respText = ''

		index = 0
		for mimeType in mimeTypeList:
			respText = respText + Service.mimeGetProtocol(mimeType)
			index = index + 1
			if index != len(mimeTypeList):
				respText = respText + "," 
		
		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_SOURCE, respText)
		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_SINK, '')

		return event['status']

	@staticmethod
	def cmsGetCurrentConnectionIDs(event):
		if not event:
			return False

		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_CONNECTION_IDS, '')

		return event['status']

	@staticmethod
	def cmsGetCurrentConnectionInfo(event):
		if not event:
			return False

		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_CONNECTION_ID, CMSService.SERVICE_CMS_DEFAULT_CON_ID)
		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_RCS_ID, CMSService.SERVICE_CMS_UNKNOWN_ID)
		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_TRANSPORT_ID, CMSService.SERVICE_CMS_UNKNOWN_ID)

		for i in range(len(mimeTypeList)):
			mimeType = mimeTypeList[i]

			protocol = Service.mimeGetProtocol(mimeType)
			Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_PROT_INFO, protocol)

		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_PEER_CON_MANAGER, '')
		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_PEER_CON_ID, CMSService.SERVICE_CMS_UNKNOWN_ID)

		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_DIRECTION, CMSService.SERVICE_CMS_OUTPUT)
		Service.upnpAddResponse(event, CMSService.SERVICE_CMS_ARG_STATUS, CMSService.SERVICE_CMS_STATUS_OK)

		return event['status']

