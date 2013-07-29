from util import hook
import json
import re
import os

@hook.event('PRIVMSG')
def catchmessage(inp, input=None):
        dir = "plugins/data/correction/"
        file = dir + input.chan
        if not os.path.exists(dir):
                os.makedirs(dir)
	if not os.path.exists(file):
		f = open(file, 'w+')
		f.close()
        if not re.findall('^s/.*/.*/$', input.msg.lower()):
		if not os.stat(file)[6]==0:
			with open(file, 'r') as f:
				data = json.load(f)
		else:
			data = {}
        	with open(file, 'w') as f:
               		data[str(input.nick)] = str(input.msg)
			json.dump(data, f, ensure_ascii=False)

@hook.regex(r'^S/.*/.*/$')
@hook.regex(r'^s/.*/.*/$')
def correction(inp, say=None, nick=None, input=None, notice=None):
        dir = "plugins/data/correction/"
        file = dir + input.chan
	if not os.path.exists(file):
		notice("I haven't seen anyone say anything on this channel yet")
	else:
		splitinput = input.msg.split("/")
		find = splitinput[1]
		replace = splitinput[2]

		with open(file, 'r') as f:
                	readdata = json.load(f)
		try:
			said = readdata[input.nick]
		except KeyError:
			notice("I haven't seen you say anything here yet")
		else:
			if splitinput[1] in said:
				say("%s meant to say: %s" % (input.nick, said.replace(find, replace)))
