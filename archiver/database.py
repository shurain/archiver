# -*- coding: utf-8 -*-

import sqlite3
import logging

from .settings import DATABASE_PATH


class PinboardDatabase(object):
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.c = self.conn.cursor()

        try:
            self.c.execute("SELECT * FROM pinboard")
        except sqlite3.OperationalError as e:
            # no such table
            logging.warn(e)
            self.c.execute("CREATE TABLE pinboard (id INTEGER PRIMARY KEY, last_updated TEXT)")

        self.c.execute("SELECT * FROM pinboard")
        res = self.c.fetchone()

        if res is None:
            self.c.execute("INSERT INTO pinboard VALUES (NULL, ?)", ('1970-01-01T00:00:00Z', ))  # beginning of time
            self.conn.commit()
            self.c.execute("SELECT * FROM pinboard")
            res = self.c.fetchone()

        pid, datestr = res  # 0 contains the index "1"

    def close(self):
        self.conn.close()

    @property
    def last_updated(self):
        self.c.execute("SELECT * FROM pinboard")
        pid, datestr = self.c.fetchone()
        return datestr

    @last_updated.setter
    def last_updated(self, at):
        self.c.execute("UPDATE pinboard set last_updated = ? where id = 1", (at,))
        self.conn.commit()
