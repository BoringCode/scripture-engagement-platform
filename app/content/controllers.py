from flask import Blueprint, render_template, flash, redirect, url_for

#Import forms
import app.content.forms as forms

#Import models
import app.content.models as models

import app.readings.models as reading_models

content = Blueprint('content', __name__)

# display add reading form
@content.route("/add/", methods=["GET", "POST"])
def add_content():
	add_content_form = forms.AddContent()
	if add_content_form.validate_on_submit():
		rowcount = models.add_content_to_db( add_content_form.name.data,
											 add_content_form.creation_time.data,
											 add_content_form.approved.data,
											 add_content_form.content.data)
		if rowcount == 1:
			flash('Content Added')
			return redirect(url_for('content.all_content'))
		else:
			flash("Content not added.")
	return render_template('content/add-content.html', form=add_content_form)