from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, Required

class Login(Form):
    username = StringField('Username', validators=[Email(), Required()])
    password = PasswordField("Password", validators=[Required()])
    submit = SubmitField('Login')