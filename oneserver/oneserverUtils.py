from manager import OneServerManager
try:
	import netinfo
except ImportError:
	OneServerManager().log.error('Library pynetinfo not found')

## Gets the public IPs for the local machine.
# @return a list of IP strings
def getPublicIPs():
	ips = []

	interfaces = netinfo.list_active_devs()
	for interface in interfaces:
		if not interface.startswith('lo'):
			ip = netinfo.get_ip(interface)
			ips.append(ip)

	return ips

