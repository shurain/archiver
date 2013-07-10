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
import socket

from evernote.edam.error.ttypes import EDAMUserException

from archiver.source import PinboardSource
from archiver.sink import EvernoteSink
from archiver.fetcher import URLFetcher
from archiver.transformer import DiffbotTransformer
from archiver.item import Item, HTMLItem, PDFItem, ImageItem, TextItem
from archiver.settings import PINBOARD_API_TOKEN, EVERNOTE_DEVELOPER_TOKEN, DIFFBOT_TOKEN, DATABASE_PATH
from archiver.enml import html2enml
from archiver.database import PinboardDatabase

logging.basicConfig(level=logging.INFO)


def main():
    pinboard_db = PinboardDatabase()
    datestr = pinboard_db.last_updated

    pinboard = PinboardSource(PINBOARD_API_TOKEN)
    diffbot = DiffbotTransformer(DIFFBOT_TOKEN)
    evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN)

    logging.info("Fetching data from {}".format(datestr))

    bookmarks = pinboard.fetch_from_date(datestr)
    # bookmarks = pinboard.fetch_from_url("http://i.imgur.com/4n92M.jpg")
    # bookmarks = pinboard.fetch_from_url("http://neoocean.net/blog/i/entry/%EB%B2%94%EC%A3%84%EC%97%90-%EB%8C%80%ED%95%9C-%ED%8B%80%EB%A6%B0-%EC%98%88%EC%B8%A1#_post_2057")
    # bookmarks = pinboard.fetch_from_url("http://nullmodel.egloos.com/3425248")
    # bookmarks = pinboard.fetch_from_url("http://www.daniel-lemire.com/blog/archives/2010/11/02/how-do-search-engines-handle-special-characters-should-you-care/")
    # bookmarks = pinboard.fetch_from_url("http://www.1011ltd.com/web/blog/post/evolving_pid")  # no content type returned

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
            item.content_type = resource.image_content_type()
            item.content = resource.fetch()
        elif resource.is_HTML() or resource.is_text():
            if resource.is_HTML():
                item = HTMLItem.from_pinboard_item(bookmark)
                json_result = diffbot.extract(item.url, html=True)
                try:
                    json_object = json.loads(json_result)
                except json.scanner.JSONDecodeError:
                    logging.error("Unable to decode JSON for resource at : {}".format(bookmark.url))
                    continue

                if 'error' in json_object:
                    logging.error("Failed to fetch resource at {}".format(item.url))
                    logging.error(u"Reason: {}".format(json_object['error']))
                    continue

                if 'statusCode' in json_object:
                    if json_object['statusCode'] == 500:
                        logging.error("Failed to fetch resource at {}".format(item.url))
                        logging.error(u"Reason: {}".format(json_object['message']))
                        continue

                if 'html' in json_object:
                    item.content = html2enml(json_object['html'])
                else:
                    # try plaintext
                    if 'text' not in json_object:
                        logging.error("Failed to fetch HTML document at all: {}".format(item.url))
                        continue
                    logging.warn("Failed to fetch HTML document for {}".format(item.url))
                    logging.warn("Degrading to using text summary")
                    item.content = html2enml(json_object['text'])
            else:
                item = TextItem.from_pinboard_item(bookmark)
                json_result = diffbot.extract(item.url, html=True)
                try:
                    json_object = json.loads(json_result)
                except json.scanner.JSONDecodeError:
                    logging.error("Unable to decode JSON for resource at : {}".format(bookmark.url))
                    continue

                # resource is plain text
                contents = resource.fetch().split('\n\n')
                data = "<div>"
                for content in contents:
                    data += ''.join(['<div>' + body + '</div>' for body in content.split('\n')])
                    data += "<div><br /></div>"
                data += "</div>"

                item.content = html2enml(data)

            # Check for default tags
            # FIXME seemingly random criteria for checking tags
            if not item.tags or (item.tags.lower() == 'unread' and len(item.tags.split()) == 1):
                # Diffbot will not contain tags key even if explicitly told to return tags if it does not find any
                if 'tags' in json_object:
                    # autotag tells that this was autotagged.
                    # Evernote cannot handle tags with commas.
                    tags = 'autotag ' + ' '.join(('_'.join(x.replace(',','').split()) for x in json_object['tags']))  # diffbot tags
                    item.tags = tags.encode('utf-8', 'xmlcharrefreplace')

        else:
            logging.error("Unknown content-type of {}".format(resource.content_type))
            continue

        try:
            evernote.push(item)
        except socket.error as e:
            logging.error("Socket error: {}".format(e))
            continue
        except EDAMUserException as e:
            logging.error("Unrecognized evernote type: {}".format(e))
            continue

        pinboard_db.last_updated = item.time

    pinboard_db.close()


if __name__ == '__main__':
    main()
