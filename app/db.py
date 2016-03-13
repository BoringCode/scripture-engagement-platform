import sqlite3
from flask import g
import os

class DB():
	DATABASE = 'app/database.db'

	def __init__(self, db_path=None):
	    if db_path is None:
	        db_path = os.path.join(os.getcwd(), self.DATABASE)
	    #Check that db_path exists
	    if not os.path.isfile(db_path):
	        raise RuntimeError("Can't find database file '{}'".format(db_path))
	    #Init connection to database
	    self.connection = sqlite3.connect(db_path)
	    self.connection.row_factory = sqlite3.Row

	def execute(self, query, arguments = {}):
		cursor = self.connection.execute(query, arguments)
		return cursor

	def close(self, exception):
		try:
			self.connection.close()
		except:
			raise exception