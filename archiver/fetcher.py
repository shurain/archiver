# -*- coding: utf-8 -*-

"""
A module for fetching resource indicated by a URL.
"""

import requests
import logging


class URLFetcher(object):
    SIZELIMIT = 100 * 2**10 * 2**10  # 100M

    def __init__(self, url):
        self.url = url
        # XXX Could allowing redirects become a problem?
        # XXX maybe stream might timeout?
        self.response = requests.get(url, allow_redirects=True, stream=True, verify=False)

    @property
    def content_type(self):
        if 'content-type' in self.response.headers:
            return self.response.headers['content-type'].split(';')[0].strip()
        else:
            return None

    def is_image(self):
        if self.content_type in ['image/gif', 'image/png', 'image/jpeg']:
            #FIXME supporting more image types?
            return True
        elif self.response.content[:8] == '\x89PNG\r\n\x1a\n':
            #png magic number
            # map(hex, map(ord, self.response.content[:8])) == ['0x89', '0x50', '0x4e', '0x47', '0xd', '0xa', '0x1a', '0xa']
            return True
        elif self.response.content[:2] == '\xff\xd8':
            #jpeg magic number
            return True
        elif self.response.content[:6] in ("GIF89a", "GIF87a"):
            return True
        else:
            return False

    def image_content_type(self):
        """Returns the content type of the image.
        This method assumes that you have already confirmed that the resource is an image.
        Returns None when no content type matches.
        """
        if self.content_type in ['image/gif', 'image/png', 'image/jpeg']:
            return self.content_type
        elif self.response.content[:8] == '\x89PNG\r\n\x1a\n':
            return 'image/png'
        elif self.response.content[:2] == '\xff\xd8':
            return 'image/jpeg'
        elif self.response.content[:6] in ("GIF89a", "GIF87a"):
            return 'image/gif'


    def is_PDF(self):
        """Check if the resource is a PDF document.

        It will try to check the content-type of the response header,
        and peep the content for magic number indicating the content type.
        """
        if self.content_type == 'application/pdf':
            return True
        if self.response.content[:4] == '%PDF':
            return True
        else:
            return False

    def is_HTML(self):
        """Check if the resource is a HTML document.

        Just checks the content-type of the response header.
        """
        if self.content_type == 'text/html':
            return True
        else:
            return False

    def is_text(self):
        """Check if the resource is a plain text.

        Just checks the content-type of the response header.
        """
        if self.content_type == 'text/plain':
            return True
        else:
            return False


    def fetch(self):
        """Fetch the resource content.

        Has a guard to check if the content exceeds the size limit.
        Size limit can be overrided by settings the SIZELIMIT variable.
        """
        if 'content-length' not in self.response.headers:
            logging.info("No content-length header, proceeding anyway.")
        elif int(self.response.headers['content-length']) > self.SIZELIMIT:
            #FIXME create a specific exception
            raise Exception("File too large")

        return self.response.content
