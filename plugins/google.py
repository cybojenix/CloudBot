from util import hook, http, text


API_CS = 'https://www.googleapis.com/customsearch/v1'


def get_keys(config):
    return {
        'cx': config['api_keys']['google_cse_id'],
        'key': config['api_keys']['google_dev_key']
    }


@hook.command('search')
@hook.command('g')
@hook.command
def google(inp, bot=None):
    try:
        keys = get_keys(bot.config)
    except KeyError:
        return u"API Keys not configured"

    parsed = http.get_json(API_CS, q=inp, **keys)

    try:
        result = parsed['items'][0]
    except KeyError:
        return u"No results found."

    title = text.truncate_str(result['title'], 60)
    content = result['snippet']

    if not content:
        content = "No description available."
    else:
        content = text.truncate_str(content.replace('\n', ''), 150)

    return u'{} -- \x02{}\x02: "{}"'.format(result['link'], title, content)


@hook.command('image')
@hook.command('gis')
@hook.command
def googleimage(inp, bot=None):
    try:
        keys = get_keys(bot.config)
    except KeyError:
        return u"API Keys not configured"

    parsed = http.get_json(API_CS, q=inp, searchType="image", **keys)

    try:
        result = parsed['items'][0]
        metadata = parsed['items'][0]['image']
    except KeyError:
        return u"No results found."

    dimens = '{}x{}px'.format(metadata['width'], metadata['height'])
    title = text.truncate_str(result['title'], 60)

    return u'{} [{}, {}]'.format(result['link'], dimens, result['mime'])
