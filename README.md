Archiver
========

WORK IN PROGRESS. THIS DOES NOT WORK. YET!

Archive all things possible.

Ultimately aiming to archive anything to anyware without hassle.
Currently supports the following.

Data Source
------------

- Pinboard

Data Transformation
-------------------

- Diffbot

Data Sink
---------

- Evernote

Dependency
----------

- requests
- simplejson
- evernote
- lxml
- pytidylib
- mock (for testing)

Usage
-----

Find `settings.py` file under `archiver` directory.
Fill in the necessary credentials.

### Shell

    $ archive

Executing on command line should archive stuff from data source to data sync.

