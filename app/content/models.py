from flask import g
import time

#Get content by reading ID
def get_reading_content(reading_id):
	query = "SELECT * FROM content JOIN reading_content ON content.id = reading_content.content_id WHERE reading_content.reading_id = :id"
	return g.db.execute(query, {"id": reading_id}).fetchall()

#Get readings by content ID
def get_content_reading(content_id):
	query = "SELECT * FROM reading JOIN reading_content ON reading.id = reading_content.reading_id WHERE reading_content.content_id = :id"
	return g.db.execute(query, {"id": content_id}).fetchall()

def find_content(id):
	return g.db.execute('SELECT * FROM content WHERE id = :id', {"id": id}).fetchone()

def add_content_to_db(name ,approved, description):
    creation_time = time.time()
    query = '''
        INSERT INTO content (name, author_id, creation_time, approved, description)
        VALUES (:name, :author_id, :creation_time, :approved, :description)
            '''
    cursor = g.db.execute(query, {"name":name, "author_id": g.user.user_id, "creation_time":creation_time, "approved":approved, "description":description})
    g.db.commit()
    return cursor.rowcount

def all_content():
    cursor = g.db.execute('select * from content')
    return cursor.fetchall()

def associated_content(reading_id):
    query = 'select content_id from reading_content where reading_id = :reading_id;'
    cursor = g.db.execute(query, {'reading_id' : reading_id})
    return cursor.fetchall()


# update content
# Should the author_id be updated too?
def update_content(name, approved, description, id):
    query = 'UPDATE content SET name = :name, approved = :approved, description = :description WHERE id = :id'
    cursor = g.db.execute(query, {'name': name, 'approved': approved, 'description': description, 'id': id})
    g.db.commit()
    return cursor.rowcount

def delete_content(id):
    g.db.execute('DELETE FROM content WHERE id = :id', {'id': id}).fetchall()
    g.db.commit()
    return