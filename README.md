Archiver
========

Archive all things possible.

Ultimately aiming to archive anything to anyware without hassle.

Currently you can load Pinboard bookmarks and strip the ads using Diffbot and send that data to Evernote.
It will also save PDF documents as well.

Installation
------------

Using virtualenv is highly recommended.

    $ pip install -r requirements.txt

Usage
-----

Find `settings.py` file under `archiver` directory.
Fill in the necessary credentials.

### Shell

    $ python archive.py

Executing on command line will pull some of the latest Pinboard bookmarks and archive them to Evernote.
Currently has some hard-coded values that needs to be changed.
Future goal is to save the update time on local sqlite database and refer to database for necessary data.

Data Source
------------

- Pinboard
    - [Social Bookmarking for Introverts](https://pinboard.in/)
    - Pinboard has one-time signup fee
    - Your API token can be found at [https://pinboard.in/settings/password](https://pinboard.in/settings/password)

Data Transformation
-------------------

- Diffbot
    - [A visual learning robot](http://diffbot.com/)
    - Diffbot has free-tier that allows for 10,000 monthly API calls

Data Sink
---------

- Evernote
    - [Remember everything](http://evernote.com/)
    - Evernote has free-tier that has limited monthly upload limit
    - API related information can be found at [Evernote developers](http://dev.evernote.com/)
        - API token related information is at [https://www.evernote.com/api/DeveloperToken.action](https://www.evernote.com/api/DeveloperToken.action)

Dependency
----------

- requests
- simplejson
- evernote
- lxml
- pytidylib
- mock (for testing)

Acknowledgement
---------------

Inspired by [pinboardToEvernote](https://github.com/mindprince/pinboardToEvernote).
