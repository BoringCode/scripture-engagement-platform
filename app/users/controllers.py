import flask
from functools import wraps
from flask import Blueprint, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
import flask.ext.login as flask_login
from urllib.parse import urlparse, urljoin

from app import login_manager

# Import models
from app.users.models import User, DBUser, register as register_user

# Import forms
import app.users.forms as forms

users = Blueprint('users', __name__)

def is_logged_in():
	return g.user is not None and g.user.is_authenticated

def next_is_valid(next):
	"""Verify that the user can navigate to this URL"""
	# Right now verify that the URL is safe
	ref_url = urlparse(flask.request.host_url)
	test_url = urlparse(urljoin(flask.request.host_url, next))
	return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def logged_out_only(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is not None and g.user.is_authenticated:
			return redirect(url_for("index"))
		return f(*args, **kwargs)
	return decorated_function

@users.route("/login/", methods=["GET", "POST"])
@logged_out_only
def login():
	form = forms.Login()

	if form.validate_on_submit():
		user = User(form.email.data, form.password.data)
		if user.is_authenticated:
			flask_login.login_user(user)

			flash("Welcome back " + user.first_name, "success")

			next = flask.request.args.get("next")
			if not next_is_valid(next):
				return flask.abort(400)

			return flask.redirect(next or flask.url_for('index'))
		flash("Cannot login with given information", "danger")
	return render_template("users/login.html", form=form)

# Set options for login required
login_manager.login_view = "users.login"
login_manager.login_message = "Please login"

@users.route("/register/", methods=["GET", "POST"])
@logged_out_only
def register():
	form = forms.Register()

	if form.validate_on_submit():
		user = register_user(form)
		if user is not False and user.is_authenticated:
			flask_login.login_user(user)

			flash("Welcome to the site " + user.first_name, "success")

			next = flask.request.args.get("next")
			if not next_is_valid(next):
				return flask.abort(400)

			return flask.redirect(next or flask.url_for('index'))
		flash("Can't create user", "danger")

	return render_template("users/register.html", form=form)

@users.route("/logout/")
@flask_login.login_required
def logout():
	flash("Logged out", "success")
	flask_login.logout_user()
	return flask.redirect(flask.url_for("index"))


@users.route("/profile/<user_id>/")
@flask_login.login_required
def profile(user_id):
	try: 
		user = DBUser(user_id)
		return render_template("users/profile.html", user=user)
	except:
		return flask.abort(404)

@login_manager.user_loader
def user_loader(user_id):
	if User.exists(user_id):
		return User(user_id, reload_obj = True)
	else:
		return None