from util import hook
import json

@hook.command(adminlevel = "slim")
def addslimadmin(inp, notice=None):
    "addslimadmin <host> -- Make <host> a slimadmin. " \
    "(you can add multiple slimadmins at once)"
    targets = inp.split()
    for target in targets:
        if target in bot.config["slim"]["slimmembers"]:
            notice("%s is already a slim admin." % target)
        else:
            notice("%s is now a slim admin." % target)
            bot.config["slim"]["slimmembers"].append(target)
            bot.config["slim"]["slimmembers"].sort()
            json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return
	
@hook.command(adminlevel = "slim")
def delslimadmin(inp, notice=None, bot=None, config=None):
    "deladmin <host> -- Make <host> a non-slimadmin." \
    "(you can delete multiple slimadmins at once)"
    targets = inp.split()
    for target in targets:
        if target in bot.config["slim"]["slimmembers"]:
            notice("%s is no longer an admin." % target)
            bot.config["slim"]["slimmembers"].remove(target)
            bot.config["slim"]["slimmembers"].sort()
            json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
        else:
            notice("%s is not an admin." % target)
    return
	
@hook.command(autohelp=False)
def slimadmins(inp, notice=None, bot=None):
    "slimadmins -- Lists bot's slimadmins."
    if bot.config["slim"]["slimmembers"]:
        notice("SlimAdmins are: %s." % ", ".join(bot.config["slim"]["slimmembers"]))
    else:
        notice("There are no users with slim powers.")
    return
