from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort

#import time
import time

# Import forms
import app.plans.forms as forms

# Import models
import app.plans.models as models

# Create blueprint for plans routes
plans = Blueprint('plans', __name__)

# Display plan

@plans.route('/')
def plan():
	return render_template('plans/index.html', plan=models.all_plans())

@plans.route("/<id>/")
def show_plan(id):
	"""Display an individual plan by ID"""
	plan = models.find_plan(id)
	if plan is None:
		abort(404)
	#Do additional things if needed
	return render_template("plans/show-plan.html", plan=plan)

@plans.route("/add/", methods=["GET", "POST"])
def add_plan():
	add_plan_form = forms.AddPlan()
	if add_plan_form.validate_on_submit():
		rowcount = models.add_plan_to_db( add_plan_form.author.data,
											 add_plan_form.name.data,
											 add_plan_form.description.data)
		if rowcount == 1:
			flash('Plan Added')
			return redirect(url_for('plans.indiv-plan'))
		else:
			flash("Plan not added.")
		#else:
			#flash("Plan '{}' already exists".format(add_plan_form.id.data))
	return render_template('plans/show-plan.html', form=add_plan_form)

@plans.route("/add_reading/", methods=["GET", "POST"])
def add_reading_to_plan():
	add_reading_to_plan_form = forms.AddReadingToPlan()
	preview_plan_form = forms.PreviewPlan()
	if add_reading_to_plan_form.validate_on_submit():
		startTime= models.add_readings_to_plan_reading(add_reading_to_plan_form.start_time.data)
		endTime=models.add_readings_to_plan_reading(add_reading_to_plan_form.end_time.data)
		currentTime= time.time()
		#convert startTime str to integer,startTimeInt
		#convert endTime str to integer, endTimeInt
		#if startTimeInt<currentTime
		#	flash('start time must be a future time')
		#if endTimeInt<currentTime
		#   flash('end time must be a future time')
		#if endTimeInt<=startTimeInt
		#	flash('end time must be greater than start time')
		#else:
		#redisplay
	#want to re-display preview with new reading as the next row in the preview table, n
	return render_template('plans/show-plan.html', form=preview_plan_form)

