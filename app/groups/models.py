from flask import g
import time

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
    return g.db.execute('select user_id from group_invitation WHERE group_id = :user_group_id', {"group_id":user_group_id}).fetchall()

def add_user_to_group(user_id, user_group_id):
    creation_time = time.time()
    query = '''
        INSERT INTO group_invitation (group_id, user_id, creation_time)
        VALUES (:user_group_id, :user_id, :creation_time)
            '''
    cursor = g.db.execute(query, {"group_id":user_group_id, "user_id":user_id, "creation_time":creation_time})
    g.db.commit()
    return cursor.rowcount

#delete user from group