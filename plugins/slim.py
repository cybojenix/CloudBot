import time
import os
import urllib
import xml.etree.ElementTree as ET
from util import hook
import re, mmap

'''
@hook.singlethread
@hook.event('*')
def slimtest(inp, conn=None):
	urllib.urlretrieve("http://otaslim.slimroms.net/ota.xml", "plugins/data/ota.xml")
	urllib.urlretrieve("http://slimroms.net/index.php/downloads/dlsearch/viewcategory/624-grouper", "plugins/data/624-grouper")
	root = ET.parse('plugins/data/ota.xml').getroot()
	global official_version
	global weekly_version
	
	# officials
	for child in root[0].findall('grouper'):
		cur_official_version = child[0].text
	
	m = re.search('\d+(\.\d+)*-', cur_official_version)
	cur_official_version = m.group(0)[:-1]
	
	#weeklies
	with open('plugins/data/624-grouper', 'r+') as f:
		data = mmap.mmap(f.fileno(), 0)
		mo = re.search('Slim-grouper.*-WEEKLY', data)
	mot = re.search('\d+(\.\d+)*-', mo.group(0))
	cur_weekly_version = mot.group(0)[:-1]

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

	try:
		weekly_version
	except NameError:
		weekly_version = cur_weekly_version
	else:
#		if re.search('\d+\.\d+(\.\d+)+', weekly_version) or \ # will come back to this later
#		re.search('\d+\.\d+(\.\d+)+', cur_weekly_version):
			if not weekly_version == cur_weekly_version:
				weekly_version = cur_weekly_version
				
				channel = "#cafogen"
				message = "a new weekly version of slimrom is is released, version " + official_version
				out = "NOTICE %s :%s" % (channel, message)
				conn.send(out)
	time.sleep(60)

@hook.command(autohelp=False)
def slimversion(inp, say=None):
    "slimversion - output the current versions of slimrom"
	
    say("The current official version is version #" + official_version)
    say("The current weekly version is version #" + weekly_version)

@hook.command(autohelp=False)
def slimdevices(inp, say=None):
	"slimdevices - output the officially supported devices for slimrom"

	root = ET.parse('plugins/data/ota.xml').getroot()
	message = "officially supported devices are.. "
	
	for child in root[0]:
	    if not "UNOFFICIAL" in child[0].text:
		message = message + child.tag + ", "
	say(message[:-2])

@hook.command		
def slimsearch(inp, notice=None, say=None):
	"slimsearch - query the list of devices to get the url from the website," \
	" for a list of devices, run slimdevices"
	
	inp = inp.split(" ")
	search = inp[0]
	message = ""
	root = ET.parse('plugins/data/ota.xml').getroot()
	
	for url in root.iter(search):
		output_url = url[1].text
		
	try:
		output_url
	except NameError:
		message = search + " not found, please run the slimdevices command"
		notice(message)
	else:
		message = search + ": " + output_url
		say(message)
'''
@hook.command		
def slimsearch(inp, notice=None, conn=None, chan=None):
	"slimsearch - query the list of devices to get the url from the website," \
	" for a list of devices, run slimdevices"
	
	if not os.path.isfile('plugins/data/ota.xml'):
		urllib.urlretrieve("http://otaslim.slimroms.net/ota.xml", "plugins/data/ota.xml")
	if time.time() - os.path.getmtime('plugins/data/ota.xml') > (60*30):
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
		message = search + " not found, please run the slimdevices command"
		notice(message)
	else:
		message = search + ": " + output_url
		out = "PRIVMSG %s :%s" % (chan, message)
		conn.send(out)

@hook.command
def slimdetect(inp, conn=None, chan=None):
    """as per the request of the NSA, this command is added in to track people's phones"""
    global slimchannel
    global slimuser
    inp = inp.split(" ")
    if not 'slimuser' in globals():
        slimuser = []
    if not 'slimchannel' in globals():
        slimchannel = {}
    slimuser.append(inp[0])
    slimchannel[inp[0]] = chan
    message = "\001%s \001" % ("VERSION")
    out = "PRIVMSG %s :%s" % (inp[0], message)
    conn.send(out)

@hook.event("NOTICE")
def ctcp_capture(inp, conn=None, input=None):
        global slimchannel
        global slimuser
        if "VERSION" in input.msg and "Android" in input.msg:
            if  slimchannel and slimuser\
              and input.nick in  slimuser:
                message = re.sub("(.*on )|( \(.*\))","",input.msg)
                message = input.nick + " - " + message.replace('\x01', '')
                out = "PRIVMSG %s :%s" % (slimchannel[input.nick], message)
                slimchannel.pop(input.nick)
                slimuser.remove(input.nick)
                conn.send(out)
            else:
                input.reply("please stop trying to go through the ctcp capture")
        elif slimuser and slimchannel \
          and input.nick in slimuser:
            message = input.nick + " is not on Slim IRC."
            out = "PRIVMSG %s :%s" % (slimchannel[input.nick], message)
            slimchannel.pop(input.nick)
            slimuser.remove(input.nick)
            conn.send(out)
