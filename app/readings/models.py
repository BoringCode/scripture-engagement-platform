from flask import g

def find_reading(id):
	return g.db.execute('SELECT * FROM reading WHERE id = :id', {"id": id}).fetchone()

def add_reading_to_db(name, creation_time,text, BG_passage_reference):
    query = '''
        INSERT INTO reading (name, creation_time, text, BG_passage_reference)
        VALUES (:name, :creation_time, :text, :BG_passage_reference)
            '''
    cursor = g.db.execute(query, {"name":name,"creation_time":creation_time, "text":text, "BG_passage_reference":BG_passage_reference})
    g.db.commit()
    return cursor.rowcount

def all_readings():
    cursor = g.db.execute('select * from reading')
    return cursor.fetchall()

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
def update_reading(name, text, reference):
    query ='''
      UPDATE reading SET name=?, text=?, BG_passage_reference=? WHERE id = :id
    '''
    return g.db.execute(query, (name, text, reference))

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