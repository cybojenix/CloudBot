from util import hook, http

convert_url = "http://rate-exchange.appspot.com/currency?from={}&to={}&q=1"

@hook.command
def convert(inp):
    """
    convert <from> <to> [amount] -- convert [amount] <from> to <to>
    """

    input = inp.lower().strip()
    parts = input.split()

    ffrom = parts[0]
    to = parts[1]
    try:
        amount = float(parts[2])
    except IndexError:
        amount = 1
    except ValueError:
        return "only use numbers for the quantity"

    page = http.get_json(convert_url.format(ffrom, to))
    if page.get("err", None):
        return "invalid currency"
    if page.get("warning", None):
        return "invalid quantity"
    value = page.get("v", None)
    if not value:
        return "dafuq just happened..."
    value = float(value) * float(amount)
    return_statement = "{:.2f} {} is {:.2f} {}".format(amount, ffrom, value, to)
    return return_statement
