import flask.ext.login as flask_login

class User(flask_login.UserMixin):

	def __init__(self, user_id):
		
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
		pass
	