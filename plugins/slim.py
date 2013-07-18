import os
import urllib
import xml.etree.ElementTree as ET
from util import hook

@hook.command(autohelp=False)
def slimversion(inp, conn=None, chan=None, nick=''):
    "slimversion - output the current versions of slimrom"
	
    os.chmod('plugins/data/slim-version.sh', 0777)
    os.system('./plugins/data/slim-version.sh')
    with open('plugins/data/version-bridge') as f:
        official_version = f.readline()
        weekly_version = f.readline()

    official_version = official_version.strip()
    weekly_version = weekly_version.strip()

    message = "(" + nick + ") The current official version is version " + official_version
    out = "PRIVMSG %s :%s" % (chan, message)
    conn.send(out)
    message = "(" + nick + ") The current weekly version is version " + weekly_version
    out = "PRIVMSG %s :%s" % (chan, message)
    conn.send(out)

@hook.command(autohelp=False)
def slimdevices(inp, conn=None, chan=None, nick=''):
	"slimdevices - output the officially supported devices for slimrom"

	ota_xml = urllib.urlretrieve("http://otaslim.slimroms.net/ota.xml", "plugins/data/ota.xml")

	root = ET.parse('plugins/data/ota.xml').getroot()
	message = "(" + nick + ") officially supported devices are.. "
	
	for child in root[0]:
	    if not "UNOFFICIAL" in child[0].text:
		message = message + child.tag + ", "
		
	os.remove('plugins/data/ota.xml')
	
	out = "PRIVMSG %s :%s" % (chan, message[:-2])
	conn.send(out)

@hook.command		
def slimsearch(inp, conn=None, chan=None, nick=''):
	"slimsearch - query the list of devices to get the url from the website," \
	" for a list of devices, run slimdevices"
	
	urllib.urlretrieve("http://otaslim.slimroms.net/ota.xml", "plugins/data/ota.xml")
	
	inp = inp.split(" ")
	search = inp[0]
	message = ""
	root = ET.parse('plugins/data/ota.xml').getroot()
	
	for url in root.iter(search):
		output_url = url[1].text
		
	try:
		output_url
	except NameError:
		message =  search + " not found, please run the slimdevices command"
		notice(message)
	else:
		message =  "(" + nick + ") " + search + ": " + output_url
		out = "PRIVMSG %s :%s" % (chan, message)
		conn.send(out)
		
	os.remove('plugins/data/ota.xml')
