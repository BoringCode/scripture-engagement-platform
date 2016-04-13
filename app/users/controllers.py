from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort

# Import models
import app.users.models as models

users = Blueprint('users', __name__)

@users.route("/login/")
def login():
	return render_template("users/login.html")
