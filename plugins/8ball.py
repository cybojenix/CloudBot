from util import hook
from util.text import multiword_replace
import random

color_codes = {
    "<r>": "\x02\x0305",
    "<g>": "\x02\x0303",
    "<y>": "\x02"
}

with open("plugins/data/8ball_responses.txt") as f:
    responses = [line.strip() for line in
        f.readlines()if not line.startswith("//")]



@hook.command('8ball')
def eightball(inp, conn=None, chan=None, nick='', mask='', bot=None, notice=None):
    "8ball [channel] <question> -- The all knowing magic eight ball, " \
    "in electronic form. Ask and it shall be answered!" \
    "If [channel] is blank the bot will answer the question in the channel the " \
    "command was used in."

    # here we use voodoo magic to tell the future
    magic = multiword_replace(random.choice(responses), color_codes)

    inp = inp.split(" ")
    if inp[0][0] == "#":
        admins = bot.config.get('admins', [])
        if nick not in admins and mask not in admins:
	    notice("Sorry, you are not allowed to use this command.")
        else:
    	    message = "(" + nick + ") "
            for x in inp[1:]:
                message = message + x + " "
	    message = message[:-1]
	    out = "PRIVMSG %s :%s" % (inp[0], message)
	    conn.send(out)
	    message = "the magic 8 ball says..." + magic
            out = "PRIVMSG %s :%s" % (inp[0], message)
	    conn.send(out)
    else:
	message = "the magic 8 ball says..." + magic
        out = "PRIVMSG %s :%s" % (chan, message)
        conn.send(out)
