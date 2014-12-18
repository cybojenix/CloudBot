from util import hook

import re

CORRECTION_RE1 = r'^(s|S)/.*/.*/?\S*$'
CORRECTION_RE2 = r'^(s|S):.*:.*:?\S*$'
delims = "/:"

def correction_logic(match, delim, input, conn, message, nick):
    split = input.msg.split(delim)

    if len(split) == 4:
        if split[3]:
            nick = split[3]
    nick = nick.lower()

    find = split[1]
    if not find:
        return u"Nothing to replace"
    replace = split[2]

    for item in conn.history[input.chan].__reversed__():
        name, timestamp, msg = item
        if msg[:2] in ["s%s" % d for d in delims]:
            # don't correct corrections, it gets really confusing
            continue
        if nick:
            if nick != name.lower():
                continue
        if find in msg:
            if "\x01ACTION" in msg:
                msg = msg.replace("\x01ACTION ", "/me ").replace("\x01", "")
            message(u"Correction, <{}> {}".format(name, msg.replace(find, "\x02" + replace + "\x02")))
            return
        else:
            continue

    return u"Did not find \"{}\" in any of {}'s recent messages.".format(find, nick)

@hook.regex(CORRECTION_RE1)
def correction1(match, input=None, conn=None, message=None, nick=None):

    return correction_logic(match, "/", input, conn, message, nick)


@hook.regex(CORRECTION_RE2)
def correction2(match, input=None, conn=None, message=None, nick=None):

    return correction_logic(match, ":", input, conn, message, nick)

