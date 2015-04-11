from util import hook, http
from time import time

_conv_data = {}
_conv_last_edit = None


def load_data(api_key):
    global _conv_data
    global _conv_last_edit

    if _conv_last_edit is not None and _conv_data and time() - _conv_last_edit < 2700:
        return _conv_data

    _conv_last_edit = time()
    url = "https://openexchangerates.org/api/latest.json?app_id={}".format(api_key)
    _conv_data = http.get_json(url)
    return _conv_data


@hook.command
def convert(inp, bot=None):
    """
    convert <from> <to> [amount] -- convert [amount] <from> to <to>
    """
    api_key = bot.config.get("api_keys", {}).get("openexchangerates")
    if not api_key:
        return "api key not added"

    input = inp.upper().strip()
    parts = input.split()

    try:
        ffrom = parts[0]
        to = parts[1]
    except IndexError:
        return "invalid arguments"

    try:
        amount = float(parts[2])
    except IndexError:
        amount = 1
    except ValueError:
        return "only use numbers for the quantity"

    data = load_data(api_key)
    if not data:
        return "internal error: data not loaded"
    rates = data.get("rates", {})
    if not rates:
        return "internal error: rates not loaded"

    f = rates.get(ffrom)
    if f is None:
        return "base currency not known"
    t = rates.get(to)
    if t is None:
        return "target currency not known"

    value = (float(amount)/float(f))*float(t)
    return "{:.2f} {} is {:.2f} {}".format(amount, ffrom, value, to)
