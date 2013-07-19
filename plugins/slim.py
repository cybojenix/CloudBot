import time
import os
import urllib
import xml.etree.ElementTree as ET
from util import hook
import re

@hook.singlethread
@hook.event('*')
def slimtest(inp, conn=None):
	urllib.urlretrieve("http://otaslim.slimroms.net/ota.xml", "plugins/data/ota.xml")
	root = ET.parse('plugins/data/ota.xml').getroot()
	global official_version
	
	for child in root[0].findall('grouper'):
		cur_official_version = child[0].text
	
	m = re.search('\d+(\.\d+)*-', cur_official_version)
	cur_official_version = m.group(0)[:-1]
	
	try:
		official_version
	except NameError:
		official_version = cur_official_version
	else:
#		if re.search('\d+\.\d+(\.\d+)+', official_version) or \ # will come back to this later
#		re.search('\d+\.\d+(\.\d+)+', cur_official_version):
			if not official_version == cur_official_version:
				official_version = cur_official_version
				
				channel = "#slimusers"
				message = "a new version of slimrom is is released, version " + official_version
				out = "NOTICE %s :%s" % (channel, message)
				conn.send(out)
	time.sleep(300)

#@hook.singlethread
#@hook.event('*')
#def slimtest(inp, conn=None):
#    channel = "#cafogen"
#    message = "test, sorry"
#    out = "NOTICE %s :%s" % (channel, message)
#    conn.send(out)
#    time.sleep(300)

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
