from flask import g
import time
from app.users.models import DBUser

def find_user(id):
    return g.db.execute('SELECT * FROM user WHERE id = :id', {"id": id}).fetchone()

def find_group(id):
    return g.db.execute('SELECT * FROM user_group WHERE id = :id', {"id": id}).fetchone()

def all_groups():
    cursor = g.db.execute('select * from user_group')
    return cursor.fetchall()

def all_users():
    cursor = g.db.execute('select * from user')
    return cursor.fetchall()

def all_users_in_group(user_group_id):
    users =  g.db.execute('SELECT user_id from group_invitation WHERE group_id = :user_group_id', {"user_group_id":user_group_id}).fetchall()
    return [DBUser(user["user_id"]) for user in users]

def all_plans():
    cursor = g.db.execute('select * from plans')
    return cursor.fetchall()

def all_plans_in_group(user_group_id):
    return g.db.execute('select plans_id from group_subscription WHERE group_id = :user_group_id', {"user_group_id":user_group_id}).fetchall()

def add_plan_to_group(id, user_group_id):
    creation_time = time.time()
    query = '''
        INSERT INTO group_subscription (plans_id, group_id, creation_time)
        VALUES (:plans_id, :group_id, :creation_time)
            '''
    cursor = g.db.execute(query, {"plans_id":id, "group_id":user_group_id, "creation_time":creation_time})
    g.db.commit()
    return cursor.rowcount

def add_user_to_group(user_group_id, user_id):
    creation_time = time.time()
    query = '''
        INSERT INTO group_invitation (group_id, user_id, creation_time)
        VALUES (:group_id, :user_id, :creation_time)
    '''
    cursor = g.db.execute(query, {"group_id":user_group_id, "user_id":user_id, "creation_time":creation_time})
    g.db.commit()
    return cursor.rowcount

def add_group_to_db(name, public, description):
    #Get creation time
    creation_time = time.time()
    query = '''
        INSERT INTO user_group (name, public, creation_time, description)
        VALUES (:name, :public, :creation_time, :description)
            '''
    cursor = g.db.execute(query, {"name":name, "public":public, "creation_time":creation_time, "description":description})
    g.db.commit()
    if cursor.rowcount == 1:
        return cursor.lastrowid
    else:
        return False

# update group
def update_group(id, name, public, description):
    query = 'UPDATE user_group SET name = :name, public = :public, description = :description WHERE id = :id'
    cursor = g.db.execute(query, {'name': name, 'public': public, 'description': description, 'id': id})
    g.db.commit()
    return cursor.rowcount

#delete user from group