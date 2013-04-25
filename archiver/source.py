class Source(object):
    pass

class PinboardSource(Source):
    URL = "https://api.pinboard.in/v1/"

    def __init__(self, token):
        self.token = token

    def fetch(self):
        #FIXME
        return []