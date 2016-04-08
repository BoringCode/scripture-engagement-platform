from flask import g
import time

# find plan
def find_plan(id):
	return g.db.execute('SELECT * FROM plans WHERE id = :id', {"id": id}).fetchone()

# add plan
def add_plan_to_db(author_id, name, description):
    #Get creation time
    creation_time = time.time()
    query = '''
        INSERT INTO plans (author_id_fk, name, creation_time, description)
        VALUES (:author_id, :name, :creation_time, :description)
            '''
    cursor = g.db.execute(query, {"author_id":author_id, "name":name, "creation_time":creation_time, "description":description})
    g.db.commit()
    return cursor.rowcount

def all_plans():
    cursor = g.db.execute('select * from plans')
    return cursor.fetchall()

def add_readings_to_plan_reading(plan_id, reading_id, start_time_offset, end_ime_offset):
    query = '''
        INSERT INTO plan_reading (plans_id, reading_id, start_time_offset, end_time_offset)
        VALUES (:plan_id, :reading_id, :start_time_offset, :end_time_offset)
            '''
    cursor = g.db.execute(query, {"plans_id":plan_id, "reading_id":reading_id, "start_time_offset":start_time_offset, "end_time_offset":end_ime_offset})
    g.db.commit()
    return cursor.rowcount

#delete plans
def delete_reading(id):
    delete_subscription(id, False)
    delete_group_subscription(id, False)
    delete_plan_reading(id, False)
    delete_feedback(False, id, False, False)

def delete_subscription(plan_id, user_id):
    return g.db.execute('DELETE FROM subscription WHERE plans_id = :plan_id OR user_id = :user_id', {"plan_id": plan_id, "user_id": user_id}).fetchall()


def delete_group_subscription(plan_id,group_id):
    return g.db.execute('DELETE FROM group_subscription WHERE plans_id = :plan_id OR group_id = :group_id', {"plans_id": plan_id, "group_id": group_id}).fetchall()

#this method is in readings, find a way to import it
def delete_plan_reading(plan_id, reading_id):
   return g.db.execute('DELETE FROM plan_reading WHERE reading_id = :reading_id OR plan_id = :plan_id', {"reading_id": reading_id, "plan_id": plan_id}).fetchall()

#add this to readings too!
def delete_feedback(author_id_fk, plan_id_fk, content_id_fk, reading_id_fk):
    return g.db.execute('DELETE FROM feedback WHERE author_id_fk = :author_id_fk OR plan_id_fk = :plan_id_fk OR content_id_fk = :content_id_fk OR reading_id_fk = :reading_id_fk', {"reading_id_fk": reading_id_fk, "plan_id_fk": plan_id_fk, "author_id_fk": author_id_fk, "content_id_fk": content_id_fk}).fetchall()

# update plan
# Should the author_id be updated too?
def update_plan(name, description):
    query ='''
      UPDATE reading SET name=?, description=? WHERE id = :id
    '''
    return g.db.execute(query, (name, description))



