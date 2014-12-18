from urllib import urlencode
from urllib2 import urlopen
import md5
from util import hook
import socket

def _utils_string_at_index(strings, index):
    if len(strings) > index:
        return strings[index]
    else:
        return ''
    
cb_url = 'http://www.cleverbot.com/webservicemin'

class CleverBot(object):
    def __init__(self, url=cb_url, end_index=35):
        self.url = url
        self.end_index = end_index
        self.vars = {}
        self.vars['start'] = 'y'
        self.vars['icognoid'] = 'wsf'
        self.vars['fno'] = '0'
        self.vars['sub'] = 'Say'
        self.vars['islearning'] = '1'
        self.vars['cleanslate'] = 'false'
        
    def digester(self):
        self.vars['stimulus'] = self.thought
        data = urlencode(self.vars)
        data_to_digest = data[9:self.end_index]
        data_digest = md5.new(data_to_digest).hexdigest()
        self.data = data + '&icognocheck=' + data_digest
        
    def get_response(self):
        try:
            url_response = urlopen(self.url, self.data).read()
        except socket.timeout:  # just try again, it should work
            try:
                url_response = urlopen(self.url, self.data).read()
            except socket.timeout:
                return "timeout error. sorry :/"
        self.response_values = url_response.split('\r')
        
    def get_vars(self):
        #self.vars['??'] = _utils_string_at_index(self.response_values, 0)
        self.vars['sessionid'] = _utils_string_at_index(self.response_values, 1)
        self.vars['logurl'] = _utils_string_at_index(self.response_values, 2)
        self.vars['vText8'] = _utils_string_at_index(self.response_values, 3)
        self.vars['vText7'] = _utils_string_at_index(self.response_values, 4)
        self.vars['vText6'] = _utils_string_at_index(self.response_values, 5)
        self.vars['vText5'] = _utils_string_at_index(self.response_values, 6)
        self.vars['vText4'] = _utils_string_at_index(self.response_values, 7)
        self.vars['vText3'] = _utils_string_at_index(self.response_values, 8)
        self.vars['vText2'] = _utils_string_at_index(self.response_values, 9)
        self.vars['prevref'] = _utils_string_at_index(self.response_values, 10)
        #self.vars['??'] = _utils_string_at_index(self.response_values, 11)
        self.vars['emotionalhistory'] = _utils_string_at_index(self.response_values, 12)
        self.vars['ttsLocMP3'] = _utils_string_at_index(self.response_values, 13)
        self.vars['ttsLocTXT'] = _utils_string_at_index(self.response_values, 14)
        self.vars['ttsLocTXT3'] = _utils_string_at_index(self.response_values, 15)
        self.vars['ttsText'] = _utils_string_at_index(self.response_values, 16)
        self.vars['lineRef'] = _utils_string_at_index(self.response_values, 17)
        self.vars['lineURL'] = _utils_string_at_index(self.response_values, 18)
        self.vars['linePOST'] = _utils_string_at_index(self.response_values, 19)
        self.vars['lineChoices'] = _utils_string_at_index(self.response_values, 20)
        self.vars['lineChoicesAbbrev'] = _utils_string_at_index(self.response_values, 21)
        self.vars['typingData'] = _utils_string_at_index(self.response_values, 22)
        self.vars['divert'] = _utils_string_at_index(self.response_values, 23)
        
        self.reply = self.vars['ttsText']
        
    def get_reply(self, thought):
        self.thought = thought
        self.digester()
        blah = self.get_response()
        if blah:
            return blah
        self.get_vars()
        
        return self.reply
    
@hook.command("cb")
@hook.command("ai")
def cleverbot(inp, reply=None):
    cb = CleverBot()
    message = cb.get_reply(inp)
    reply(message)

@hook.event('PRIVMSG')
def cb(inp, reply=None, bot=None):
    if inp[1][:8].lower() in ['slimbot:', 'slimbot,', 'thlgbot,', 'thlgbot:']:
        inp = inp[1][8:].strip()
        for plug in bot.plugs['command']:
            if plug[1]['name'].lower().startswith(inp.split(' ')[0].lower()):
                return
        cb = CleverBot()
        message = cb.get_reply(inp)
        reply(message)
    
if __name__ == '__main__':
    cleverbot = CleverBot()
    print cleverbot.think_thought("hello")
