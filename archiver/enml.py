"""
HTML to ENML Converter

1. Convert the document into valid XML
2. Discard all tags that are not accepted by the ENML DTD
3. Convert tags to the proper ENML equivalent (e.g. BODY becomes EN-NOTE)
4. Validate against the ENML DTD
5. Validate href and src values to be valid URLs and protocols

http://dev.evernote.com/start/core/enml.php
"""
try:
    from lxml import etree
except ImportError:
    # Python 2.5
    import xml.etree.cElementTree as etree


def html2enml(html):
    return ''

def remove_prohibited_elements():
    return ''

def remove_prohibited_attributes():
    return ''

def sanitize_urls():
    return ''

def validate_dtd(html, f):
    """
    html string, f file handle
    """
    dtd = etree.DTD(f)  # FIXME this is very slow
    root = etree.XML(html)
    return dtd.validate(root)


def add_styles():
    return ''

if __name__ == '__main__':
    validate_dtd("<foo/>")