#!/usr/bin/env python
from .pinboard import fetch_pinboard
from .evernote import send_to_evernote


def main():
    bookmarks = fetch_pinboard()
    for bookmark in bookmarks:
        data = preprocess()  # do the right thing for right content type
        send_to_evernote(data)

if __name__ == '__main__':
    main()