import os

from util import hook

@hook.command('slim')
def slim(inp, conn=None, chan=None, nick=''):
        "slim [option] -- options are 'version' " \
        "more to come!"
        inp = inp.split(" ")
        if inp[0][0] == "v":
                os.chmod('plugins/data/slim-version.sh', 0777)
                os.system('./plugins/data/slim-version.sh')
                with open('plugins/data/version-bridge') as f:
                        official_version = f.readline()
                        weekly_version = f.readline()

                official_version = official_version.strip()
                weekly_version = weekly_version.strip()

                message = "(" + nick + ") The current official version is version " + official_version
                out = "PRIVMSG %s :%s" % (chan, message)
                conn.send(out)
                message = "(" + nick + ") The current weekly version is version " + weekly_version
                out = "PRIVMSG %s :%s" % (chan, message)
                conn.send(out)
