from flask import Blueprint, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
import flask.ext.login as flask_login

# Import forms
import app.posts.forms as forms

# Import models
import app.posts.models as models

# Create blueprint for readings routes
posts = Blueprint('posts', __name__)

@posts.route("/new/", methods=["POST"])
@flask_login.login_required
def new_post():
	form = forms.NewPost()
	if form.validate_on_submit():
		models.create_post(g.user.user_id, form.comment.data, form.originator_type.data, form.originator_id.data)
		flash("Post submitted")
	return form.redirect('index')
