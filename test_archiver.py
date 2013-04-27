#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
from datetime import datetime
try:
    import simplejson as json
except ImportError:
    import json
from StringIO import StringIO
from lxml import etree
from itertools import chain


from archiver.item import PinboardItem, HTMLItem, PDFItem, ImageItem
from archiver.source import PinboardSource
from archiver.sink import EvernoteSink
from archiver.transformer import DiffbotTransformer
from archiver.fetcher import URLFetcher
from archiver.enml import validate_dtd, remove_prohibited_attributes, remove_prohibited_elements, html2enml
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

    def test_fetch_all(self):
        with mock.patch('requests.get') as requests_get:
            requests_get.return_value.content = self.xml

            bookmarks = self.pin.fetch_all()
            requests_get.assert_called_with(
                'https://api.pinboard.in/v1/posts/all?auth_token={}'.format(self.PINBOARD_API_TOKEN))

            self.assertEquals(bookmarks[0].url, "http://estima.wordpress.com/2013/04/25/axon")


class TestDiffbotTransformer(unittest.TestCase):
    def setUp(self):
        self.url = 'http://httpbin.org/'
        self.json_result = r"""{"tags":["Military service","Hypertext Transfer Protocol","Windows service"],"summary":"Testing an HTTP Library can become difficult sometimes.  PostBin.org is fantastic for testing POST requests, but not much else.  This exists to cover all kinds of HTTP scenarios.  Additional endpoints are being considered (e.g.  \/deflate). {\"user-agent\": \"curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3\"}","text":"Freely hosted in HTTP, HTTPS & EU flavors.\n\n\nTesting an HTTP Library can become difficult sometimes. PostBin.org is fantastic for testing POST requests, but not much else. This exists to cover all kinds of HTTP scenarios. Additional endpoints are being considered (e.g. \/deflate).\nAll endpoint responses are JSON-encoded.\nEXAMPLES\n$ curl http:\/\/httpbin.org\/ip\n{\"origin\": \"24.127.96.129\"}\n$ curl http:\/\/httpbin.org\/user-agent\n{\"user-agent\": \"curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3\"}\n$ curl http:\/\/httpbin.org\/get\n{ \"args\": {}, \"headers\": { \"Accept\": \"*\/*\", \"Connection\": \"close\", \"Content-Length\": \"\", \"Content-Type\": \"\", \"Host\": \"httpbin.org\", \"User-Agent\": \"curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3\" }, \"origin\": \"24.127.96.129\", \"url\": \"http:\/\/httpbin.org\/get\" }\n$ curl -I http:\/\/httpbin.org\/status\/418\nHTTP\/1.1 418 I'M A TEAPOT Server: nginx\/0.7.67 Date: Mon, 13 Jun 2011 04:25:38 GMT Connection: close x-more-info: http:\/\/tools.ietf.org\/html\/rfc2324 Content-Length: 135\nAUTHOR\nA Kenneth Reitz Project.\nSEE ALSO\nhttp:\/\/python-requests.org","title":"httpbin(1): HTTP Client Testing Service","type":"article","url":"http:\/\/httpbin.org\/","xpath":"\/HTML[1]\/BODY[1]\/DIV[1]"}"""
        self.json_html_result = r"""{"tags":["Military service","Hypertext Transfer Protocol","Windows service"],"summary":"Testing an HTTP Library can become difficult sometimes.  PostBin.org is fantastic for testing POST requests, but not much else.  This exists to cover all kinds of HTTP scenarios.  Additional endpoints are being considered (e.g.  \/deflate). {\"user-agent\": \"curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3\"}","text":"Freely hosted in HTTP, HTTPS & EU flavors.\n\n\nTesting an HTTP Library can become difficult sometimes. PostBin.org is fantastic for testing POST requests, but not much else. This exists to cover all kinds of HTTP scenarios. Additional endpoints are being considered (e.g. \/deflate).\nAll endpoint responses are JSON-encoded.\nEXAMPLES\n$ curl http:\/\/httpbin.org\/ip\n{\"origin\": \"24.127.96.129\"}\n$ curl http:\/\/httpbin.org\/user-agent\n{\"user-agent\": \"curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3\"}\n$ curl http:\/\/httpbin.org\/get\n{ \"args\": {}, \"headers\": { \"Accept\": \"*\/*\", \"Connection\": \"close\", \"Content-Length\": \"\", \"Content-Type\": \"\", \"Host\": \"httpbin.org\", \"User-Agent\": \"curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3\" }, \"origin\": \"24.127.96.129\", \"url\": \"http:\/\/httpbin.org\/get\" }\n$ curl -I http:\/\/httpbin.org\/status\/418\nHTTP\/1.1 418 I'M A TEAPOT Server: nginx\/0.7.67 Date: Mon, 13 Jun 2011 04:25:38 GMT Connection: close x-more-info: http:\/\/tools.ietf.org\/html\/rfc2324 Content-Length: 135\nAUTHOR\nA Kenneth Reitz Project.\nSEE ALSO\nhttp:\/\/python-requests.org","title":"httpbin(1): HTTP Client Testing Service","html":"<div><p>Freely hosted in <a href=\"http:\/\/httpbin.org\">HTTP<\/a>,\n<a href=\"https:\/\/httpbin.org\">HTTPS<\/a> &amp;\n<a href=\"http:\/\/eu.httpbin.org\">EU<\/a>\nflavors.<\/p><h2 id=\"ENDPOINTS\">ENDPOINTS<\/h2><h2 id=\"DESCRIPTION\">DESCRIPTION<\/h2><p>Testing an HTTP Library can become difficult sometimes. PostBin.org is fantastic\nfor testing POST requests, but not much else. This exists to cover all kinds of HTTP\nscenarios. Additional endpoints are being considered (e.g. <code>\/deflate<\/code>).<\/p><p>All endpoint responses are JSON-encoded.<\/p><h2 id=\"EXAMPLES\">EXAMPLES<\/h2><h3 id=\"-curl-http-httpbin-org-ip\">$ curl http:\/\/httpbin.org\/ip<\/h3><pre>&lt;code&gt;{&quot;origin&quot;: &quot;24.127.96.129&quot;}\n&lt;\/code&gt;<\/pre><h3 id=\"-curl-http-httpbin-org-user-agent\">$ curl http:\/\/httpbin.org\/user-agent<\/h3><pre>&lt;code&gt;{&quot;user-agent&quot;: &quot;curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3&quot;}\n&lt;\/code&gt;<\/pre><h3 id=\"-curl-http-httpbin-org-get\">$ curl http:\/\/httpbin.org\/get<\/h3><pre>&lt;code&gt;{\n   &quot;args&quot;: {},\n   &quot;headers&quot;: {\n      &quot;Accept&quot;: &quot;*\/*&quot;,\n      &quot;Connection&quot;: &quot;close&quot;,\n      &quot;Content-Length&quot;: &quot;&quot;,\n      &quot;Content-Type&quot;: &quot;&quot;,\n      &quot;Host&quot;: &quot;httpbin.org&quot;,\n      &quot;User-Agent&quot;: &quot;curl\/7.19.7 (universal-apple-darwin10.0) libcurl\/7.19.7 OpenSSL\/0.9.8l zlib\/1.2.3&quot;\n   },\n   &quot;origin&quot;: &quot;24.127.96.129&quot;,\n   &quot;url&quot;: &quot;http:\/\/httpbin.org\/get&quot;\n}\n&lt;\/code&gt;<\/pre><h3 id=\"-curl-I-http-httpbin-org-status-418\">$ curl -I http:\/\/httpbin.org\/status\/418<\/h3><pre>&lt;code&gt;HTTP\/1.1 418 I'M A TEAPOT\nServer: nginx\/0.7.67\nDate: Mon, 13 Jun 2011 04:25:38 GMT\nConnection: close\nx-more-info: http:\/\/tools.ietf.org\/html\/rfc2324\nContent-Length: 135\n&lt;\/code&gt;<\/pre><h2 id=\"AUTHOR\">AUTHOR<\/h2><p>A <a href=\"http:\/\/kennethreitz.com\/pages\/open-projects.html\">Kenneth Reitz<\/a>\nProject.<\/p><h2 id=\"SEE-ALSO\">SEE ALSO<\/h2><p><a data-bare-link=\"true\" href=\"http:\/\/python-requests.org\">http:\/\/python-requests.org<\/a><\/p><\/div>","type":"article","url":"http:\/\/httpbin.org\/","xpath":"\/HTML[1]\/BODY[1]\/DIV[1]"}"""
        self.diffbot = DiffbotTransformer(DIFFBOT_TOKEN)

    def test_connection(self):
        with mock.patch('requests.get') as requests_get:
            requests_get.return_value.content = self.json_result
            json_result = self.diffbot.extract(self.url)

            requests_get.assert_called_with(
                'https://www.diffbot.com/api/article?token={}&url=http://httpbin.org/&tags&summary'.format(DIFFBOT_TOKEN))

    def test_extract_body(self):
        #FIXME makes actual connection
        json_result = self.diffbot.extract(self.url)
        self.assertEquals(json_result, self.json_result)

    def test_html_connection(self):
        with mock.patch('requests.get') as requests_get:
            requests_get.return_value.content = self.json_html_result
            json_result = self.diffbot.extract(self.url, html=True)

            requests_get.assert_called_with(
                'https://www.diffbot.com/api/article?token={}&url=http://httpbin.org/&html&tags&summary'.format(DIFFBOT_TOKEN))

    def test_extract_body_html(self):
        #FIXME makes actual connection
        json_result = self.diffbot.extract(self.url, html=True)
        self.assertEquals(json_result, self.json_html_result)


class TestURLFetcher(unittest.TestCase):
    def setUp(self):
        self.url = 'http://httpbin.org/'
        self.pdf_url = 'http://httpbin.org/response-headers?Content-Type=application/pdf;%20charset=UTF-8&Server=httpbin'
        self.html_url = 'http://httpbin.org/response-headers?Content-Type=text/html;%20charset=UTF-8&Server=httpbin'

    def test_url_fetch(self):
        with mock.patch('requests.get') as requests_get:
            resource = URLFetcher(self.url)
            self.assertTrue(requests_get.called)

    def test_pdf_fetch(self):
        #FIXME makes actual connection
        resource = URLFetcher(self.pdf_url)
        self.assertTrue(resource.is_PDF())

    def test_html_fetch(self):
        #FIXME makes actual connection
        resource = URLFetcher(self.html_url)
        self.assertFalse(resource.is_PDF())
        self.assertTrue(resource.is_HTML())

    def test_size_limit(self):
        #FIXME makes actual connection
        resource = URLFetcher(self.pdf_url)
        # This raises error if we forgot to cast the 'content-length' header to int
        # '104' > 100 * 2**10 * 2**10
        resource.fetch()


class TestItem(unittest.TestCase):
    def setUp(self):
        self.image_pinboarditem = PinboardItem(url="http://i.imgur.com/4n92M.jpg", title="Untitled (http://i.imgur.com/4n92M.jpg)", time='2012-12-26T10:03:34Z', body="RT @alex_gaynor: I should print one of these out and tape it to my walls: ", tags="image")

    def test_image_item(self):
        item = ImageItem.from_pinboard_item(self.image_pinboarditem)
        # item.content_type = resource.content_type
        # item.content = resource.fetch()
        self.assertTrue(hasattr(item, 'itemtype'))


class TestEvernoteSink(unittest.TestCase):
    def setUp(self):
        #FIXME Currently writes straight to the real user notebook.
        #Refer to http://discussion.evernote.com/topic/36108-passwords-and-tokens-on-sandbox/
        #Need to reset password, revoke OAuth tokens, revoke dev tokens.
        # self.evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN, sandbox=True)
        self.evernote = EvernoteSink(EVERNOTE_DEVELOPER_TOKEN)
        self.item = PinboardItem(url="http://httpbin.org/", title="httpbin", time='2013-04-25T00:00:00Z', body="Hey", tags="tag1 tag2")

    def test_connection(self):
        pass

    def test_create_note(self):
        self.evernote.note_store = mock.MagicMock()        
        created_note = self.evernote.create_note(title="Evernote Test", content="Hello World!")
        self.assertTrue(self.evernote.note_store.createNote.called)

    def test_push_arbitrary_item(self):
        self.evernote.create_note = mock.MagicMock()        
        self.evernote.push(self.item)
        self.evernote.create_note.assert_called_once_with(content=mock.ANY, title=mock.ANY, tags=mock.ANY)

    def test_push_html_item(self):
        #FIXME test for HTML specifics
        item = HTMLItem.from_pinboard_item(self.item)
        self.evernote.create_note = mock.MagicMock()        
        self.evernote.push(self.item)
        self.evernote.create_note.assert_called_once_with(content=mock.ANY, title=mock.ANY, tags=mock.ANY)

    def test_push_pdf_item(self):
        #FIXME test for PDF specifics
        item = PDFItem.from_pinboard_item(self.item)
        self.evernote.create_note = mock.MagicMock()        
        self.evernote.push(self.item)
        self.evernote.create_note.assert_called_once_with(content=mock.ANY, title=mock.ANY, tags=mock.ANY)
        #FIXME check for hash values

    #FIXME check utf-8 support


class TestENMLSanitization(unittest.TestCase):
    # Commented out because it is way too slow. Need a means to cache the DTD object.
    # def setUp(self):
    #     with open("archiver/enml2.dtd", 'r') as f:
    #         dtd = f.read()
    #     self.f = StringIO(dtd)

    # def test_validation_against_dtd(self):
    #     # FIXME this is freakishly slow
    #     self.assertTrue(validate_dtd("<a></a>", self.f))
    #     self.assertFalse(validate_dtd("<form></form>", self.f))

    def test_remove_prohibited_attributes(self):
        root = etree.fromstring("""<div id="hello">remove me<p onerror="dosomething">remove me</p></div>""")
        res = remove_prohibited_attributes(root)
        #res.findall('.//*') will only search for the child
        for n in chain([res], res.findall('.//*')):
            self.assertTrue('onerror' not in n.attrib)
            self.assertTrue('id' not in n.attrib)

    def test_remove_prohibited_elements(self):
        root = etree.fromstring("""<div>remove me<p>remove me</p><form>some form</form></div>""")
        res = remove_prohibited_elements(root)
        for n in res.findall('.//*'):
            self.assertTrue('form' not in n.tag)

    def test_url_sanitization(self):
        root = etree.fromstring("""<div><a href="http://httpbin.org">http</a><a href="https://httpbin.org">https</a><a href="ftp://httpbin.org">ftp</a></div>""")
        res = remove_prohibited_attributes(root)
        for n in res.findall('.//*'):
            self.assertTrue('ftp' not in n.attrib)

    def test_html_with_body(self):
        data = """<body onload=\"brython({debug:1, cache:'none'})\">\n<center>\n\n<\/center>\n<div><img src=\"http:\/\/brython.info\/brython.png\"><\/img><br><\/br><b>browser python<\/b><\/div>\n\n\n\n<div><p style=\"display:inline;\">\nWithout a doubt, you've seen a clock like this in demos of HTML5\n<\/p><p><canvas height=\"250\" id=\"clock\" width=\"250\">\n<i>sorry, Brython can't make the demo work on your browser ; <br><\/br>check if Javascript is turned on\n<br><\/br><\/i><\/canvas><\/p><p>\nHowever, right click and view the source of this page...\n<\/p><p>It is not Javascript code! Intead, you will find Python code in a script of type \"text\/python\"\n<\/p><p>Brython is designed to replace Javascript as the scripting language for the Web. As such, it is a Python 3 implementation (you can take it for a test drive through a web <a href=\"http:\/\/brython.info\/tests\/console_en.html\">console<\/a>), adapted to the HTML5 environment, that is to say with an interface to the DOM objects and events\n<\/p><p>The <a href=\"http:\/\/brython.info\/gallery\/gallery_en.html\">gallery<\/a> highlights a few of the possibilities, from creating simple document elements to drag and drop and 3D navigation\n<\/p><\/div>\n\n\n<\/body>"""
        html2enml(data)

    def test_html_without_body(self):
        data = """<div><h2>Introduction<\/h2><p>Conditional random field는 (CRF) 레이블의 인접성에 대한 정보를 바탕으로 레이블을 추측하는 기계학습 기법이다.\nCRF를 활용하여 여러 가지 재미있는 것들을 할 수 있는데, 이를 활용하는 방법에 대해 이야기하겠다. <a href=\"http:\/\/blog.shurain.net\/2013\/04\/crf.html\"><span id=\"ref1\">[1]<\/span><\/a><\/p><p>하지만 그래도 CRF가 어떤 식으로 동작하는 지 대충은 알아야 하니 대략적인 설명을 해보도록 하자.\n보통 품사 태깅을 (Part-of-speech tagging) 예로 많이 드니, 이를 예로 들도록 하겠다. <a href=\"http:\/\/blog.shurain.net\/2013\/04\/crf.html\"><span id=\"ref2\">[2]<\/span><\/a><\/p><h2>Part-of-Speech Tagging<\/h2><p>다음과 같은 문장이 주어졌다고 가정하자. <\/p><blockquote>\n<p>\"Bob drank coffee at Starbucks\"<\/p>\n<\/blockquote><p>각 단어에 품사를 붙여보면 다음과 같다.<\/p><blockquote>\n<p>\"NOUN VERB NOUN PREPOSITION NOUN\"<\/p>\n<\/blockquote><p>전통적인 supervised learning 기법을 적용한다고 생각해보면 트레이닝 데이터가 있을 것이고\n데이터로부터 의미 있는 특징을 (feature) 뽑아내는 과정이 있을 것이다.<\/p><p>CRF에서는 특징 함수를 (feature function) 정의하여 사용한다.\n특징 함수는 문장과 해당 문장을 구성하는 단어들의 위치 및 레이블 정보를 입력으로 받아서 어떤 실수를 (주로 0, 1) 출력하게 된다. \n각 특징 함수는 개별적인 가중치를 갖는데, 결국 어떤 문장이 주어지면 어떤 레이블이 얼마나 적합한 레이블인지를 weighted feature sum으로 계산하게 된다.<\/p><p>특징 함수의 장점은 임의의 특징을 표현하는 것이 가능하다는 점이다.\n몇 가지 특징 함수의 예를 들어보면 다음과 같다.<\/p><ul>\n<li>만약 i 번 레이블이 ADVERB 이고 \"-ly\"로 해당 단어가 끝나면 1, 아니면 0을 리턴하는 함수<\/li>\n<li>만약 i 번 레이블이 VERB 이고 문장이 물음표로 끝나면 1, 아니면 0을 리턴하는 함수<\/li>\n<li>만약 i-1 번 레이블이 ADJECTIVE이고 i번 레이블이 NOUN이면 1, 아니면 0을 리턴하는 함수<\/li>\n<\/ul><p>보는 바와 같이 특징 함수는 매우 자유로운 형태를 띌 수 있다.\nCRF는 이처럼 자유롭게 특징 함수를 만들고, 각각의 특징 함수에 가중치를 부여하고 그 합을 구해서 사용하게 된다.\n최종적으로 문장이 주어졌을 때, 특정한 레이블이 얼마나 그럴싸한지는 해당 레이블의 점수를 (weighted feature sum) 모든 가능한 레이블의 점수로 나눠주면 된다.<\/p><p>가중치를 어떤 식으로 학습하는지, 다른 종류의 더 복잡한 CRF에 대한 설명은 생략하기로 하고 이런 CRF를 어떻게 다른 용도로 활용하는 것이 가능한지 살펴보자.<\/p><h2>Different Uses<\/h2><p>CRF는 특징 함수를 매우 자유롭게 설정할 수 있기 때문에 다른 유용한 것들을 할 수 있다.\n가령 띄어쓰기가 되어 있지 않은 문장을 자동으로 띄어쓰기 해주는 것이 가능하다.\n어떤 문장이 주어졌을 때, 레이블로 각 문자마다 여기서 띄어쓰기를 해야 하는지 아닌지 정보를 0\/1로 주는 것을 상상할 수 있다.\n가령, <\/p><blockquote>\n<p>CRF로띄어쓰기를해보자<\/p>\n<\/blockquote><p>라는 문장이 주어진 경우, 올바른 형태는<\/p><blockquote>\n<p>CRF로_띄어쓰기를_해보자<\/p>\n<\/blockquote><p>일 것이다. 여기에 레이블을 붙여보면, <\/p><blockquote>\n<p>C\/0 <br><\/br>\nR\/0 <br><\/br>\nF\/0 <br><\/br>\n로\/1 <br><\/br>\n띄\/0 <br><\/br>\n어\/0 <br><\/br>\n쓰\/0 <br><\/br>\n기\/0 <br><\/br>\n를\/1 <br><\/br>\n해\/0 <br><\/br>\n보\/0 <br><\/br>\n자\/1 <br><\/br><\/p>\n<\/blockquote><p>정도로 붙여보는 것이 가능하다.\n이런 식으로 레이블이 붙어 있을 때, 이로부터 유용한 띄어쓰기 정보를 뽑아내는 특징 함수만 만들어 주면 CRF를 사용해서 이를 학습할 수 있다.\n가령 어떤 문자가 나타난 경우 그 앞의 문자와의 관계 등을 특징 함수에 넣어주는 것을 쉽게 상상할 수 있다.\n한국어 위키피디아 등의 데이터를 활용하면 쉽게 트레이닝 데이터를 만들 수 있고, 바로 CRF로 학습을 하면 끝이다. <a href=\"http:\/\/blog.shurain.net\/2013\/04\/crf.html\"><span id=\"ref3\">[3]<\/span><\/a><\/p><p><\/p><p><\/p><p><\/p><\/div>"""
        html2enml(data)


class TestArchive(unittest.TestCase):
    def setUp(self):
        pass

    def test_unicode(self):
        pass


if __name__ == '__main__':
    unittest.main()