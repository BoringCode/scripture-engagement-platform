from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from app.groups.models import all_users, all_users_in_group

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