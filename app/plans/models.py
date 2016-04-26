from flask import g
import time

# access individual plan
def find_plan(id):
    return g.db.execute('SELECT * FROM plans WHERE id = :id', {"id": id}).fetchone()

# add new plan to database
def add_plan_to_db( name, description):
    #Get creation time
    creation_time = time.time()
    query = '''
        INSERT INTO plans ( name, creation_time, description)
        VALUES ( :name, :creation_time, :description)
            '''
    cursor = g.db.execute(query, { "name":name, "creation_time":creation_time, "description":description})
    g.db.commit()
    if cursor.rowcount == 1:
        return cursor.lastrowid
    else:
        return None

# access all plans in database
def all_plans():
    cursor = g.db.execute('select * from plans')
    return cursor.fetchall()

# add readings to plan
def add_readings_to_plan_reading(plan_id, reading_id, start_time_offset, end_time_offset):
    query = '''
        INSERT INTO plan_reading (plans_id, reading_id, start_time_offset, end_time_offset)
        VALUES (:plan_id, :reading_id, :start_time_offset, :end_time_offset)
            '''
    cursor = g.db.execute(query, {"plan_id":plan_id, "reading_id":reading_id, "start_time_offset":start_time_offset, "end_time_offset":end_time_offset})
    g.db.commit()
    return cursor.rowcount

def find_plan_reading(plan_id):
    query = '''
    SElECT id, name FROM reading LEFT JOIN plan_reading ON plan_reading.reading_id = reading.id WHERE plan_reading.plans_id = :plan_id
    '''
    return g.db.execute(query, {"plan_id":plan_id}).fetchall()
#-----------------------------------------------------------------------------------------------------------------------------------------------------

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
def update_plan(name, description, id):
    query = 'UPDATE plans SET name = :name, description = :description WHERE id = :id'
    cursor = g.db.execute(query, {'name': name, 'description': description, 'id': id})
    g.db.commit()
    return cursor.rowcount

#this funtion temporoary gives the next plan id. Will need to confirm this temporoary id is still the next one when plan is created.
def retrieveNextPlanId():
    return g.db.execute('SELECT * FROM plans ORDER BY id DESC LIMIT 1')+1

