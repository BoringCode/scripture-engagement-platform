from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort
import time
from datetime import datetime
from wtforms import ValidationError

# Import forms
import app.plans.forms as forms

# Import models
import app.plans.models as models

# Create blueprint for plans routes
plans = Blueprint('plans', __name__)

# Display all plan
@plans.route('/')
def plan():
	return render_template('plans/index.html', plans=models.all_plans())

# Display individual plan
@plans.route("/<id>/")
def show_plan(id):
	"""Display an individual plan by ID"""
	plan = models.find_plan(id)
	if plan is None:
		abort(404)
	readings = models.find_plan_reading(id)
	return render_template("plans/show-plan.html", plan = models.find_plan(id), readings = readings)


# Add new plan
@plans.route("/add/", methods=["GET", "POST"])
def add_plan():
	add_plan_form = forms.Plan()
	if add_plan_form.validate_on_submit():
		returnValue = models.add_plan_to_db(	 add_plan_form.name.data,
											 add_plan_form.description.data)
		if returnValue is not None:
			flash('Plan Added')
			return redirect(url_for('plans.show_plan',id=returnValue))
		else:
			flash("Plan not added.")
		#else:
			#flash("Plan '{}' already exists".format(add_plan_form.id.data))
	return render_template('plans/add-plan.html', form=add_plan_form)

# View Edit Plans page
@plans.route('/edit/')
def edit_plans():
	return render_template('plans/edit-plans.html', plans=models.all_plans())


class ObjectCreator:
	def __init__(self, sqlite_row):
		self.values_dict = self.make_dict_from_values(sqlite_row)
		self.__dict__.update(self.values_dict)

	def make_dict_from_values(self, sqlite_row):
		keys = sqlite_row.keys()
		values_d = {}
		for key in keys:
			values_d[key] = sqlite_row[key]
		return values_d


# View individual plan you want to edit
@plans.route("/<id>/edit/", methods = ['GET', 'POST'])
def edit_show_plan(id):
	plan = models.find_plan(id)
	if plan is None:
		abort(404)

	edit_plan_form = forms.UpdatePlan(obj=ObjectCreator(plan))
	if edit_plan_form.validate_on_submit():  #  This function is saying whether this is a post request
		if edit_plan_form.cancel.data:
			return redirect(url_for('plans.edit_plans'))

		returnValue = models.update_plan(edit_plan_form.name.data, edit_plan_form.description.data, id)
		if returnValue is not None:
			flash('Plan Updated')
			return redirect(url_for('plans.show_plan', id=id))
		else:
			flash("Plan Not Updated")
	return render_template("plans/edit-show-plan.html", id= plan, plan = models.find_plan(id), form=edit_plan_form)


@plans.route("/<id>/add-reading/", methods=["GET", "POST"])
def add_reading_to_plan(id):
	#remove line ater add plan form submit passes it
	plan = models.find_plan(id)
	if plan is None:
		abort(404)

	add_reading_to_plan_form = forms.AddReadingToPlan()
	add_reading_to_plan_form.set_choices()
	if add_reading_to_plan_form.validate_on_submit():
		startTime= add_reading_to_plan_form.start_time.data
		endTime= add_reading_to_plan_form.end_time.data
		reading_id= add_reading_to_plan_form.reading_select.data
		creationTimeInt = plan["creation_time"]

		creationTime = datetime.fromtimestamp(creationTimeInt).strftime('%m/%d/%Y')

		#convert startTime str to integer,startTimeInt
		startTimeInt = time.mktime(startTime.timetuple())

		#convert endTime str to integer, endTimeInt
		endTimeInt = time.mktime(endTime.timetuple())

		timeValidFlag = True
		if startTimeInt<creationTimeInt:
			timeValidFlag = False
			message = ('start time must be after '+ creationTime)
			raise ValidationError(message)
		if endTimeInt<creationTimeInt:
			timeValidFlag = False
			message = ('end time must be after '+ creationTime)
			raise ValidationError(message)
		if endTimeInt<startTimeInt:
			timeValidFlag = False
			raise ValidationError('start time must precede end time')
		if timeValidFlag == True:
			start_time_offset=startTimeInt-creationTimeInt
			end_time_offset=endTimeInt-creationTimeInt
			returnValue = models.add_readings_to_plan_reading(id, reading_id, startTimeInt, endTimeInt)
			if returnValue is not None:
				flash('Reading Added')
				return redirect(url_for('plans.show_plan', id=id))
		else:
			flash("Reading not added.")
	return render_template('plans/add-reading-to-plan.html', form=add_reading_to_plan_form, plan = models.find_plan(id))