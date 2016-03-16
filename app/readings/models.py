from flask import g

def find_reading(id):
	return g.db.execute('SELECT * FROM reading WHERE id = :id', {"id": id}).fetchone() 