from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Email, Length

class AddPlan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)])
    description = TextAreaField('DeSCription of Plan', validators=[Length(min=1,max=1000)])
    creation_time = DateField("Today's Date (yyyy/mm/dd)")
    submit = SubmitField('Add Plan to Database')