from util import hook
from time import time

_pulser_last_pinged = None

@hook.regex(r'.*(?i)cloud.*')
def pulser(match, message=None, nick=None):
    global _pulser_last_pinged
    if nick.lower() == "pulser":
        return
    t = time()
    if _pulser_last_pinged and t - _pulser_last_pinged < 60*5:
        return
    _pulser_last_pinged = t
    message(u"pulser, %s is talking about Clouds!!" % nick)
