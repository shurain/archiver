#!/usr/bin/env python
import requests


class Archive(object):
    def __init__(self, link):
        self.link = link

        # XXX Could allowing redirects become a problem?
        self.response = requests.head(self.link, allow_redirects=True)

    def content_type(self):
        return self.response.headers['content-type']

    def file_extension(self):
        #FIXME check for url encoded data (periods, etc.)
        pass

    def magic_number(self):
        #FIXME check the magic number.
        #PDF begins with "%PDF"
        pass

    def fetch(self):
        # FIXME what better ways for this?
        # Assuming response is HEAD
        if self.response.request.method == 'HEAD':
            # XXX time consuming
            self.response = requests.get(self.response.url)
            return self.response.content


if __name__ == '__main__':
    #normal pdf
    pdf = "http://www.valvesoftware.com/publications/2009/ai_systems_of_l4d_mike_booth.pdf"

    #redirection occurs
    redirection = "http://nvidia.com/content/PDF/sc_2010/CUDA_Tutorial/SC10_Accelerating_GPU_Computation_Through_Mixed-Precision_Methods.pdf"

    #returns content type of "text/html; charset=EUC-KR" on HEAD while returning content type of "application/pdf" on GET
    #It doesn't, anymore. Accessing it must have changed it.
    malformed_return = 'http://theory.snu.ac.kr/mediawiki/images/d/d5/%ED%95%9C%EA%B8%80_edit_distance.pdf'
