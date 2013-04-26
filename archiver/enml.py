"""
HTML to ENML Converter

1. Convert the document into valid XML
2. Discard all tags that are not accepted by the ENML DTD
3. Convert tags to the proper ENML equivalent (e.g. BODY becomes EN-NOTE)
4. Validate against the ENML DTD
5. Validate href and src values to be valid URLs and protocols

http://dev.evernote.com/start/core/enml.php
"""
from lxml import etree
from lxml.html import fromstring
from urlparse import urlparse
from itertools import chain
from tidylib import tidy_document, tidy_fragment

import logging


def html2enml(html):
    doc, err= tidy_fragment(
        html,
        options={
            "output-xhtml": 1,
            "drop-proprietary-attributes": 1,
            "merge-divs": 1,
            "clean": 1
        }
    )

    root = fromstring(doc)
    # root = fromstring(html)
    root = remove_prohibited_elements(root)
    root = remove_prohibited_attributes(root)
    # Skipping dtd validation
    # validate_dtd(html, f):
    root.tag = 'div'
    # logging.debug(root)

    return etree.tostring(root)

def remove_prohibited_elements(root):
    prohibited_elements = [
    "applet",
    "base",
    "basefont",
    "bgsound",
    "blink",
    "body",
    "button",
    "dir",
    "embed",
    "fieldset",
    "form",
    "frame",
    "frameset",
    "head",
    "html",
    "iframe",
    "ilayer",
    "input",
    "isindex",
    "label",
    "layer",  # WAT? Original document say "layer,"
    "legend",
    "link",
    "marquee",
    "menu",
    "meta",
    "noframes",
    "noscript",
    "object",
    "optgroup",
    "option",
    "param",
    "plaintext",
    "script",
    "select",
    "style",
    "textarea",
    "xml",
    ]
    for node in root.findall('.//*'):
        if node.tag in prohibited_elements:
            p = node.getparent()
            p.remove(node)

    return root

def remove_prohibited_attributes(root):
    prohibited_attributes = [
        "id",
        "class",
        "onclick",
        "ondblclick",
        "accesskey",
        "data",
        "dynsrc",
        "tabindex",
    ]

    regex_prohibited_attributes = [
        "on",  # starts with on. original documentation says "on*"
    ]

    # Note that this will change the contents of root node inplace
    for node in chain(root.findall('.//*'), [root]):
        for att in prohibited_attributes:
            if att in node.attrib:
                node.attrib.pop(att)
        for att in regex_prohibited_attributes:
            [node.attrib.pop(k) for k in node.attrib.keys() if k.startswith(att)]

        #url sanitization
        if 'href' in node.attrib:
            url = urlparse(node.attrib.get('href'))
            if url.scheme not in ('http', 'https', 'file'):
                node.attrib.pop('href')

    return root

def validate_dtd(html, f):
    """
    html string, f file handle
    """
    dtd = etree.DTD(f)  # FIXME this is very slow
    root = etree.XML(html)
    return dtd.validate(root)


def add_styles():
    return ''
