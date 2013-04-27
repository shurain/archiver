#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json
from lxml import etree
import requests
import logging
import sqlite3
from datetime import datetime

from archiver.source import PinboardSource
from archiver.sink import EvernoteSink
from archiver.fetcher import URLFetcher
from archiver.transformer import DiffbotTransformer
from archiver.item import Item, HTMLItem, PDFItem, ImageItem
from archiver.settings import PINBOARD_API_TOKEN, EVERNOTE_DEVELOPER_TOKEN, DIFFBOT_TOKEN, DATABASE_PATH
from archiver.enml import html2enml

logging.basicConfig(level=logging.DEBUG)


def main():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM pinboard")
    except sqlite3.OperationalError as e:
        # no such table
        logging.warn(e)
        c.execute("CREATE TABLE pinboard (id INTEGER PRIMARY KEY, last_updated TEXT)")

    c.execute("SELECT * FROM pinboard")
    res = c.fetchone()

    if res is None:
        c.execute("INSERT INTO pinboard VALUES (NULL, ?)", ('1970-01-01T00:00:00Z', ))  # beginning of time
        conn.commit()
        c.execute("SELECT * FROM pinboard")
        res = c.fetchone()
    pid, datestr = res  # 0 contains the index "1"

    pinboard = PinboardSource(PINBOARD_API_TOKEN)
    diffbot = DiffbotTransformer(DIFFBOT_TOKEN)
    evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN)

    logging.info("Fetching data from {}".format(datestr))

    bookmarks = pinboard.fetch_from_date(datestr)
    # bookmarks = pinboard.fetch_from_url("http://i.imgur.com/4n92M.jpg")

    items = []
    for bookmark in reversed(bookmarks):
        logging.info("Handling : {}".format(bookmark.url))
        try:
            resource = URLFetcher(bookmark.url)
        except requests.exceptions.ConnectionError as e:
            logging.error("Failed to fetch resource at {}".format(bookmark.url))
            logging.error("Reason: {}".format(e))
            continue

        item = Item()
        if resource.is_PDF():
            item = PDFItem.from_pinboard_item(bookmark)
            item.content = resource.fetch()  #FIXME this could take very long. Need a way to address this problem.
        elif resource.is_image():
            item = ImageItem.from_pinboard_item(bookmark)
            item.content_type = resource.content_type
            item.content = resource.fetch()
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
            # FIXME seemingly random criteria for checking tags
            if not item.tags or (item.tags.lower() == 'unread' and len(item.tags.split()) == 1):
                # Diffbot will not contain tags key even if explicitly told to return tags if it does not find any
                if 'tags' in json_object:
                    # autotag tells that this was autotagged.
                    item.tags = 'autotag ' + ' '.join(('_'.join(x.split()) for x in json_object['tags']))  # diffbot tags

        evernote.push(item)
        c.execute("UPDATE pinboard set last_updated = ? where id = 1", (item.time,))
        conn.commit()

        # items.append(item)

    # for item in items:
    #     evernote.push(item)

    # Hold the data fetch time
    # Commit the holded timestamp
    conn.close()

if __name__ == '__main__':
    main()