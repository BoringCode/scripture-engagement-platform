import flask.ext.login as flask_login
from flask import g, flash
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

	query = '''
	INSERT INTO user (email_address, password, first_name, last_name)
	VALUES(:email, :pw_hash, :first_name, :last_name)
	'''

	cursor = g.db.execute(query, {"email": email, "pw_hash": pw_hash, "first_name": first_name, "last_name": last_name})
	g.db.commit()

	# Check that the query worked, then return a new user object
	if cursor.rowcount > 0:
		return User(form.email.data, form.password.data)
	else:
		return False

class User(flask_login.UserMixin):

	def __init__(self, user_id, password = False, reload_obj = False):
		self.user_id = user_id

		# If not reloading the object, make sure the user exists and the password is correct
		if not User.exists(user_id) or (reload_obj == False and password != False and not self.check_password(password)):
			self._is_active = False
			self._is_authenticated = False
		else:
			# Reloading object from session
			if reload_obj: self.get()
			self._is_active = self.user["active"]
			self._is_authenticated = True

	@property
	def is_active(self):
	    return self._is_active	

	@property
	def is_authenticated(self):
	    return self._is_authenticated

	def get_id(self):
		return self.user_id

	@staticmethod
	def exists(user_id):
		"""Check the database to see if user exists"""
		user = g.db.execute('SELECT email_address FROM user WHERE email_address = :id', {"id": user_id}).fetchone()
		return user is not None

	def get(self):
		self.user = g.db.execute('SELECT * FROM user WHERE email_address = :id', {"id": self.user_id}).fetchone()
		if self.user is not None:
			self.pw_hash = self.user["password"]

	def check_password(self, password):
		if not hasattr(self, 'user') or self.user is None:
			self.get()
		return check_password_hash(self.pw_hash, password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)
	