try:
    from util import hook
except:
    pass

from datetime import datetime, timedelta
from base64 import b64encode
from sys import argv

lg_time_list = []

# 00 to 09
lg_time_list.extend(["F7", "mx", "4i", "0b", "Zp", "57", "L7", "97", "tu", "p5"])
# 10 to 19
lg_time_list.extend(["oW", "Bx", "0U", "Ko", "Uq", "6Y", "GB", "HH", "Ns", "JD"])
#20 to 29
lg_time_list.extend(["KE", "LF", "MJ", "NO", "O6", "31", "Q2", "RQ", "SA", "TF"])
#30 to 39
lg_time_list.extend(["U4", "VF", "WR", "X8", "YB", "ZN", "2R", "bL", "cg", "db"])
# 40 to 49
lg_time_list.extend(["ed", "fd", "gd", "hf", "i8", "j7", "k5", "l3", "md", "nf"])
# 50 to 59
lg_time_list.extend(["oh", "pc", "qv", "rg", "s3", "tq", "u8", "vd", "wc", "xJ"])

def convert_to_lg_time():
    dt = datetime.utcnow() + timedelta(hours=9)
    normtime = []
    normtime.extend([dt.month])
    normtime.extend([dt.day])
    normtime.extend([dt.hour])
    normtime.extend([dt.minute])
    normtime.extend([dt.second])
    converted = ""

    for i in normtime:
        converted = "".join([converted, lg_time_list[i]])

    return converted


def full_lg_fetch_url(path):
    url = "http://dl02.gdms.lge.com:5006/csmg/popup/B2BMANUALDNAction.jsp"
    status = "status=%s" % convert_to_lg_time()
    path = "path=%s" % b64encode(path)
    suffix = "&".join([path, status])
    full = "?".join([url, suffix])
    return full


@hook.command("lgurl")
@hook.command("lgtime")
def lg_func(inp, reply=None):
    if not inp == "":
        to_reply = full_lg_fetch_url(inp)
    else:
        to_reply = convert_to_lg_time()
    reply(to_reply)


if __name__ == "__main__":
    if len(argv) > 1:
        print full_lg_fetch_url(argv[1])
    else:
        print convert_to_lg_time()
