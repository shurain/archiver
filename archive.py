#!/usr/bin/env python
try:
    import simplejson as json
except ImportError:
    import json

from archiver.source import PinboardSource
from archiver.sink import EvernoteSink
from archiver.fetcher import URLFetcher
from archiver.transformer import DiffbotTransformer
from archiver.item import HTMLItem, PDFItem
from archiver.settings import PINBOARD_API_TOKEN, EVERNOTE_DEVELOPER_TOKEN, DIFFBOT_TOKEN


def main():
    pinboard = PinboardSource(PINBOARD_API_TOKEN)
    datestr = '2013-04-25T00:00:00Z'

    bookmarks = pinboard.fetch_from_date(datestr)

    diffbot = DiffbotTransformer(DIFFBOT_TOKEN)

    items = []
    for bookmark in bookmarks:
        resource = URLFetcher(bookmark.url)

        if resource.is_PDF():
            item = PDFItem.from_pinboard_item(bookmark)
            item.content = resource.fetch()
        elif resource.is_HTML():
            item = HTMLItem.from_pinboard_item(bookmark)
            json_result = diffbot.extract(item.url, html=True)
            json_object = json.loads(json_result)
            item.content = json_object['html']

        items.append(item)

    # evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN)
    for item in items:
        print item.content[:20]
    #     evernote.push(item)


if __name__ == '__main__':
    main()