# -*- coding: utf-8 -*-

class Item(object):
    pass

class PinboardItem(Item):
    def __init__(self, url, title, time, body='', tags=''):
        self.url = url
        self.title = title
        self.time = time
        self.body = body
        self.tags = tags
        self.itemtype = 'pinboard'

    def __str__(self):
        return self.url

class ImageItem(Item):
    @classmethod
    def from_pinboard_item(cls, item):
        imageitem = cls()
        imageitem.url = item.url
        imageitem.title = item.title
        imageitem.time = item.time
        imageitem.body = item.body
        imageitem.tags = item.tags
        imageitem.itemtype = 'image'
        return imageitem 

class PDFItem(Item):
    @classmethod
    def from_pinboard_item(cls, item):
        pdfitem = cls()
        pdfitem.url = item.url
        pdfitem.title = item.title
        pdfitem.time = item.time
        pdfitem.body = item.body
        pdfitem.tags = item.tags
        pdfitem.itemtype = 'PDF'
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
        htmlitem.itemtype = 'HTML'
        return htmlitem 

class TextItem(Item):
    @classmethod
    def from_pinboard_item(cls, item):
        textitem = cls()
        textitem.url = item.url
        textitem.title = item.title
        textitem.time = item.time
        textitem.body = item.body
        textitem.tags = item.tags
        textitem.itemtype = 'text'
        return textitem 
