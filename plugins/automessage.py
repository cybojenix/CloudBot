from util import hook
import time
import json

@hook.event("JOIN")
def joineventmessage(inp, notice=None, chan=None, bot=None):
    try:
        bot.config["plugins"]["automessage"][chan.lower()]
    except KeyError:
        return None
    try:
        on = bot.config["plugins"]["automessage"][chan.lower()]["on"]
        message = bot.config["plugins"]["automessage"][chan.lower()]["message"]
    except KeyError:
        print "malformed config file"
        return

    if not on == "true":
        return None

    time.sleep(5)
    notice(message)

@hook.command("am", permissions=["automessage"])
def automessage(inp, notice=None, bot=None, mask=None):
    "am [option] -- configurator for automessage, see am help for more details"
    split = inp.split(" ")
    am_commands = ['addchan', 'changemessage', 'delchan', 'disablechan', \
        'enablechan', 'help', 'info']
    # lets be kind and give the users a manual
    if "addchan" in split[0:2]:
        help_message = "am addchan [channel] [message] -- add a channel to the automessage list"
    elif "changemessage" in split[0:2]:
        help_message = "am changemessage [channel] [message] -- change the message to send to a channel"
    elif "delchan" in split[0:2]:
        help_message = "am delchan [channel] -- remove a channel from the automessage list"
    elif "disablechan" in split[0:2]:
        help_message = "am disablechan [channel] -- disables the automessage on a certain channel"
    elif "enablechan" in split[0:2]:
        help_message = "am enablechan [channel] -- enables the automessage on a certain channel"
    elif "help" in split[0:2]:
        help_message = "am [option] -- configurator for automessage, see am help for more details"
    elif "info" in split[0:2]:
        help_message = "am info [channel] -- lists channels that have automessage, with a * next to the enabled channels. "
        help_message += "If a channel is defined, the message to be sent is shown, along with the creator"
    else:
        notice("please refer to \"am help\"")
        return

    if split[0] == "help":
        try:
            option = split[1]
        except IndexError:
            notice("am [option] -- configurator for automessage. available options are...")
            notice(", ".join(am_commands))
            return
        if option in am_commands:
            notice(help_message)
        else:
            notice("Invalid command. Supported commands are...")
            notice(", ".join(am_commands))
        return

    # define all the variables from the start, easy tracking
    channels = []
    message_config = bot.config["plugins"]["automessage"]
    for k in message_config:
        channels.append(k)

    if not split[0] == "info":
        try:
            if not split[1][0] == "#":
                split[1] = "#" + split[1]
            channel = split[1].lower()
        except IndexError:
            notice(help_message)
            return
    if split[0] in ('addchan', 'changemessage'):
        try:
            mess_base = split[2]
        except IndexError:
            notice(help_message)
            return
         
    if split[0] == "addchan":
        if channel in channels:
            notice("%s is already set up to recieve automessages" % channel)
            return
        message = " ".join(split[2:])
        notice("added automessages for %s" % channel)
        message_config[channel] = {"on": "true", "message": message, "creator": mask}
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)

    if split[0] == "delchan":
        if not channel in channels:
            notice("%s does not recieve automessages anyway.." % channel)
            return
        notice("removed %s from recieving automessages" % channel)
        del message_config[channel]
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)

    if split[0] == "changemessage":
        if not channel in channels:
            notice("%s has not been set up to recieve automessages" % channel)
            return
        message = " ".join(split[2:])
        notice("changed automessage for %s to %s" % (channel, message))
        message_config[channel]["message"] = message
        message_config[channel]["creator"] = mask
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)

    if split[0] == "disablechan":
        if not channel in channels:
            notice("%s has not been set up to recieve automessages" % channel)
            return
        message_config[channel]["on"] = "false"
        notice("%s's automessages have been disabled" % channel)
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)

    if split[0] == "enablechan":
        if not channel in channels:
            notice("%s has not been set up to recieve automessages" % channel)
            return
        message_config[channel]["on"] = "true"
        notice("%s's automessages have been enabled" % channel)
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)

    if split[0] == "info":
        try:
            if not split[1][0] == "#":
                split[1] = "#" + split[1]
            channel = split[1].lower()
        except IndexError:
            message = ""
            notice("channels with automessage are...")
            for v in channels:
                if message_config[v]["on"] == "true":
                    message += v + "*, "
                else:
                    message += v + ", "
            notice(message[:-2])
            notice("(note, channels marked with * are enabled)")
            return
        if not channel in channels:
            notice("%s has not been set up to recieve automessages" % channel)
            return
        notice("information on %s..." % channel)
        if message_config[channel]["on"] == "true":
            notice("enabled: yes")
        else:
            notice("enabled: no")
        notice("automessage: %s" % message_config[channel]["message"])
        notice("message creator: %s" % message_config[channel]["creator"])
        return
