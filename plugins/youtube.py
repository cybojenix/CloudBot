import re
import time

import isodate
import requests

from util import timeformat, hook

def pluralize(num=0, text=''):
    """
    Takes a number and a string, and pluralizes that string using the number and combines the results.
    :rtype: str
    """
    return "{:,} {}{}".format(num, text, "s"[num == 1:])


youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)([-_a-zA-Z0-9]+)', re.I)

base_url = 'https://www.googleapis.com/youtube/v3/'
api_url = base_url + 'videos?part=contentDetails%2C+snippet%2C+statistics&id={}&key={}'
search_api_url = base_url + 'search?part=id&maxResults=1'
playlist_api_url = base_url + 'playlists?part=snippet%2CcontentDetails%2Cstatus'
video_url = "http://youtu.be/%s"
err_no_api = "The YouTube API is off in the Google Developers Console."
yt_dev_key = None

def get_video_description(video_id):
    global yt_dev_key
    if not yt_dev_key:
        return
    json = requests.get(api_url.format(video_id, yt_dev_key)).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return

    data = json['items']
    snippet = data[0]['snippet']
    statistics = data[0]['statistics']
    content_details = data[0]['contentDetails']

    out = '\x02{}\x02'.format(snippet['title'])

    if not content_details.get('duration'):
        return out

    length = isodate.parse_duration(content_details['duration'])
    out += ' - length \x02{}\x02'.format(timeformat.format_time(int(length.total_seconds()), simple=True))
    total_votes = float(statistics['likeCount']) + float(statistics['dislikeCount'])

    if total_votes != 0:
        # format
        likes = pluralize(int(statistics['likeCount']), "like")
        dislikes = pluralize(int(statistics['dislikeCount']), "dislike")

        percent = 100 * float(statistics['likeCount']) / total_votes
        out += ' - {}, {} (\x02{:.1f}\x02%)'.format(likes,
                                                    dislikes, percent)

    if 'viewCount' in statistics:
        views = int(statistics['viewCount'])
        out += ' - \x02{:,}\x02 view{}'.format(views, "s"[views == 1:])

    uploader = snippet['channelTitle']

    upload_time = time.strptime(snippet['publishedAt'], "%Y-%m-%dT%H:%M:%S.000Z")
    out += ' - \x02{}\x02 on \x02{}\x02'.format(uploader,
                                                time.strftime("%Y.%m.%d", upload_time))

    if 'contentRating' in content_details:
        out += ' - \x034NSFW\x02'

    return out


def yt_load_dev_key(bot):
    global yt_dev_key
    if not yt_dev_key:
        yt_dev_key = bot.config.get("api_keys", {}).get("google_dev_key", None)
        if not yt_dev_key:
            return False
    return True


@hook.regex(*youtube_re)
def youtube_url(match, bot=None):
    if not yt_load_dev_key(bot):
        return
    return get_video_description(match.group(1))


@hook.command('you')
@hook.command('yt')
@hook.command('y')
@hook.command
def youtube(inp, bot=None):
    """youtube <query> -- Returns the first YouTube search result for <query>."""
    if not yt_load_dev_key(bot):
        return "This command requires a Google Developers Console API key."

    json = requests.get(search_api_url, params={"q": inp, "key": yt_dev_key}).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return 'Error performing search.'

    if json['pageInfo']['totalResults'] == 0:
        return 'No results found.'

    video_id = json['items'][0]['id']['videoId']

    return get_video_description(video_id) + " - " + video_url % video_id


@hook.command("ytime")
@hook.command
def youtime(inp):
    """youtime <query> -- Gets the total run time of the first YouTube search result for <query>."""
    if not yt_load_dev_key(bot):
        return "This command requires a Google Developers Console API key."

    json = requests.get(search_api_url, params={"q": inp, "key": dev_key}).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return 'Error performing search.'

    if json['pageInfo']['totalResults'] == 0:
        return 'No results found.'

    video_id = json['items'][0]['id']['videoId']
    json = requests.get(api_url.format(video_id, dev_key)).json()

    if json.get('error'):
        return
    data = json['items']
    snippet = data[0]['snippet']
    content_details = data[0]['contentDetails']
    statistics = data[0]['statistics']

    if not content_details.get('duration'):
        return

    length = isodate.parse_duration(content_details['duration'])
    l_sec = int(length.total_seconds())
    views = int(statistics['viewCount'])
    total = int(l_sec * views)

    length_text = timeformat.format_time(l_sec, simple=True)
    total_text = timeformat.format_time(total, accuracy=8)

    return 'The video \x02{}\x02 has a length of {} and has been viewed {:,} times for ' \
           'a total run time of {}!'.format(snippet['title'], length_text, views,
                                            total_text)


ytpl_re = (r'(.*:)//(www.youtube.com/playlist|youtube.com/playlist)(:[0-9]+)?(.*)', re.I)


@hook.regex(*ytpl_re)
def ytplaylist_url(match, bot=None):
    if not yt_load_dev_key(bot):
        return
    location = match.group(4).split("=")[-1]
    json = requests.get(playlist_api_url, params={"id": location, "key": yt_dev_key}).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return 'Error looking up playlist.'

    data = json['items']
    snippet = data[0]['snippet']
    content_details = data[0]['contentDetails']

    title = snippet['title']
    author = snippet['channelTitle']
    num_videos = int(content_details['itemCount'])
    count_videos = ' - \x02{:,}\x02 video{}'.format(num_videos, "s"[num_videos == 1:])
    return "\x02{}\x02 {} - \x02{}\x02".format(title, count_videos, author)
