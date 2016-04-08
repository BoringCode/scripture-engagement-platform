from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Email, Length

class AddReading(Form):
	#id = StringField('Reading Number', validators=[Length(min=1, max=6)])
	name = StringField('Reading Name', validators=[Length(min=1,max=40)])
	text = TextAreaField('Description of Reading', validators=[Length(min=1, max=500)])
	BG_passage_reference = StringField('Passage Reference', validators=[Length(min=1,max=50)])
	submit = SubmitField('Add Reading to Database')
