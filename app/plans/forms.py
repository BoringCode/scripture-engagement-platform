from wtforms.widgets import TableWidget
from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Email, Length
from flask.ext.admin.form.widgets import DatePickerWidget

class AddPlan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)])
    description = TextAreaField('Description of Plan', validators=[Length(min=1,max=1000)])
    creation_time = DateField("Today's Date (yyyy/mm/dd)")
    submit = SubmitField('Add Plan to Database')

class AddReadingToPlan(Form):
    name = StringField('Plan Name', validators=[Length(min=1,max=40)])
    #need reading_id from the dropdown here
    #need to figure out DatePickerWidget
    start_time = DateField ('Start', format='%m/%d/%Y')
    end_time = DateField('End',format='%m/%d/%Y')
    submit = SubmitField('Add Reading to Plan')

class PreviewPlan(Form):
    reading_table = TableWidget()
    reading_name = StringField(widget=reading_table)
    start_time = DateField ('Start', format='%m/%d/%Y', widget=reading_table)
    end_time = DateField('End',format='%m/%d/%Y', widget=reading_table)

