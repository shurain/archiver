#!/usr/bin/env python
try:
    import simplejson as json
except ImportError:
    import json
from lxml import etree
import requests
import logging

from archiver.source import PinboardSource
from archiver.sink import EvernoteSink
from archiver.fetcher import URLFetcher
from archiver.transformer import DiffbotTransformer
from archiver.item import HTMLItem, PDFItem
from archiver.settings import PINBOARD_API_TOKEN, EVERNOTE_DEVELOPER_TOKEN, DIFFBOT_TOKEN
from archiver.enml import html2enml


def main():
    pinboard = PinboardSource(PINBOARD_API_TOKEN)
    datestr = '2013-04-26T00:00:00Z'

    bookmarks = pinboard.fetch_from_date(datestr)

    diffbot = DiffbotTransformer(DIFFBOT_TOKEN)

    items = []
    for bookmark in bookmarks:
        try:
            resource = URLFetcher(bookmark.url)
        except requests.exceptions.ConnectionError as e:
            logging.error("Failed to fetch resource at {} due to {}".format(bookmark.url, e))
            continue

        if resource.is_PDF():
            item = PDFItem.from_pinboard_item(bookmark)
            item.content = 'PDF CONTENT'
            # item.content = resource.fetch()
        elif resource.is_HTML():
            item = HTMLItem.from_pinboard_item(bookmark)
            json_result = diffbot.extract(item.url, html=True)
            json_object = json.loads(json_result)
            try:
                item.content = html2enml(json_object['html'])
            except (etree.XMLSyntaxError, KeyError) as e:
                # cannot parse
                # try plaintext
                logging.error("Failed to parse {}".format(json_object['url']))
                logging.error("Reason: {}".format(e))
                logging.error("Degrading to using text summary")
                item.content = json_object['text']
                # Check for default tags
                if not item.tags:
                    # FIXME check for excluded tags
                    # FIXME fetch tags from diffbot
                    pass


        items.append(item)

    evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN)
    for item in items:
        evernote.push(item)


if __name__ == '__main__':
    main()