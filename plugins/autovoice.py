from util import hook
from json import dump

@hook.event("JOIN")
def autovoice(inp, nick=None, chan=None, conn=None, bot=None):
    disabled = bot.config["plugins"].get("autovoice_disabled", False)
    if disabled is True:
        print "disabled"
        return
    try:
        if type(bot.config["plugins"]["autovoice"]) is not list:
            print "WARNING: autovoice config malformed"
            return
    except KeyError:
        print "WARNING: autovoice config not set up"
        return None
    channels = [a.lower() for a in bot.config["plugins"]["autovoice"]]
    if not channels:
        print "no channels"
        return
    print channels
    if chan.lower() in channels:
        print "sent voice"
        conn.send("MODE {} +v {}".format(chan, nick))

@hook.command("av", permissions=["autovoice"], autohelp=False)
def autovoice(inp, notice=None, bot=None, input=None):
    if inp == "off":
        bot.config["plugins"]["autovoice_disabled"] = True
        notice("autovoice disabled")
        dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
        return
    if inp == "on":
        bot.config["plugins"]["autovoice_disabled"] = False
        notice("autovoice enabled")
        dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
        return
