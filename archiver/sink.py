# -*- coding: utf-8 -*-

import hashlib
import binascii

from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from evernote.edam.userstore import UserStore
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

from evernote.api.client import EvernoteClient

from .settings import EVERNOTE_NOTEBOOK

import logging

class Sink(object):
    pass

class EvernoteSink(Sink):
    def __init__(self, token, sandbox=False):
        """Initialize evernote connection.
        Client connection handle is assigned to the client property.
        Two properties user_store and note_store are provided for the convenience.
        """
        self.token = token
        self.client = EvernoteClient(token=self.token, sandbox=sandbox)
        self.user_store = self.client.get_user_store()
        self.note_store = self.client.get_note_store()

    def image_resource(self, item):
        #FIXME create pdf resource
        md5 = hashlib.md5()
        md5.update(item.content)
        hashvalue = md5.digest()

        data = Types.Data()
        data.size = len(item.content)  #FIXME better ways of doing this calculation?
        data.bodyHash = hashvalue
        data.body = item.content

        resource = Types.Resource()
        resource.mime = item.content_type
        resource.data = data
        return resource

    def pdf_resource(self, item):
        #FIXME create pdf resource
        md5 = hashlib.md5()
        md5.update(item.content)
        hashvalue = md5.digest()

        data = Types.Data()
        data.size = len(item.content)  #FIXME better ways of doing this calculation?
        data.bodyHash = hashvalue
        data.body = item.content

        resource = Types.Resource()
        resource.mime = 'application/pdf'
        resource.data = data
        return resource

    def note_attribute(self, source_url=''):
        attribute = Types.NoteAttributes()
        attribute.sourceURL = source_url
        return attribute

    def create_note(self, title, content, notebook_name='', tags='', attribute=None, resources=None):
        note = Types.Note()
        note.title = title
        if attribute:
            note.attribute = attribute
        if tags:
            note.tagNames = tags.split()  # Assuming no spaces in tags

        if notebook_name:
            notebooks = self.note_store.listNotebooks(self.token)
            for notebook in notebooks:
                if notebook.name == notebook_name:
                    note.notebookGuid = notebook.guid
                    break
            else:
                pass  # create a note in default notebook

        note.content = """<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
        <en-note>{}""".format(content.encode('ascii', 'xmlcharrefreplace'))

        if resources:
            note.resources = resources
            for r in resources:
                note.content += """<en-media type="{}" hash="{}"/>""".format(r.mime, binascii.hexlify(r.data.bodyHash))

        note.content += "</en-note>"

        logging.debug(note.content)

        created_note = self.note_store.createNote(self.token, note)
        return created_note

    def push(self, item):
        kwargs = {
            'title': item.title.encode('utf-8', 'xmlcharrefreplace'),
            'content': item.body,
            'tags': item.tags,
            'notebook_name': EVERNOTE_NOTEBOOK,
        }

        if item.itemtype == 'PDF':
            resource = self.pdf_resource(item)
            kwargs['resources'] = [resource]
        elif item.itemtype == 'image':
            resource = self.image_resource(item)
            kwargs['resources'] = [resource]
        elif item.itemtype == 'HTML' or item.itemtype == 'text':
            #FIXME check for image inside and create image resources
            kwargs['content'] = item.content
        #FIXME handle plain text properly.
        # Evernote documentation suggests the following
        # Applications that wish to store plaintext notes in Evernote must convert newlines into HTML-style blocks.
        # To ensure that notes render correctly across clients, we recommend that you wrap each paragraph in a <div> element. 
        # For each blank line, insert a <div> containing a single <br>. 
        
        # elif item.itemtype == 'text':
        #     content = item.body.split('\n')
        #     kwargs['content'] = ''.join(['<div>' + body + '</div>' for body in content])
        else:
            # XXX Assuming plaintext type        
            # Should I raise exception for unknown items?
            item.itemtype = 'text'


        self.create_note(**kwargs)

class Database(Sink):
    pass