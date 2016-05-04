from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Length
from app.readings.models import all_readings


class Plan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)],)
    description = TextAreaField('Description of Plan', validators=[Length(min=1,max=1000)])
    submit = SubmitField('Add Plan to Database')

class UpdatePlan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)],)
    description = TextAreaField('Description of Plan', validators=[Length(min=1,max=1000)])
    submit = SubmitField('Update Plan')
    delete = SubmitField('Delete Plan')
    cancel = SubmitField('Cancel')

class AddReadingToPlan(Form):
    reading_select = SelectField('Select Reading')
    start_time = DateField ('Start', format='%m/%d/%Y')
    end_time = DateField('End',format='%m/%d/%Y')
    submit = SubmitField('Add Reading to Plan')

    def set_choices(self):
        allReadings=all_readings()
        readings = [[0,'select...']]
        for reading in allReadings:
            readings.append([str(reading["id"]),reading["name"]])
        self.reading_select.choices = readings

