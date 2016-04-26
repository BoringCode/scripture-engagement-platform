from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
import wtforms.validators as validators
import re

#Custom validator for password
class PasswordRequired(object):
    def __init__(self, min=-1, pattern='^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{1,}$', message=None):
        self.min = min
        self.pattern = pattern

        if not message:
            message = u'Password must be at least %i characters long and must contain at least one letter, digit, and special character.' % (min)
        self.message = message

    def __call__(self, form, field):
        length = field.data and len(field.data) or 0
        #Check length and whether it matches the pattern
        if length < self.min or not(re.match(self.pattern, field.data)):
            raise validators.ValidationError(self.message)

class Login(Form):
    email = StringField('Email', validators=[validators.Email(), validators.Required()])
    password = PasswordField("Password", validators=[validators.Required()])
    submit = SubmitField('Login')

class Register(Form):
	email = StringField('Email', validators=[validators.Email(), validators.Required()])
	first_name = StringField("First Name", validators=[validators.Required()])
	last_name = StringField("Last Name", validators=[validators.Required()])
	password = PasswordField("Password", [validators.InputRequired("Password is required"), PasswordRequired(min=8), validators.EqualTo("password_confirm", message = "Passwords must match.")])
	password_confirm = PasswordField("Confirm Password", [validators.InputRequired("Please confirm your password"), PasswordRequired()])
	submit = SubmitField('Login')