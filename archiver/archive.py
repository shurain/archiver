#!/usr/bin/env python
from .source import PinboardSource
from .sink import EvernoteSink
from .fetcher import URLFetcher
from .transformer import DiffbotTransformer
from .item import HTMLItem, PDFItem
from .settings import PINBOARD_API_TOKEN, EVERNOTE_DEVELOPER_TOKEN, DIFFBOT_TOKEN


def main():
    pinboard = PinboardSource(PINBOARD_API_TOKEN)
    bookmarks = pinboard.latest()
    
    diffbot = DiffbotTransformer(DIFFBOT_TOKEN)

    items = []
    for bookmark in bookmarks:
        data = URLFetcher(bookmark.url)

        if data.is_PDF():
            item = PDFItem(data)
        elif data.is_HTML():
            item = HTMLItem(data)
            item.meta = diffbot.extract(item)

        items.append(item)

    evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN)
    for item in items:
        evernote.push(item)


if __name__ == '__main__':
    main()