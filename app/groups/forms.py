from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from app.groups.models import all_users, all_users_in_group

class AddGroup(Form):
    group_name = TextField
    description = TextField
    submit = SubmitField('Add Group')

class AddUserToGroup(Form):
    user_select = SelectField('Select User')
    submit = SubmitField('Add User to Group')

    def set_choices(self, group_id):
        allUsers=all_users()
        allGroupUsers = all_users_in_group(group_id)
        users = [[0,'select...']]
        for user in allUsers:
            if user.id not in allGroupUsers.id:
                users.append([str(user["id"]),user.username["username"],user.last_name["lastname"],user.first_name["firstname"]])
        self.user_select.choices = users

class AddPlanToGroup(Form):
    user_select = SelectField('Select Plan')
    submit = SubmitField('Add Plan to Group')

    def set_choices(self, group_id):
        allPlans=all_plans()
        allPlansGroups = all_plans_in_group(group_id)
        plans = [[0,'select...']]
        for plan in allPlans:
            if plan.id not in allPlansGroups.id:
                plans.append([str(plan["id"]),plan.name["name"],plan.description["description"]])
        self.plan_select.choices = plans

class ShowAllGroups(Form):
    #List Groups on Static Page??
    group_name = TextField
    description = TextField
    submit = SubmitField('Add Group')

class ShowGroup(Form):
    #List Group Details from DB.
    group_name = TextField
    description = TextField
    submit = SubmitField('Add Group')