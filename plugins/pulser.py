from util import hook
from time import time

_pulser_last_pinged = None

@hook.regex(r'[cC][lL][oO][uU][dD]')
def pulser(match, message=None, nick=None):
    global _pulser_last_pinged
    if nick == "pulser":
        return
    t = time()
    if _pulser_last_pinged and _pulser_last_pinged - t < 60*5:
        return
    _pulser_last_pinged = t
    message(u"Pulser, %s is talking about Clouds!!" % nick)
