from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort
import flask.ext.login as flask_login
import app.content.forms as forms
from .. object_creator import ObjectCreator

#Import models
import app.content.models as models

import app.readings.models as reading_models

content = Blueprint('content', __name__)

# display add reading form
@content.route("/add/", methods=["GET", "POST"])
@flask_login.login_required
def add_content():
	add_content_form = forms.AddContent()
	if add_content_form.validate_on_submit():
		rowcount = models.add_content_to_db( add_content_form.name.data,
											 add_content_form.approved.data,
											 add_content_form.description.data)
		if rowcount == 1:
			flash('Content Added')
			return redirect(url_for('content.all_content'))
		else:
			flash("Content not added.")
	return render_template('content/add-content.html', form=add_content_form)

# Display all content
@content.route('/')
def all_content():
	return render_template('content/index.html', content=models.all_content())

# Display individual content
@content.route("/<id>/")
def view_content(id):
	"""Display an individual content by ID"""
	content = models.find_content(id)
	if content is None:
		abort(404)
	return render_template("content/show-content.html", content = models.find_content(id))

# View Edit Content page
@content.route('/edit/')
@flask_login.login_required
def edit_content():
	return render_template('content/edit-content.html', content=models.all_content())

# View individual content you want to edit
@content.route("/<id>/edit/", methods = ['GET', 'POST'])
@flask_login.login_required
def edit_show_content(id):
	content = models.find_content(id)
	if content is None:
		abort(404)

	edit_content_form = forms.UpdateContent(obj=ObjectCreator(content))
	if edit_content_form.validate_on_submit():  #  This function is saying whether this is a post request
		if edit_content_form.cancel.data:
			return redirect(url_for('content.edit_content'))


		if edit_content_form.delete.data:
			flash('Content Deleted')
			return redirect(url_for('content.all_content', id=id, content = models.delete_content(id)))


		returnValue = models.update_content(edit_content_form.name.data, edit_content_form.approved.data, edit_content_form.description.data, id)
		if returnValue is not None:
			flash('Content Updated')
			return redirect(url_for('content.all_content', id=id))
		else:
			flash("Content Not Updated")
	return render_template("content/edit-show-content.html", id= content, content = models.find_content(id), form=edit_content_form)