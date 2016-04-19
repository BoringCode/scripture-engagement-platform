import flask.ext.login as flask_login
from werkzeug.security import generate_password_hash, check_password_hash

class User(flask_login.UserMixin):

	def __init__(self, user_id):
		if not User.exists(user_id):
			raise RuntimeError("User does not exist")
		
		self._is_active = True
		self._is_authenticated = True

	@property
	def is_active(self):
	    return self._is_active	

	@property
	def is_authenticated(self):
	    return self._is_authenticated

	@staticmethod
	def exists(user_id):
		"""Check the database to see if user exists"""
		return False

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)
	