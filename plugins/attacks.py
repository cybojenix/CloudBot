import random

from util import hook


with open("plugins/data/larts.txt") as f:
    larts = [line.strip() for line in f.readlines()
             if not line.startswith("//")]

with open("plugins/data/insults.txt") as f:
    insults = [line.strip() for line in f.readlines()
               if not line.startswith("//")]

with open("plugins/data/flirts.txt") as f:
    flirts = [line.strip() for line in f.readlines()
              if not line.startswith("//")]


@hook.command
def lart(inp, action=None, nick=None, conn=None, notice=None, bot=None):
    """lart <user> -- LARTs <user>."""
    target = inp.strip()

    # if the user is trying to make the bot slap itself, slap them
    if target.lower() == conn.nick.lower() or target.lower() in ["itself", "yourself"]:
        target = nick

    masters = bot.config.get("masters", [])
    if masters:
        if target.lower() in masters:
            target = nick

    values = {"user": target}
    phrase = random.choice(larts)

    # act out the message
    action(phrase.format(**values))


@hook.command
def insult(inp, nick=None, message=None, conn=None, notice=None, bot=None):
    """insult <user> -- Makes the bot insult <user>."""
    target = inp.strip()

    if target == conn.nick.lower() or target == "itself":
        target = nick

    masters = bot.config.get("masters", [])
    if masters:
        if target.lower() in masters:   
            target = nick

    out = 'Yo {}... "{}"'.format(target, random.choice(insults))
    message(out)


@hook.command
def flirt(inp, message=None, conn=None, notice=None):
    """flirt <user> -- Make the bot flirt with <user>."""
    target = inp.strip()

    if target == conn.nick.lower():
        target = 'themself'

    out = 'hey {}... "{}"'.format(target, random.choice(flirts))
    message(out)
