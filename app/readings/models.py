from flask import g

def find_reading(id):
	return g.db.execute('SELECT * FROM reading WHERE id = :id', {"id": id}).fetchone()

def add_reading_to_db(id, name, creation_time,text, BG_passage_reference):
    query = '''
        INSERT INTO reading (id, name, creation_time, text, BG_passage_reference)
        VALUES (:id, :name, :creation_time, :text, :BG_passage_reference)
            '''
    cursor = g.db.execute(query, {"id":id,"name":name,"creation_time":creation_time, "text":text, "BG_passage_reference":BG_passage_reference})
    g.db.commit()
    return cursor.rowcount

def all_readings():
    cursor = g.db.execute('select * from reading')
    return cursor.fetchall()