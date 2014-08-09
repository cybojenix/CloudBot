from util import hook
from json import dump

@hook.command(permissions=["masters"])
def masters(inp, notice=None, bot=None):
    """masters -- List all the users with master protection"""
    masters = bot.config.get("masters", [])
    if masters:
        notice("Users with master protection are: {}".format(", ".join(masters)))
    else:
        notice("There are no masters")
    return

@hook.command(permissions=["masters"])
def master(inp, notice=None, bot=None):
    """master <nick> -- Adds master protection to <nick>"""
    target = inp.lower()
    masters = bot.config.get("masters", [])
    if target in masters:
        notice("{} is already a master".format(target))
        return
    notice("{} has been given master protection".format(target))
    masters.append(target)
    masters.sort()
    dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return

@hook.command(permissions=["masters"])
def unmaster(inp, notice=None, bot=None):
    """unmaster <nick> -- Removes master protection from <nick>"""
    target = inp.lower()
    masters = bot.config.get("masters", [])
    if not target in masters:
        notice("{} is not a master".format(target))
        return
    notice("{} has lost master protection".format(target))
    masters.remove(target)
    masters.sort()
    dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return
