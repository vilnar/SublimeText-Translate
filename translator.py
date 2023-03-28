import json

from urllib import parse, request
from collections import OrderedDict

from os.path import dirname, realpath
PLUGINPATH = dirname(realpath(__file__))

class Translate(object):
    error_codes = {
        501: "ERR_SERVICE_NOT_AVAIBLE_TRY_AGAIN_OR_USE_PROXY",
        503: "ERR_VALUE_ERROR",
        504: "ERR_PROXY_NOT_SPECIFIED",
    }

    def __init__(self, source_lang='auto', target_lang='en'):
        self.cache = {
            'languages': None, 
        }
        self.api_urls = {
            'translate': 'https://translate.googleapis.com/translate_a/single?client=gtx', #&ie=UTF-8&oe=UTF-8
        }
        if not source_lang:
            source_lang = 'auto'
        if not target_lang:
            target_lang = 'en'
        self.source = source_lang
        self.target = target_lang

    @property
    def langs(self, cache=True):
        try:
            if not self.cache['languages'] and cache:
                with open(PLUGINPATH+'/supported_languages.json') as f:
                  _data = f.read()
                _languages = json.loads(_data, object_pairs_hook=OrderedDict)
                print('[Google] translate, supported {0} languages.'.format(len(_languages)))
                self.cache['languages'] = _languages
        except IOError:
            raise GoogleTranslateException(self.error_codes[501])
        except ValueError:
            raise GoogleTranslateException(self.error_codes[503])
        return self.cache['languages']

    def GoogleTranslate(self, text, source_lang='', target_lang=''):
        if not source_lang:
            source_lang = self.source
        if not target_lang:
            target_lang = self.target

        API_URL = self.api_urls['translate']
        _text = parse.quote(text.encode("utf-8"))
        _url  = "{0}&sl={1}&tl={2}&dt=t&q={3}".format(API_URL, source_lang, target_lang, _text)
        # print('GoogleTranslate: sl {0}, tl {1}, url {2}'.format(source_lang, target_lang, _url))
        _data = request.urlopen(_url).read()
        _obj = json.loads(str(_data,'utf-8'))
        result = []
        for s in _obj[0]:
            result.append(s[0])
        return "".join(result)



class GoogleTranslateException(object):
    def __init__(self, exception):
        print(exception)
        sublime.active_window().run_command("show_panel", {"panel": "console"})