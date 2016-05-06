from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort
import flask.ext.login as flask_login

# Import forms
import app.readings.forms as forms

# Import models
import app.readings.models as models

# Import posts forms
import app.posts.forms as posts_forms

from app.scripture.bg_api import BGAPI

bg_api = BGAPI()

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
	# Grab discussion board
	reading_passages= models.find_reading_passages(id,reading["translation"])
	posts = models.get_posts(id)
	post_form = posts_forms.NewPost(originator_type="reading", originator_id=id)
	return render_template("readings/show-reading.html", reading=reading, verses=reading_passages, contents=models.all_reading_content(id), posts=posts, post_form=post_form)

@readings.route("/add/", methods=["GET", "POST"])
@flask_login.login_required
def add_reading():
	add_reading_form = forms.AddReading()
	if add_reading_form.validate_on_submit():
		rowcount = models.add_reading_to_db( add_reading_form.name.data,
											 add_reading_form.text.data,
											 add_reading_form.translation.data)
		if rowcount == 1:
			flash('Reading Added')
			return redirect(url_for('readings.all_readings'))
		else:
			flash("Reading not added.")
		#else:
			#flash("Reading '{}' already exists".format(add_reading_form.id.data))
	return render_template('readings/add-reading.html', form=add_reading_form)

@readings.route("/<id>/add-passage/", methods=["GET","POST"])
def add_passages(id):
	print(id)
	add_passages_form = forms.AddPassage()
	if add_passages_form.validate_on_submit():
		#reading = models.find_reading(add_passages_form.reading_id.data)
		if add_passages_form.finished.data == "yes":
			#if reading is None:
				#flash('There is no reading with that ID')
				#return redirect(url_for('readings.add_passages'))
			#else:
				rowcount = models.add_more_passages(id,
													add_passages_form.BG_passage_reference.data)
				if rowcount == 1:
					flash('Passage added to reading.')
					return redirect(url_for('readings.add_passages', id=id))
				else:
					flash("Passage not added")
		if add_passages_form.finished.data == "no":
			#if reading is None:
				#flash('There is no reading with that ID')
				#return redirect(url_for('readings.add_passages'))
			#else:
				rowcount = models.add_more_passages(id,
													add_passages_form.BG_passage_reference.data)
				if rowcount == 1:
					flash('Passage added to reading.')
					return redirect(url_for('readings.all_readings'))
		else:
			flash('Somethings terribly wrong.')
	return render_template('readings/add-passage.html', form=add_passages_form)





