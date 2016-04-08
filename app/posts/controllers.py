from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort

# Import forms
import app.posts.forms as forms

# Import models
import app.posts.models as models

# Create blueprint for readings routes
posts = Blueprint('posts', __name__)

@posts.route("/new/", methods=["POST"])
def new_post():
	form = forms.NewPost()
	if form.validate_on_submit():
		models.create_post(1, form.comment.data, form.originator_type.data, form.originator_id.data)
		flash("Post submitted")
	return form.redirect('index')
