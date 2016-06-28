#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import sqlite3 as lite
import time
#import mysql.connector
import datetime as dt

class DB_LOGGER():

	def log_to_sqlite(self, db_name, table_name, log_data,):
		try:
			con = lite.connect(db_name+'.db')
			cur = con.cursor()
			cur.execute("CREATE TABLE IF NOT EXISTS"+table_name+"(Value REAL, Time TEXT)")
			dt = time.asctime( time.localtime(time.time()) )
			cur.execute("INSERT INTO TEMPLOG (Value, Time) VALUES(?,?,?)", (log_data, dt))
			con.commit()
		except lite.Error, e:
			if con:
				con.rollback()
				print "Error %s:" % e.args[0]
				sys.exit(1)

	def log_to_mySQL(self, user, password, host, db_name):
		try:
			cnx = mysql.connector.connect(user=user, password=password, host=host, database=db_name)
			print cnx
		except mysql.connector.Error as err:
			print err