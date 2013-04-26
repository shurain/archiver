from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from evernote.edam.userstore import UserStore
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

from evernote.api.client import EvernoteClient

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

    def image_resource(self):
        pass

    def pdf_resource(self):
        pass

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
            for note in notebooks:
                if notebook.name == notebook_name:
                    note.notebookGuid = notebook.guid
                    break
            else:
                pass  # create a note in default notebook

        note.content = """<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
        <en-note>{}""".format(content.encode('ascii', 'xmlcharrefreplace'))

        if resources:
            #FIXME
            pass

        note.content += "</en-note>"

        created_note = self.note_store.createNote(self.token, note)
        return created_note

    def push(self, item):
        kwargs = {
            'title': item.title.encode('utf-8', 'xmlcharrefreplace'),
            'content': item.body,
            'tags': item.tags,
        }

        if item.itemtype == 'PDF':
            #FIXME create pdf resource
            pass
        elif item.itemtype == 'HTML':
            #FIXME check for image inside and create image resources
            kwargs['content'] = item.content
        else:
            # XXX Assuming plaintext type        
            # Should I raise exception for unknown items?
            item.itemtype = 'text'


        self.create_note(**kwargs)

class Database(Sink):
    pass