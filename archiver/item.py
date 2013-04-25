class Item(object):
    pass

class PinboardItem(Item):
    def __init__(self, url, title, time, body='', tags=''):
        self.url = url
        self.title = title
        self.time = time
        self.body = body
        self.tags = tags

    def __str__(self):
        return self.url

class PDFItem(Item):
    def __init__(self, data):
        #data is from URLFetch
        pass

class HTMLItem(Item):
    def __init__(self, data):
        #data is from URLFetch
        pass