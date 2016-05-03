from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort
import time
from datetime import datetime
from wtforms import ValidationError

# Import forms
import app.groups.forms as forms

# Import models
import app.groups.models as models

# Create blueprint for plans routes
groups = Blueprint('groups', __name__)

# Display all groups
@groups.route('/')
def group ():
	return render_template('groups/show-all-groups.html', groups=models.all_groups())

# Display individual group
@groups.route("/<id>/")
def show_group(id):
	"""Display an individual group by ID"""
	group = models.find_group(id)
	if group is None:
		abort(404)
	users = models.all_users_in_group(id)
	return render_template("groups/show-group.html", group = models.find_group(id), users = users)


@groups.route("/<id>/add-user-to-group/", methods=["GET", "POST"])
def add_user_to_group(id):
	group = models.find_group(id)
	if group is None:
		abort(404)

	add_user_to_group_form = forms.AddUserToGroup(id)
	add_user_to_group_form.set_choices()

	if add_user_to_group_form.validate_on_submit():
		user_id= add_user_to_group_form.user_select.data
		returnValue = models.add_user_to_group(id, user_id)
		if returnValue is not None:
			flash('User added to group')
			return redirect(url_for('groups.show-group', id=id))
		else:
			flash("User not added to group.")
	return render_template('groups/add-user-to-group.html', form=add_user_to_group_form, group = models.find_group(id))