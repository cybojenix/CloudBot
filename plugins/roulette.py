# russian roulette
import random
from util import hook
import os
import json
import time

@hook.command(autohelp=False)
def load(inp, say=None, me=None, chan=None):
	"load [<number of barrels>] [<number of bullets>] - " \
	" load the gun up"
	dir = "plugins/data/rr/"
	if not os.path.exists(dir):
		os.makedirs(dir)
	file = dir + chan
	
	try:
		inp[0]
	except IndexError:
		no_barrels = 6
		no_bullet = 1
	else:
		inp = inp.split(" ")
		try:
			inp[0]
			inp[1]
		except IndexError:
			no_barrels = 6
			no_bullet = 1
		else:
			try:
				int(inp[0])
				int(inp[1])
			except ValueError:
				no_barrels = 6
				no_bullet = 1
			else:
				no_barrels =int(inp[0])
				no_bullet = int(inp[1])
	
	bullet_place = []
	
	me("loads the bullets, spins the barrel...")
	for x in range(no_bullet):
		bul_pl = random.randint(1, no_barrels)
		while bul_pl in bullet_place:
			bul_pl = random.randint(1, no_barrels)
		bullet_place.append(bul_pl)
	
	data = json.dumps({'no_bullet': no_bullet, 'current_position': 0, 'bullet_place': bullet_place, 'dead': []})
	with open(file, 'w+') as final_file:
		final_file.write(data)
	
	say("the bullets have been loaded. pull the trigger...")

@hook.command(autohelp=False)
def pull(inp, say=None, nick=None, notice=None, me=None, chan=None):
	"pull the trigger"
	file = "plugins/data/rr/" + chan
	if not os.path.exists(file):
		notice("please start a game with command load")
	else:
		with open(file, 'r') as final_file:
			data = json.load(final_file)
			
		no_bullet = data["no_bullet"]
		current_position = data["current_position"]
		bullet_place = data["bullet_place"]
		dead = data["dead"]
		
		if nick in dead:
			say("you can not shoot if you are dead %s" % nick)
		else:
			if no_bullet == 0:
				notice("please start a game with command load")
			else:
				say("click....")
				time.sleep(2)
				current_position += 1
				if current_position in bullet_place:
					say("BANG!! %s is DEAD" % nick)
					no_bullet -= 1
					dead.append(nick)
				
					if chan[0] == "#":
						me("drags the body off...")
						out = "KICK %s %s : you died...." % (chan, nick)
				else:
					say("%s gets to live another day.." % nick)
				if no_bullet == 0:
					say("there are no bullets left")

				data = json.dumps({'no_bullet': no_bullet, 'current_position': current_position, 'bullet_place': bullet_place, 'dead': dead})
				with open(file, 'w+') as final_file:
					final_file.write(data)
			
