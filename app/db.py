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

	# @param String script (path to script file)
	def executeScript(self, script):
		try:
			f = open(os.path.join(os.getcwd(), script), "r")
			self.connection.cursor().executescript(f.read())
			self.commit()
			f.close()
			return True
		except:
			raise RuntimeError("Can't execute script: " + str(os.path.join(os.getcwd(), script)))
			return False

	def commit(self):
		return self.connection.commit()


	def close(self, exception):
		try:
			self.connection.close()
		except:
			raise exception