from flask import g
import time
from app.users.models import DBUser

from app.scripture.bg_api import BGAPI

bg_api = BGAPI()

def find_reading(id):
	return g.db.execute('SELECT * FROM reading WHERE id = :id', {"id": id}).fetchone()

def find_reading_passages(id,translation):
    passages = g.db.execute('SELECT * FROM reading_passages WHERE reading_id = :id', {"id":id}).fetchall()
    verses = {}
    for entry in passages:
        verses[entry["BG_passage_reference"]] = bg_api.get_passage(translation, entry["BG_passage_reference"])
    return verses

def get_posts(id):
    query = "SELECT * FROM post LEFT JOIN reading_post ON reading_post.post_id = post.id WHERE reading_post.reading_id = :id ORDER BY time DESC"
    rows = g.db.execute(query, {"id": id}).fetchall()
    posts = []
    # Parse results from query (grab author information)
    for row in rows:
        posts.append({
            "time": row["time"],
            "approved": row["approved"],
            "message": row["message"],
            "author": DBUser(row["user_id_fk"])
        })
    return posts

def add_reading_to_db(name,text, translation):
    #Get creation time
    creation_time = time.time()
    query = '''
        INSERT INTO reading (name, author_id, creation_time, text, translation)
        VALUES (:name, :author_id, :creation_time, :text, :translation)
            '''
    cursor = g.db.execute(query, {"name":name, "author_id": g.user.user_id, "creation_time":creation_time, "text":text, "translation":translation})
    g.db.commit()
    return cursor.rowcount

def all_readings():
    cursor = g.db.execute('select * from reading')
    return cursor.fetchall()

def add_more_passages(id, BG_passage_reference):
    query = '''
        INSERT INTO reading_passages (reading_id, BG_passage_reference)
        VALUES(:id, :BG_passage_reference)
        '''
    cursor = g.db.execute(query, {"id":id, "BG_passage_reference":BG_passage_reference})
    g.db.commit()
    return cursor.rowcount

#delete readings
def delete_reading(id):
    delete_reading_content(id, False)
    delete_reading_post(id, False)
    delete_plan_reading(False, id)

#delete_reading_post(id,False)
    return g.db.execute('DELETE FROM reading WHERE id = :id', {"id": id}).fetchone()

def delete_reading_content(reading_id, content_id):
    return g.db.execute('DELETE FROM reading_content WHERE reading_id = :reading_id OR content_id = :content_id', {"reading_id": reading_id, "content_id": content_id}).fetchall()


def delete_reading_post(reading_id,post_id):
#return g.db.execute('DELETE FROM reading_post WHERE reading_id = :reading_id OR post_id = :post_id', {"reading_id": reading_id, "post_id": post_id}).fetchall()
    return True

def delete_plan_reading(plan_id, reading_id):
    #return g.db.execute('DELETE FROM plan_reading WHERE reading_id = :reading_id OR plan_id = :plan_id', {"reading_id": reading_id, "plan_id": plan_id}).fetchall()
    return True

#update reading
def update_reading(id, name, text, translation):
    query ='''
      UPDATE reading SET name=:name, text=:text, translation=:translation WHERE id = :id
    '''
    return g.db.execute(query, {"id": id, "name": name, "text": text, "translation": translation}).rowcount

#reading content
def all_reading_content(reading_id):
    query = '''
        SELECT content.name, content.content
        FROM content, reading, reading_content
        WHERE (content.id=reading_content.content_id) AND (reading.id=reading_content.reading_id) AND (reading.id= :reading_id)
        ORDER BY content.id;
    '''

    cursor = g.db.execute(query, {"reading_id":reading_id})
    return cursor.fetchall()

