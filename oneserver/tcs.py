from entry import Entry
from manager import OneServerManager
import os
from wrappers.libDLNA import DLNAInterface

def populate(files):
	if len(files) <= 0:
		raise ValueError("Invalid list")
	
	manager = OneServerManager()
	
	tcsRoot =  Entry("/tcs", manager.CONTAINER_MIME, None, [], "TCS", "tcs", -1, None)


	idlna = DLNAInterface()
	dlna  = manager.dlna
	
	for f in files:
		profile = idlna.dlna_guess_media_profile(dlna, f)

		manager.log.debug('Profile for %s: %s', f, str(profile))

		if profile is None:
			raise ValueError("Invalid media type on {0}".format(f))
		try:
			profile.contents
		except ValueError:
			OneServerManager().log.debug("Invalid profile object, skipping "+f)
			break
		
		size = os.path.getsize(f)

		child = Entry(f, profile, tcsRoot, None, f, "", size, createLocalFileHandle)
		tcsRoot.children.append(child)

	return tcsRoot

def createLocalFileHandle(entry):
	fh =  open(entry.fullPath, "r")
	OneServerManager().log.debug("Opened fh at {0}".format(str(fh)))
	return fh
