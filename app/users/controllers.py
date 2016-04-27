import flask
from flask import Blueprint, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
import flask.ext.login as flask_login

from app import login_manager

# Import models
from app.users.models import User, DBUser, register as register_user

# Import forms
import app.users.forms as forms

users = Blueprint('users', __name__)

@users.route("/login/", methods=["GET", "POST"])
def login():
	form = forms.Login()

	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))

	if form.validate_on_submit():
		user = User(form.email.data, form.password.data)
		if user.is_authenticated:
			flask_login.login_user(user)

			flash('Logged in successfully.')

			next = flask.request.args.get('next')
		    # next_is_valid should check if the user has valid
		    # permission to access the `next` url
			#if not next_is_valid(next):
			#	return flask.abort(400)

			return flask.redirect(next or flask.url_for('index'))
		flash("Cannot login with given information", "danger")
	return render_template("users/login.html", form=form)

@users.route("/register/", methods=["GET", "POST"])
def register():
	form = forms.Register()

	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))

	if form.validate_on_submit():
		user = register_user(form)
		if user is not False and user.is_authenticated:
			flask_login.login_user(user)

			flash("Created user!")

			next = flask.request.args.get('next')

		    # next_is_valid should check if the user has valid
		    # permission to access the `next` url
			#if not next_is_valid(next):
			#	return flask.abort(400)

			return flask.redirect(next or flask.url_for('index'))
		flash("Can't create user", "danger")

	return render_template("users/register.html", form=form)

@users.route("/logout/")
@flask_login.login_required
def logout():
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

"""
@login_manager.request_loader
def request_loader(request):
	user_id = request.form.get("email")
	password = request.form.get("password")
	if user_id is not None and password is not None and User.exists(user_id):
		return User(user_id, password)
	else:
		return None
"""


@login_manager.user_loader
def user_loader(user_id):
	if User.exists(user_id):
		return User(user_id, reload_obj = True)
	else:
		return None
