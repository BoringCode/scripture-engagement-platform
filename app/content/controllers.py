from flask import Blueprint, render_template, flash, redirect, url_for

#Import forms
import app.content.forms as forms

#Import models
import app.content.models as models

content = Blueprint('content', __name__)

@content.route("/add-content", methods=["GET", "POST"])
def add_content():
	form = forms.AddContent()

	if form.validate_on_submit():
		flash("Cool")

	return render_template("content/add-content.html", form=form)

