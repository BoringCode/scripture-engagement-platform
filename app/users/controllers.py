from flask import Blueprint, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
import flask.ext.login as flask_login

from app import login_manager

# Import models
from app.users.models import User

# Import forms
import app.users.forms as forms

users = Blueprint('users', __name__)

@users.route("/login/", methods=["GET", "POST"])
def login():
	form = forms.Login()

	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))

	if form.validate_on_submit() and User.exists(form.username.data):
		user = User(form.email.data)
		if user.checkPassword(form.password.data):
			flask_login.login_user(user)

			flash('Logged in successfully.')

			next = flask.request.args.get('next')
		    # next_is_valid should check if the user has valid
		    # permission to access the `next` url
			if not next_is_valid(next):
				return flask.abort(400)

			return flask.redirect(next or flask.url_for('index'))
		flash("Can't login", "danger")
	return render_template("users/login.html", form=form)

@users.route("/profile/")
def profile():
	return render_template("users/profile.html")

@login_manager.request_loader
def request_loader(request):
	user_id = request.form.get("email")
	if User.exists(user_id):
		return User(user_id)
	else:
		return None

@login_manager.user_loader
def user_loader(user_id):
	if User.exists(user_id):
		return User(user_id)
	else:
		return None
