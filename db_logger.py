#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import sqlite3 as lite
import time
import random
import datetime as dt

class SQLITE_DB_LOGGER():

	def log_to_sqlite(self, log_data):
		try:
			con = lite.connect('test.db')
			cur = con.cursor()
			cur.execute('SELECT SQLITE_VERSION()')
			data = cur.fetchone()
			print "SQLite version: %s" % data
			cur.execute("CREATE TABLE IF NOT EXISTS TEMPLOG (id INTEGER, Value REAL, Time TEXT)")
			tid = 0
			dt = time.asctime( time.localtime(time.time()) )
			cur.execute("INSERT INTO TEMPLOG (id, Value, Time) VALUES(?,?,?)", (tid, log_data, dt))
			con.commit()
		except lite.Error, e:
			if con:
				con.rollback()
				print "Error %s:" % e.args[0]
				sys.exit(1)