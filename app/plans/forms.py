from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField, FormField
from wtforms.validators import Length
from wtforms.widgets import TableWidget
from flask.ext.admin.form.widgets import DatePickerWidget



class AddReadingToPlan(Form):
    reading_select = SelectField(u'Select Reading')
    start_time = DateField ('Start', format='%m/%d/%Y')
    end_time = DateField('End',format='%m/%d/%Y')
    submit = SubmitField('Add Reading to Plan')

    def set_choices(self):
        from app.readings.models import all_readings
        allReadings=all_readings()
        readings = [[0,'select...']]
        for reading in allReadings:
            readings.append([reading.id,reading.name])
        self.reading_select.choices = readings

class PreviewPlan(Form):
   reading_table = TableWidget()
#   reading_name = StringField(widget=reading_table)
#   preview_start_time = DateField ('Start', format='%m/%d/%Y', widget=reading_table)
#   preview_end_time = DateField('End',format='%m/%d/%Y', widget=reading_table)

class AddPlan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)])
    description = TextAreaField('Description of Plan', validators=[Length(min=1,max=1000)])
    submit = SubmitField('Add Plan to Database')


