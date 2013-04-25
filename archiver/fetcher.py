import requests


class URLFetcher(object):
    SIZELIMIT = 100 * 2**10 * 2**10  # 100M

    def __init__(self, url):
        self.url = url
        # XXX Could allowing redirects become a problem?
        # XXX maybe stream might timeout?
        self.response = requests.get(url, allow_redirects=True, stream=True)

    def content_type(self):
        return self.response.headers['content-type']

    def is_PDF(self):
        if self.response.headers['content-type'] == 'application/pdf':
            return True
        if self.response.content[:4] == '%PDF':
            return True
        else:
            return False

    def fetch(self):
        if self.response.headers['content-length'] > SIZELIMIT:
            #FIXME create a specific exception
            raise Exception("File too large")
        return self.response.content
