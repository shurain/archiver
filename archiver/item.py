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
    @classmethod
    def from_pinboard_item(cls, item):
        pdfitem = cls()
        pdfitem.url = item.url
        pdfitem.title = item.title
        pdfitem.time = item.time
        pdfitem.body = item.body
        pdfitem.tags = item.tags
        return pdfitem

class HTMLItem(Item):
    @classmethod
    def from_pinboard_item(cls, item):
        htmlitem = cls()
        htmlitem.url = item.url
        htmlitem.title = item.title
        htmlitem.time = item.time
        htmlitem.body = item.body
        htmlitem.tags = item.tags
        return htmlitem 
