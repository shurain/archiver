try:
    from lxml import etree
except ImportError:
    # Python 2.5
    import xml.etree.cElementTree as etree
import requests
from datetime import datetime

from item import PinboardItem


class Source(object):
    pass

class PinboardSource(Source):
    """Pinboard (https://pinboard.in/) data source.
    Fetches bookmarks from Pinboard.
    """

    URL = "https://api.pinboard.in/v1/"

    def __init__(self, token):
        self.token = token

    def grab_xml(self, url):
        """Given URL string, fetch the content and return it."""
        r = requests.get(url)
        return r.content

    def parse_xml(self, xml):
        """Given XML string, parse it and return a list of PinboardItem."""
        root = etree.fromstring(xml)
        item_list = []
        for post in root.iterchildren():
            url = post.get('href')
            title = post.get('description')
            time = post.get('time')
            body = post.get('extended')
            tags = post.get('tag')

            item = PinboardItem(url=url, title=title, body=body, tags=tags, time=time)
            item_list.append(item)

        return item_list

    def fetch_from_date(self, datestr):
        """Fetch the bookmarks after the given date string.
        UTC timestamp is used for date string.

        datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        """
        url = self.URL + 'posts/all?auth_token={}&fromdt={}'.format(self.token, datestr)
        return self.parse_xml(self.grab_xml(url))

    def fetch_all(self):
        pass

    def fetch(self):
        #FIXME
        return []