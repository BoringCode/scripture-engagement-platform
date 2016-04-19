from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort

from app import login_manager

# Import models
from app.users.models import User

users = Blueprint('users', __name__)

@users.route("/login/")
def login():
	return render_template("users/login.html")

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
