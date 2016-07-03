#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import sqlite3 as lite
import time
import mysql.connector

class DB_LOGGER():

	#create table witgh predefined name (table_name) and logs given data(log_data - REAL) and current timestamp - TEXT
	def log_to_sqlite(self, db_name, table_name, log_data,):
		try:
			con = lite.connect(db_name+'.db')
			cur = con.cursor()
			cur.execute("CREATE TABLE IF NOT EXISTS "+table_name+"(Value REAL, Time TEXT)")
			dt = time.asctime( time.localtime(time.time()) )
			cur.execute("INSERT INTO " + table_name + " (Value, Time) VALUES(?,?)", (log_data, dt))
			con.commit()
		except lite.Error, e:
			if con:
				con.rollback()
				print "Error %s:" % e.args[0]
				sys.exit(1)
