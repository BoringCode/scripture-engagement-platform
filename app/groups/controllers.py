from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import abort
import time
from datetime import datetime
from wtforms import ValidationError

# Import forms
import app.groups.forms as forms

# Import models
import app.groups.models as models

# Import posts
import app.posts.forms as posts_forms

# Create blueprint for groups routes
groups = Blueprint('groups', __name__)

# Display all groups
@groups.route('/')
def group():
	return render_template('groups/show-all-groups.html', groups=models.all_groups())

# Display individual group
@groups.route("/<id>/")
def show_group(id):
	"""Display an individual group by ID"""
	group = models.find_group(id)
	if group is None:
		abort(404)
	users = models.all_users_in_group(id)
	posts = models.get_posts(id)
	post_form = posts_forms.NewPost(originator_type="group", originator_id=id)
	return render_template("groups/show-group.html", group = models.find_group(id), users = users, posts=posts, post_form=post_form)


#Display add groups page
@groups.route("/add/", methods=["GET", "POST"])
def add_group():
	add_group_form = forms.AddGroup()
	if add_group_form.validate_on_submit():
		rowcount = models.add_group_to_db(   len(models.all_groups()),
                                             add_group_form.group_name.data,
											 add_group_form.public.data,
											 add_group_form.description.data)
		if rowcount is not None:
			flash('Group Added')
			return redirect(url_for('groups.show_group', id = rowcount))
		else:
			flash("Group not added.")
	return render_template('groups/add-group.html', form=add_group_form)

#View add user to group page
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

#View add plan to group page
@groups.route("/<id>/add-plan-to-group/", methods=["GET", "POST"])
def add_plan_to_group(id):
	group = models.find_group(id)
	if group is None:
		abort(404)

	add_plan_to_group_form = forms.AddPlanToGroup(id)
	add_plan_to_group_form.set_choices()

	if add_plan_to_group_form.validate_on_submit():
		plan_id= add_plan_to_group_form.user_select.data
		returnValue = models.add_plan_to_group(id, plan_id)
		if returnValue is not None:
			flash('Plan added to group')
			return redirect(url_for('groups.show-group', id=id))
		else:
			flash("Plan not added to group.")
	return render_template('groups/add-plan-to-group.html', form=add_plan_to_group_form, group = models.find_group(id))

# View Edit Groups page
@groups.route('/edit/')
def edit_group():
	return render_template('groups/edit-groups.html', groups=models.all_groups())


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

# View individual group you want to edit
@groups.route("/<id>/edit/", methods = ['GET', 'POST'])
def edit_show_group(id):
	group = models.find_group(id)
	if group is None:
		abort(404)

	edit_group_form = forms.UpdateGroup(obj=ObjectCreator(group))
	if edit_group_form.validate_on_submit():  #  This function is saying whether this is a post request
		if edit_group_form.cancel.data:
			return redirect(url_for('groups.edit_group'))

		returnValue = models.update_group(edit_group_form.name.data, edit_group_form.public.data, edit_group_form.description.data, id)
		if returnValue is not None:
			flash('Group Updated')
			return redirect(url_for('groups.show_group', id=id))
		else:
			flash("Group Not Updated")
	return render_template("groups/edit-show-group.html", id= group, group = models.find_group(id), form=edit_group_form)
