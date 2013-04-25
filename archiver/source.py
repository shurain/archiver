try:
    from lxml import etree
except ImportError:
    # Python 2.5
    import xml.etree.cElementTree as etree
import requests
from item import PinboardItem


class Source(object):
    pass

class PinboardSource(Source):
    URL = "https://api.pinboard.in/v1/"

    def __init__(self, token):
        self.token = token

    def grab_xml(self, url):
        r = requests.get(url)
        return r.content

    def parse_xml(self, xml):
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
        pass

    def fetch_all(self):
        pass

    def fetch(self):
        #FIXME
        return []