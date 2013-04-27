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

    pinboard = PinboardSource(PINBOARD_API_TOKEN)
    datestr = res[1]  # 0 contains the index "1"

    logging.info("Fetching data from {}".format(datestr))

    bookmarks = pinboard.fetch_from_date(datestr)
    # bookmarks = pinboard.fetch_from_url("http://i.imgur.com/4n92M.jpg")

    # Hold the data fetch time
    c.execute("UPDATE pinboard set last_updated = ? where id = 1", (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),))

    diffbot = DiffbotTransformer(DIFFBOT_TOKEN)

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
            if not item.tags or (item.tags.lower() == 'unread' and len(item.tags.split()) == 1):
                # FIXME seemingly random criteria for checking tags
                # autotag tells that this was autotagged.
                item.tags = 'autotag ' + ' '.join(('_'.join(x.split()) for x in json_object['tags']))  # diffbot tags

        items.append(item)

    evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN)
    for item in items:
        evernote.push(item)

    # Commit the holded timestamp
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()