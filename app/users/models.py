import flask.ext.login as flask_login
from flask import g, flash
import time
from werkzeug.security import generate_password_hash, check_password_hash

def register(form):
	"""Create user from form input"""

	email = form.email.data

	if User.exists(email):
		flash("User already exists, try logging in")
		return False

	first_name = form.first_name.data
	last_name = form.last_name.data
	# We don't store the user's password (EVER)
	pw_hash = generate_password_hash(form.password.data)
	creation_time = time.time()

	query = '''
	INSERT INTO user (email_address, password, first_name, last_name, creation_time)
	VALUES(:email, :pw_hash, :first_name, :last_name, :creation_time)
	'''

	cursor = g.db.execute(query, {"email": email, "pw_hash": pw_hash, "first_name": first_name, "last_name": last_name, "creation_time": creation_time})
	g.db.commit()

	# Check that the query worked, then return a new user object
	if cursor.rowcount > 0:
		return User(form.email.data, form.password.data)
	else:
		return False

class DBUser():
	def __init__(self, user_id):
		self._user_id = user_id

		if not DBUser.exists(self._user_id):
			raise TypeError

		self.get()

	@property 
	def first_name(self):
		return self._user["first_name"]

	@property
	def last_name(self):
	    return self._user["last_name"]	

	@property
	def is_active(self):
	    return self._user["active"]

	@property
	def user_id(self):
		return self._user_id

	def get(self):
		if hasattr(self, '_user') and self._user is not None: return
		self._user = g.db.execute('SELECT * FROM user WHERE id = :id', {"id": self._user_id}).fetchone()

	@staticmethod
	def exists(user_id):
		"""Check the database to see if user exists (based upon user index)"""
		user = g.db.execute('SELECT email_address FROM user WHERE id = :id', {"id": user_id}).fetchone()
		return user is not None


class User(flask_login.UserMixin):

	def __init__(self, user_id, password = False, reload_obj = False):
		self._user_id = user_id

		# If not reloading the object, make sure the user exists and the password is correct
		if not User.exists(self._user_id) or (reload_obj == False and password != False and not self.check_password(password)):
			self._is_active = False
			self._is_authenticated = False
		else:
			self.get()
			self._is_active = self._user["active"]
			self._is_authenticated = True

	@property 
	def first_name(self):
		return self._user["first_name"]

	@property
	def last_name(self):
	    return self._user["last_name"]

	@property
	def user_index(self):
	    return self._user["id"]
		
	@property
	def is_active(self):
	    return self._is_active	

	@property
	def is_authenticated(self):
	    return self._is_authenticated

	def get_id(self):
		return self._user_id

	@staticmethod
	def exists(user_id):
		"""Check the database to see if user exists"""
		user = g.db.execute('SELECT email_address FROM user WHERE email_address = :id', {"id": user_id}).fetchone()
		return user is not None

	def get(self):
		if hasattr(self, '_user') and self._user is not None: return
		self._user = g.db.execute('SELECT * FROM user WHERE email_address = :id', {"id": self._user_id}).fetchone()

	def check_password(self, password):
		"""Verify that entered password generates a hash equal to the hash stored in the database"""
		self.get()
		return check_password_hash(self._user["password"], password)

	def set_password(self, password):
		"""Update user's password"""
		new_password_hash = generate_password_hash(password)
		query = 'UPDATE user SET password=:password WHERE email_address = :id'
		return g.db.execute(query, {"password": new_password_hash, "id": self._user_id}).rowcount == 1
	