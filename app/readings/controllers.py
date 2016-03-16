from flask import Blueprint, render_template, flash, redirect, url_for

# Import forms
import app.readings.forms as forms
# Import models
import app.readings.models as models

# Create blueprint for readings routes
readings = Blueprint('readings', __name__)

# Display index page
@readings.route('/')
def index():
	flash("Welcome")
	return render_template('readings/index.html')

@readings.route("/add-reading/", methods=["GET", "POST"])
def add_reading():
	form = forms.AddReading()

	if form.validate_on_submit():
		flash("Cool")

	return render_template("readings/add-reading.html", form=form)


@readings.route("/indiv_reading/", methods=["GET", "POST"])
def indiv_reading():
	form = forms.IndivReading()

	if form.validate_on_submit():
		flash("Finished")

	return render_template("readings/indiv_reading.html", form=form)
