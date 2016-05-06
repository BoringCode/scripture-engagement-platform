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
    return g.db.execute('select user_id from group_invitation WHERE group_id = :user_group_id', {"user_group_id":user_group_id}).fetchall()

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

def add_user_to_group(user_id, user_group_id):
    creation_time = time.time()
    query = '''
        INSERT INTO group_invitation (group_id, user_id, creation_time)
        VALUES (:user_group_id, :user_id, :creation_time)
            '''
    cursor = g.db.execute(query, {"group_id":user_group_id, "user_id":user_id, "creation_time":creation_time})
    g.db.commit()
    return cursor.rowcount

def add_group_to_db(id, name, public, description):
    #Get creation time
    creation_time = time.time()
    query = '''
        INSERT INTO user_group (id, name, public, creation_time, description)
        VALUES (:id, :name, :public, :creation_time, :description)
            '''
    cursor = g.db.execute(query, {"id":id, "name":name, "public":public, "creation_time":creation_time, "description":description})
    g.db.commit()
    return cursor.rowcount

# update group
def update_group(id, name, public, description):
    query = 'UPDATE user_group SET name = :name, public = :public, description = :description WHERE id = :id'
    cursor = g.db.execute(query, {'name': name, 'public': public, 'description': description, 'id': id})
    g.db.commit()
    return cursor.rowcount

def get_posts(id):
    query = "SELECT * FROM post LEFT JOIN group_post ON group_post.post_id = post.id WHERE group_post.group_id = :id ORDER BY time DESC"
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

#delete user from group