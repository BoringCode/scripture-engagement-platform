from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort

# Import forms
import app.readings.forms as forms

# Import models
import app.readings.models as models

# Create blueprint for readings routes
readings = Blueprint('readings', __name__)

# Display readings
@readings.route('/')
def all_readings():
	return render_template('readings/index.html', readings=models.all_readings())

@readings.route("/<id>/")
def show_reading(id):
	"""Display an individual reading by ID"""
	reading = models.find_reading(id)
	if reading is None:
		abort(404)
	#Do additional things if needed
	return render_template("readings/show-reading.html", reading=reading)

@readings.route("/add/", methods=["GET", "POST"])
def add_reading():
	add_reading_form = forms.AddReading()
	if add_reading_form.validate_on_submit():
		rowcount = models.add_reading_to_db( add_reading_form.name.data,
											 add_reading_form.creation_time.data,
											 add_reading_form.text.data,
											 add_reading_form.BG_passage_reference.data)
		if rowcount == 1:
			flash('Reading Added')
			return redirect(url_for('readings.all_readings'))
		else:
			flash("Reading not added.")
		#else:
			#flash("Reading '{}' already exists".format(add_reading_form.id.data))
	return render_template('readings/add-reading.html', form=add_reading_form)






