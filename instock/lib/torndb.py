#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""A lightweight wrapper around pymysql.
Originally part of the Tornado framework.  The tornado.database module
is slated for removal in Tornado 3.0, and it is now available separately
as torndb.
"""

from __future__ import absolute_import, division, with_statement
import copy
import itertools
import logging
import os
import time
import sqlite3

__author__ = 'myh '
__date__ = '2023/3/10 '

try:

    # import MySQLdb.constants
    # import MySQLdb.converters
    # import MySQLdb.cursors

    # 修改
    import pymysql.connections
    import pymysql.converters
    import pymysql.cursors
    import pymysql.constants.FLAG


except ImportError:
    # If MySQLdb isn't available this module won't actually be useable,
    # but we want it to at least be importable on readthedocs.org,
    # which has limitations on third-party modules.
    if 'READTHEDOCS' in os.environ:
        pymysql = None
    else:
        try:
            conn = sqlite3.connect('database.db')
        except sqlite3.Error as e:
            logging.error(f"SQLite连接错误: {e}")

version = "0.3"
version_info = (0, 3, 0, 0)


class Connection(object):
    """A lightweight wrapper around MySQLdb DB-API connections.
    The main value we provide is wrapping rows in a dict/object so that
    columns can be accessed by name. Typical usage::
        db = torndb.Connection("localhost", "mydatabase")
        for article in db.query("SELECT * FROM articles"):
            print article.title
    Cursors are hidden by the implementation, but other than that, the methods
    are very similar to the DB-API.
    We explicitly set the timezone to UTC and assume the character encoding to
    UTF-8 (can be changed) on all connections to avoid time zone and encoding errors.
    The sql_mode parameter is set by default to "traditional", which "gives an error instead of a warning"
    (http://dev.mysql.com/doc/refman/5.0/en/server-sql-mode.html). However, it can be set to
    any other mode including blank (None) thereby explicitly clearing the SQL mode.
    """

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def query(self, query, *parameters):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def execute(self, query, *parameters):
        self.cursor.execute(query, parameters)
        self.connection.commit()

    def close(self):
        self.connection.close()


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if pymysql is not None:
    # Fix the access conversions to properly recognize unicode/binary
    FIELD_TYPE = pymysql.constants.FIELD_TYPE
    FLAG = pymysql.constants.FLAG
    CONVERSIONS = copy.copy(pymysql.converters.conversions)

    field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
    if 'VARCHAR' in vars(FIELD_TYPE):
        field_types.append(FIELD_TYPE.VARCHAR)

    for field_type in field_types:
        # CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]
        CONVERSIONS[field_type] = [(FLAG.BINARY, str)].append(CONVERSIONS[field_type])

    # Alias some common MySQL exceptions
    IntegrityError = pymysql.IntegrityError
    OperationalError = pymysql.OperationalError
