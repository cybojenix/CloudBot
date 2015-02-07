from util import hook
from time import time

_pulser_last_pinged = {}

#@hook.regex(r'.*(?i)cloud.*')
def pulser(match, message=None, nick=None, chan=None):
    global _pulser_last_pinged
    if nick.lower() == "pulser":
        return
    t = time()
    if t - _pulser_last_pinged.get(chan.lower(), 0) < 60*5:
        return
    _pulser_last_pinged[chan.lower()] = t
    message(u"pulser, %s is talking about Clouds!!" % nick)
