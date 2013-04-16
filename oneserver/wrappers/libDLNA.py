## @package This package will provide a python interface to libDLNA

from manager import OneServerManager

import sys
try:
	from ctypes import cdll
	from ctypes import c_char_p,c_int,c_void_p
	from ctypes import POINTER,Structure
	from ctypes.util import find_library
	
except ImportError:
	OneServerManager().log.error("Library Ctypes not found")
	sys.exit()

## Provides the libdlna interface
class DLNAInterface():
	
	dlna_protocol_info_type_t = { 
			"DLNA_PROTOCOL_INFO_TYPE_UNKNOWN": 0,
			"DLNA_PROTOCOL_INFO_TYPE_HTTP"  : 1,
			"DLNA_PROTOCOL_INFO_TYPE_RTP" 	: 2,
			"DLNA_PROTOCOL_INFO_TYPE_ANY" 	: 3}

	dlna_org_play_speed_t = { 
			"DLNA_ORG_PLAY_SPEED_INVALID" : 0,
			"DLNA_ORG_PLAY_SPEED_NORMAL"  : 1}

	dlna_org_conversion_t = {
			"DLNA_ORG_CONVERSION_NONE" : 0,
			"DLNA_ORG_CONVERSION_TRANSCODED" : 1}
	
	dlna_org_operation_t = {
			"DLNA_ORG_OPERATION_NONE" : 0x00,
			"DLNA_ORG_OPERATION_RANGE": 0x01,
			"DLNA_ORG_OPERATION_TIMESEEK" : 0x10}

	dlna_org_flags_t = {
			"DLNA_ORG_FLAG_PACED" 				: (1 <<31),
			"DLNA_ORG_FLAG_TIME_BASED_SEEK" 		: (1 <<30),
			"DLNA_ORG_FLAG_BYTE_BASED_SEEK" 		: (1 <<29),
			"DLNA_ORG_FLAG_PLAY_CONTAINER" 			: (1 <<28),
			"DLNA_ORG_FLAG_SO_INCREASE" 			: (1 <<27),
			"DLNA_ORG_FLAG_SN_INCREASE" 			: (1 <<26),
			"DLNA_ORG_FLAG_RTSP_PAUSE" 			: (1 <<25),
			"DLNA_ORG_FLAG_STREAMING_TRANSFER_MODE" 	: (1 <<24),
			"DLNA_ORG_FLAG_INTERACTIVE_TRANSFERT_MODE" 	: (1 <<23),
			"DLNA_ORG_FLAG_BACKGROUND_TRANSFERT_MODE" 	: (1 <<22),
			"DLNA_ORG_FLAG_CONNECTION_STALL" 		: (1 <<21),
			"DLNA_ORG_FLAG_DLNA_V15" 			: (1 <<20)}

	flags = dlna_org_flags_t['DLNA_ORG_FLAG_STREAMING_TRANSFER_MODE'] |    \
		dlna_org_flags_t['DLNA_ORG_FLAG_BACKGROUND_TRANSFERT_MODE']  | \
		dlna_org_flags_t['DLNA_ORG_FLAG_CONNECTION_STALL'] |           \
		dlna_org_flags_t['DLNA_ORG_FLAG_DLNA_V15']

	dlna_media_class_t = {
			"DLNA_CLASS_UNKNOWN" : 0,
			"DLNA_CLASS_IMAGE"   : 1,
			"DLNA_CLASS_AUDIO"   : 2,
			"DLNA_CLASS_AV"      : 3,
			"DLNA_CLASS_COLLECTION" : 4}

	dlna_media_profile_t = {
			"DLNA_PROFILE_IMAGE_JPEG" 	: 1,
			"DLNA_PROFILE_IMAGE_PNG" 	: 2,
			"DLNA_PROFILE_AUDIO_AC3" 	: 3,
			"DLNA_PROFILE_AUDIO_AMR" 	: 4,
			"DLNA_PROFILE_AUDIO_ATRAC3" 	: 5,
			"DLNA_PROFILE_AUDIO_LPCM" 	: 6,
			"DLNA_PROFILE_AUDIO_MP3" 	: 7,
			"DLNA_PROFILE_AUDIO_MPEG4" 	: 8,
			"DLNA_PROFILE_AUDIO_WMA" 	: 9,
			"DLNA_PROFILE_AV_MPEG1" 	:10,
			"DLNA_PROFILE_AV_MPEG2" 	:11,
			"DLNA_PROFILE_AV_MPEG4_PART2" 	:12,
			"DLNA_PROFILE_AV_MPEG4_PART10" 	:13,
			"DLNA_PROFILE_AV_WMV9" 		:14}



	
	## Initializes the python interface, must be called before any other method
	def __init__(self):
		libPath = find_library("dlna")
		self.dlna = cdll.LoadLibrary(libPath)
		dlna = self.dlna
		
		dlna.dlna_init.restype = POINTER(dlna_t)
		
		dlna.dlna_uninit.argstypes = [POINTER(dlna_t)]

		dlna.dlna_set_verbosity.argstypes = [POINTER(dlna_t), c_int]

		dlna.dlna_set_extension_check.argtypes = [POINTER(dlna_t), c_int]

		dlna.dlna_register_all_media_profiles.argstypes = [POINTER(dlna_t)]

		dlna.dlna_register_media_profile.argstypes = [POINTER(dlna_t), dlna_profile_s]

		dlna.dlna_guess_media_profile.argstypes = [POINTER(dlna_t), c_char_p]
		dlna.dlna_guess_media_profile.restype = POINTER(dlna_profile_s)
		
		dlna.dlna_profile_upnp_object_item.argtypes = [POINTER(dlna_profile_s)]
		dlna.dlna_profile_upnp_object_item.restype = c_char_p

		dlna.dlna_write_protocol_info.argtype = [c_int, c_int, c_int, c_int, c_int, POINTER(dlna_profile_s)]
		dlna.dlna_write_protocol_info.restype = c_char_p
		
		#Oh God, there should be 16 char*
		dlna.dlna_dms_description_get.argtype = [c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]
		dlna.dlna_dms_description_get.restype = c_char_p

	# Here be dragons and C wrapper functions

	## Initialization of the LIbrary
	#  @warning Must be called first
	#  @return the DLNA library's controller
	def dlna_init(self):
		return self.dlna.dlna_init()

	## Unintialization of the library
	#  @param dlna The DLNA library controller
	def dlna_uninit(self, dlna):
		self.dlna.dlna_uninit(dlna)
	
	## Set verbosity of the library
	#  @param dlna The DLNA library Controller
	#  @param level The verbosity level, 0 is off 1 is disable
	def dlna_set_verbosity(self, dlna, level):
		self.dlna.dlna_set_verbosity(dlna,level)

	## Set library's check on file extentions
	#  @param dlna The DLNA library Controller
	#  @param level The level of check (0 is no check, 1 is check)
	def dlna_set_extension_check(self, dlna, level):
		self.dlna.dlna_set_extension_check(dlna, level)

	## Registers all supported DLNA profiles
	#  @param dlna The DLNA library controller
	def dlna_register_all_media_profiles(self, dlna):
		self.dlna.dlna_register_all_media_profiles(dlna)

	## Registers one DLNA profile
	#  @param dlna The DLNA library controller
	#  @param profile The profile ID to register (dlna_media_profile_t)
	def dlna_register_media_profile(self, dlna, profile):
		if profile not in DLNAInterface.dlna_media_profile_t.values():
			raise ValueError("profile must exist in dlna_media_profile_t (no cheating and adding it)")
		self.dlna.dlna_register_media_profile(dlna,profile)

	## Guess which DLNA profile one input file/stream is compatible with
	#  @warning This function returns a pointer that shouldn't be freed
	#  @param dlna The DLNA library Controller
	#  @param filename The file to be checked for compliance
	#  @returns A dlna_profile_s if compatible, None otherwise
	def dlna_guess_media_profile(self,dlna,filename):
		return self.dlna.dlna_guess_media_profile(dlna,filename)

	## Provides teh UPnP A/V ContentDirectory Object Item associated to the profile
	#  @warning Don't free the returned pointer
	#  @param profile The targeted DLNA profile
	#  @return A pointer on CDS Object Item string
	def dlna_profile_upnp_object_item(self, profile):
		return self.dlna.dlna_profile_upnp_object_item(profile)

	## Output the protocol information string that must be sent by a DMS to a DMP
	#  for the file to be played/recognized
	# @param streaming_ type Streaming method 		(dlna_protocol_info_type_t)
	# @param speed DLNA.ORG_PS parameter 	(dlna_org_play_speed_t)
	# @param ci DLNA.ORG_CI paramter 	(dlna_org_conversion_t)
	# @param op DLNA.ORG_OP paramter 	(dlna_org_operation_t)
	# @param flags DLNA.ORG_FLAGS paramter 	(dlna_org_flags_t)
	# @param profile The DLNA's file profil (POINTER(dlna_profile_s))
	# @return The protocol information string
	def dlna_write_protocol_info(self, streaming_type, speed, ci, op, flags, p):
		if streaming_type not in DLNAInterface.dlna_protocol_info_type_t.values():
			raise ValueError("streaming_type must be in dlna_protocol_info_type_t")
		if speed not in DLNAInterface.dlna_org_play_speed_t.values():
			raise ValueError("speed must be in dlna_org_play_speed_t")
		if ci not in DLNAInterface.dlna_org_conversion_t.values():
			raise ValueError("ci must be in dlna_org_conversion_t")
		if op not in DLNAInterface.dlna_org_operation_t.values():
			raise ValueError("op must be in dlna_org_operation_t")
		OneServerManager().log.debug("type=%s, speed=%s, ci=%s, op=%s, flags=%s, profile=%s" % (streaming_type, speed,ci,op,flags,p))
		return self.dlna.dlna_write_protocol_info(streaming_type,speed,ci,op,flags,p)

	## Create a valid UPnP device description for Digital Media Server (DMS).
	#
	# @param friendly_name      UPnP device friendly name.
	# @param manufacturer       UPnP device manufacturer.
	# @param manufacturer_url   UPnP device manufacturer URL.
	# @param model_description  UPnP device model description.
	# @param model_name         UPnP device model name.
	# @param model_number       UPnP device model number.
	# @param model_url          UPnP device model URL.
	# @param serial_number      UPnP device serial number.
	# @param uuid               UPnP device unique identifier.
	# @param presentation_url   UPnP device web presentation page URL.
	# @param cms_scpd_url       UPnP ConnectionManager service SCPD URL.
	# @param cms_control_url    UPnP ConnectionManager service control URL.
	# @param cms_event_url      UPnP ConnectionManager service event URL.
	# @param cds_scpd_url       UPnP ContentDirectory service SCPD URL.
	# @param cds_control_url    UPnP ContentDirectory service control URL.
	# @param cds_event_url      UPnP ContentDirectory service event URL.
	# 
	# @return                       The DMS device description string.
	def dlna_dms_description_get(self, friendly_name, manufacturer,manufacturer_url, model_description,model_name,
			model_number, model_url,serial_number,uuid,presentation_url,cms_scpd_url,cms_control_url,
			cms_event_url,cds_scpd_url,cds_control_url,cds_event_url):
		return self.dlna.dlna_dms_description_get(friendly_name, manufacturer,manufacturer_url, model_description,model_name,
			model_number, model_url,serial_number,uuid,presentation_url,cms_scpd_url,cms_control_url,
			cms_event_url,cds_scpd_url,cds_control_url,cds_event_url)


	
class dlna_profile_s(Structure): pass
dlna_profile_s._fields_ = [
		( "id", c_char_p),
		( "mime", c_char_p),
		( "label", c_char_p),
		( "class", c_int)]

class dlna_t(Structure): pass
dlna_t._fields_ = [
		( "inited", c_int),
		( "verbosity", c_int),
		( "check_extentions", c_int),
		( "first_profile", c_void_p)]
