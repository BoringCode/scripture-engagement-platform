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
	add_reading_form = forms.AddReading()
	if add_reading_form.validate_on_submit():
		reading = models.find_reading(add_reading_form.id.data)
		if reading is None:
			rowcount = models.add_reading_to_db(add_reading_form.id.data,
												 add_reading_form.name.data,
												 add_reading_form.creation_time.data,
												 add_reading_form.text.data,
												 add_reading_form.BG_passage_reference.data)
			if rowcount == 1:
				flash('Reading Added')
				return redirect(url_for('readings.all_readings'))
			else:
				flash("Reading not added.")
		else:
			flash("Reading '{}' already exists".format(add_reading_form.id.data))
	return render_template('readings/add-reading.html', form=add_reading_form)

@readings.route('/all-readings')
def all_readings():
	return render_template('readings/showmeallreadings.html', readings=models.all_readings())

	return render_template("readings/add-reading.html", form=form)


