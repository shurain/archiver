import requests


class Transformer(object):
    pass

class DiffbotTransformer(Transformer):
    URL = 'https://www.diffbot.com/api/article'

    def __init__(self, token):
        self.token = token

    def extract(self, url, callback=False, html=False, dontStripAds=False, timeout=False, tags=True, comments=False, summary=True):
        args = {
            'callback': callback,
            'html': html,
            'dontStripAds': dontStripAds,
            'timeout': timeout,
            'tags': tags,
            'comments': comments,
            'summary': summary,
        }

        valid_args = {k: v for (k, v) in args.iteritems() if v}
        url = self.URL + '?token={}&url={}'.format(self.token, url)
        options = '&'.join((k for k in valid_args))
        if options:
            url += '&' + options

        response = requests.get(url)
        return response.content