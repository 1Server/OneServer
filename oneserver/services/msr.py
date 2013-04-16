from service import Service

class MSRService(Service):
	MSR_DESCRIPTION = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<scpd xmlns=\"urn:schemas-upnp-org:service-1-0\">
<specVersion>
  <major>1</major>
  <minor>0</minor>
</specVersion>
<actionList>
  <action>
    <name>IsAuthorized</name>
    <argumentList>
      <argument>
        <name>DeviceID</name>
        <direction>in</direction>
        <relatedStateVariable>A_ARG_TYPE_DeviceID</relatedStateVariable>
      </argument>
      <argument>
        <name>Result</name>
        <direction>out</direction>
        <relatedStateVariable>A_ARG_TYPE_Result</relatedStateVariable>
      </argument>
    </argumentList>
  </action>
  <action>
    <name>RegisterDevice</name>
    <argumentList>
      <argument>
        <name>RegistrationReqMsg</name>
        <direction>in</direction>
        <relatedStateVariable>A_ARG_TYPE_RegistrationReqMsg</relatedStateVariable>
      </argument>
      <argument>
        <name>RegistrationRespMsg</name>
        <direction>out</direction>
        <relatedStateVariable>A_ARG_TYPE_RegistrationRespMsg</relatedStateVariable>
      </argument>
    </argumentList>
  </action>
  <action>
    <name>IsValidated</name>
    <argumentList>
      <argument>
        <name>DeviceID</name>
        <direction>in</direction>
        <relatedStateVariable>A_ARG_TYPE_DeviceID</relatedStateVariable>
      </argument>
      <argument>
        <name>Result</name>
        <direction>out</direction>
        <relatedStateVariable>A_ARG_TYPE_Result</relatedStateVariable>
      </argument>
    </argumentList>
  </action>
</actionList>
<serviceStateTable>
  <stateVariable sendEvents=\"no\">
    <name>A_ARG_TYPE_DeviceID</name>
    <dataType>string</dataType>
  </stateVariable>
  <stateVariable sendEvents=\"no\">
    <name>A_ARG_TYPE_Result</name>
    <dataType>int</dataType>
  </stateVariable>
  <stateVariable sendEvents=\"no\">
    <name>A_ARG_TYPE_RegistrationReqMsg</name>
    <dataType>bin.base64</dataType>
  </stateVariable>
  <stateVariable sendEvents=\"no\">
    <name>A_ARG_TYPE_RegistrationRespMsg</name>
    <dataType>bin.base64</dataType>
  </stateVariable>
  <stateVariable sendEvents=\"no\">
    <name>AuthorizationGrantedUpdateID</name>
    <dataType>ui4</dataType>
  </stateVariable>
  <stateVariable sendEvents=\"no\">
    <name>AuthorizationDeniedUpdateID</name>
    <dataType>ui4</dataType>
  </stateVariable>
  <stateVariable sendEvents=\"no\">
    <name>ValidationSucceededUpdateID</name>
    <dataType>ui4</dataType>
  </stateVariable>
  <stateVariable sendEvents=\"no\">
    <name>ValidationRevokedUpdateID</name>
    <dataType>ui4</dataType>
  </stateVariable>
</serviceStateTable>
</scpd>"""

	MSR_LOCATION = 'msr.xml'
	MSR_SERVICE_ID = 'urn:microsoft.com:serviceId:X_MS_MediaReceiverRegistrar'
	MSR_SERVICE_TYPE = 'urn:microsoft.com:service:X_MS_MediaReceiverRegistrar:1'

	##
	# Represents the MSR IsAuthorized action.
	SERVICE_MSR_ACTION_IS_AUTHORIZED = 'IsAuthorized'

	##
	# Represents the MSR RegisterDevice action.
	SERVICE_MSR_ACTION_REGISTER_DEVICE = 'RegisterDevice'

	##
	# Represents the MSR IsValidated action.
	SERVICE_MSR_ACTION_IS_VALIDATED = 'IsValidated'

	##
	# Represents the MSR DeviceID argument.
	SERVICE_MSR_ARG_DEVICE_ID = 'DeviceID'

	##
	# Represents the MSR Result argument.
	SERVICE_MSR_ARG_RESULT = 'Result'

	##
	# Represents the MSR RegistrationReqMsg argument.
	SERVICE_MSR_ARG_REGISTRATION_REQUEST_MSG = 'RegistrationReqMsg'

	##
	# Represents the MSR RegistrationRespMsg argument.
	SERVICE_MSR_ARG_REGISTRATION_RESPONSE_MSG = 'RegistrationRespMsg'

	##
	# Represents the MSR Registered/Activated ID value.
	SERVICE_MSR_STATUS_OK = '1'

	def __init__(self):
		self.id_t   = self.MSR_SERVICE_ID
		self.type_t = self.MSR_SERVICE_TYPE

		actions = dict()
		actions[self.SERVICE_MSR_ACTION_IS_AUTHORIZED]   = MSRService.msrIsAuthorized
		actions[self.SERVICE_MSR_ACTION_REGISTER_DEVICE] = MSRService.msrRegsiterDevice
		actions[self.SERVICE_MSR_ACTION_IS_VALIDATED]    = MSRService.msrIsValidated

		self.actions = actions

	@staticmethod
	def msrIsAuthorized(event):
		if not event:
			return False

		# Sends a fake authorization.
		Service.upnpAddResponse(event, MSRService.SERVICE_MSR_ARG_RESULT, MSRService.SERVICE_MSR_STATUS_OK)

		return event.status

	@staticmethod
	def msrRegsiterDevice(event):
		if not event:
			return False

		# Take no action.

		return event.status

	@staticmethod
	def msrIsValidated(event):
		if not event:
			return False

		# Sends a fake authorization.
		Service.upnpAddResponse(event, MSRService.SERVICE_MSR_ARG_RESULT, MSRService.SERVICE_MSR_STATUS_OK)

		return event.status

