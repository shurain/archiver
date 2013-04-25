#!/usr/bin/env python
import unittest
import mock
from datetime import datetime

from archiver.item import PinboardItem
from archiver.source import PinboardSource
from archiver import sink
from archiver import transformer
from archiver import fetcher
from archiver.settings import *


class TestPinboardSource(unittest.TestCase):
    def setUp(self):
        self.PINBOARD_API_TOKEN = PINBOARD_API_TOKEN
        self.pin = PinboardSource(self.PINBOARD_API_TOKEN)
        self.xml = """<?xml version="1.0" encoding="UTF-8" ?>\n<posts user="shurain" dt="2013-04-25T08:42:48Z">\n    <post href="http://estima.wordpress.com/2013/04/25/axon" time="2013-04-25T08:42:48Z" description="\xeb\xaa\xa8\xeb\x93\xa0 \xea\xb2\x83\xec\x9d\x84 \xeb\x8b\xa4 \xec\xb0\x8d\xeb\x8a\x94 \xea\xb2\xbd\xec\xb0\xb0\xec\x9d\x98 \xec\x86\x8c\xed\x98\x95\xeb\xb9\x84\xeb\x94\x94\xec\x98\xa4\xec\xb9\xb4\xeb\xa9\x94\xeb\x9d\xbc-\xec\x97\x91\xec\x86\x90 \xed\x94\x8c\xeb\xa0\x89\xec\x8a\xa4 | \xec\x97\x90\xec\x8a\xa4\xed\x8b\xb0\xeb\xa7\x88\xec\x9d\x98 \xec\x9d\xb8\xed\x84\xb0\xeb\x84\xb7\xec\x9d\xb4\xec\x95\xbc\xea\xb8\xb0" extended="" tag="police camera" hash="6c0309ae794a2727a048e5e1f9e1876b"  shared="no"  />\n    <post href="http://theory.snu.ac.kr/mediawiki/images/d/d5/%ED%95%9C%EA%B8%80_edit_distance.pdf" time="2013-04-25T07:16:33Z" description="\xed\x95\x9c\xea\xb8\x80\xec\x97\x90 \xeb\x8c\x80\xed\x95\x9c \xed\x8e\xb8\xec\xa7\x91\xea\xb1\xb0\xeb\xa6\xac \xeb\xac\xb8\xec\xa0\x9c" extended="" tag="algorithm distance profanity_filtering" hash="fa9322de8bdcb82e6cadcd4b0dec4bdb"  shared="no"  />\n    <post href="https://github.com/kevinschaul/binify" time="2013-04-25T06:02:07Z" description="kevinschaul/binify \xc2\xb7 GitHub" extended="" tag="repo visualization hexagon_binning" hash="f378fa02b0a9965bfdea858e0985b220"  shared="no"  />\n    <post href="http://techcrunch.com/2013/04/22/want-to-raise-a-million-bucks-heres-what-youll-need/" time="2013-04-25T05:43:50Z" description="Want To Raise A Million Bucks? Here\xe2\x80\x99s What You\xe2\x80\x99ll Need | TechCrunch" extended="" tag="startup investment" hash="d76e2079690d7c1c1020805a761e7a76"  shared="no"  />\n    <post href="http://mobile.reuters.com/article/idUSBRE93N06E20130424?irpc=932" time="2013-04-25T01:35:21Z" description="Analysis: Sleeping ad giant Amazon finally stirs" extended="" tag="amazon advertisement" hash="1c4b82b4331a246a278445fc6f7b4bb1"  shared="no"  />\n    <post href="http://qiao.github.io/PathFinding.js/visual/" time="2013-04-25T01:32:24Z" description="PathFinding.js" extended="" tag="path_finding ai" hash="388e9fca89029606b761a602359224e7"  shared="no"  />\n    <post href="http://kevinschaul.com/2013/04/18/introducing-binify?buffer_share=55493" time="2013-04-25T01:30:15Z" description="Introducing: Binify | Kevin Schaul" extended="" tag="visualization hexagon_binning" hash="f5c2d58817398126a21cfa3d8c3cd115"  shared="no"  />\n    <post href="http://www.valvesoftware.com/publications/2009/ai_systems_of_l4d_mike_booth.pdf" time="2013-04-25T00:30:05Z" description="The AI Systems of Left 4 Dead" extended="" tag="pdf slides game ai" hash="3004f5a94d870a0ddfcfc639981262a6"  shared="no"  />\n    <post href="http://blogs.hbr.org/bregman/2010/05/how-and-why-to-stop-multitaski.html?buffer_share=7f1b8" time="2013-04-24T16:31:06Z" description="How (and Why) to Stop Multitasking - Peter Bregman - Harvard Business Revie" extended="" tag="productivity multitasking" hash="9afea76d5d6e758375522b6c323d2959"  shared="no"  />\n    <post href="http://pyvideo.org/video/1717/effective-django-0" time="2013-04-24T16:28:59Z" description="pyvideo.org - Effective Django" extended="" tag="video pycon_2013 django" hash="97397c0b2fdc9fd2867508c1a4597f12"  shared="no"  />\n    <post href="http://pyvideo.org/video/1654/a-beginners-introduction-to-pydata-how-to-build" time="2013-04-24T16:13:39Z" description="pyvideo.org - A beginner\'s introduction to Pydata: how to build a minimal r" extended="" tag="video pycon_2013" hash="f5f02efb0d02c7221693b86fce05331c"  shared="no"  />\n    <post href="https://developer.nvidia.com/content/cuda-pro-tip-write-flexible-kernels-grid-stride-loops" time="2013-04-24T14:56:08Z" description="CUDA Pro Tip: Write Flexible Kernels with Grid-Stride Loops" extended="" tag="cuda gpgpu" hash="8b1b715837eba081166c23261a8fddbf"  shared="no"  />\n    <post href="http://arxiv.org/abs/1304.6257" time="2013-04-24T14:55:18Z" description="An Evolutionary Algorithm Approach to Link Prediction in Dynamic Social Net" extended="" tag="paper link_prediction" hash="dfd9cd529351e8916f0915bb692ce728"  shared="no"  />\n    <post href="http://arxiv.org/abs/1304.6181" time="2013-04-24T14:54:19Z" description="Evaluating Web Content Quality via Multi-scale Features. (arXiv:1304.6181v1" extended="" tag="paper" hash="3626f3ae8ab2a8fa85df66f7673c993a"  shared="no"  />\n    <post href="https://github.com/bponsler/pysiriproxy" time="2013-04-24T14:44:57Z" description="bponsler/pysiriproxy \xc2\xb7 GitHub" extended="Port of SiriProxy from Ruby to Python." tag="repo" hash="a5ba89a718d125fbd69dbf7fb5a2ef20"  shared="no"  />\n</posts>\n\t"""

    def test_connection(self):
        url = self.pin.URL + 'posts/recent?auth_token=' + self.PINBOARD_API_TOKEN
        with mock.patch('requests.get') as requests_get:
            self.pin.grab_xml(url)
            self.assertTrue(requests_get.called)

    def test_xml_parsing(self):
        result = self.pin.parse_xml(self.xml)
        self.assertEquals(str(result[0]), "http://estima.wordpress.com/2013/04/25/axon")

    def test_fetch_from_date(self):
        with mock.patch('requests.get') as requests_get:
            requests_get.return_value.content = self.xml
            datestr = '2013-04-25T00:00:00Z'

            self.pin.fetch_from_date(datestr)
            requests_get.assert_called_with(
                'https://api.pinboard.in/v1/posts/all?auth_token={}&fromdt={}'.format(self.PINBOARD_API_TOKEN, datestr))

class TestEvernoteSink(unittest.TestCase):
    pass

class TestDiffbotMiddleware(unittest.TestCase):
    pass

class TestPDFFetcher(unittest.TestCase):
    pass

class TestHTMLItem(unittest.TestCase):
    pass

class TestPDFItem(unittest.TestCase):
    pass

class TestArchive(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()