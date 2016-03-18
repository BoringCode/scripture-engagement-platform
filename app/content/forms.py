from flask.ext.wtf import Form
from wtforms import StringField, TextField, SubmitField, SelectField, DateTimeField
from wtforms.validators import Email, Length

class AddContent(Form):
    name = StringField('Content Name', validators=[Length(min=1,max=40)])
    creation_time = DateTimeField('Creation Date')
    approved = SelectField('Approved?', choices=[('Approved','approved'), ('Not Approved', 'not approved')])
    content = StringField('Link to Content', validators=[Length(min=1, max=500)])
    submit = SubmitField('Add Content to Database')

