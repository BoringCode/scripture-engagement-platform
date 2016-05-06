from flask import g
import time

import app.readings.models as readings_model

import app.groups.models as group_models

def create_post(user, message, originator_type, originator_id):
	"""Create post given user and message"""
	post_time = time.time()
	query = '''
	INSERT INTO post (user_id_fk, time, message)
	VALUES (:user_id, :time, :message)
	'''
	cursor = g.db.execute(query, {"user_id": user, "time": post_time, "message": message})
	if (cursor.rowcount == 1):
		post_id = cursor.lastrowid

		# Create relationship with originating post type (reading or group)
		if originator_type == "reading" and readings_model.find_reading(originator_id) is not None:
			query = '''
			INSERT INTO reading_post (reading_id, post_id)
			VALUES (:reading_id, :post_id)
			'''
			cursor = g.db.execute(query, {"reading_id": originator_id, "post_id": post_id})
			g.db.commit()

		if originator_type == "group" and group_models.find_group(originator_id) is not None:
			query = '''
			INSERT INTO group_post (group_id, post_id)
			VALUES (:group_id, :post_id)
			'''
			cursor = g.db.execute(query,{"group_id": originator_id, "post_id": post_id})
			g.db.commit()
	return cursor.rowcount