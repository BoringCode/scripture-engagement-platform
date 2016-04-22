from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Length


class Plan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)],)
    description = TextAreaField('Description of Plan', validators=[Length(min=1,max=1000)])
    submit = SubmitField('Add Plan to Database')

class UpdatePlan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)],)
    description = TextAreaField('Description of Plan', validators=[Length(min=1,max=1000)])
    submit = SubmitField('Update Plan')
    cancel = SubmitField('Cancel')

