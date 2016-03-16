from flask.ext.wtf import Form
from wtforms import StringField, TextField, SubmitField, SelectField, DateTimeField
from wtforms.validators import Email, Length

class AddReading(Form):
	id = TextField('Reading Number', validators=[Length(min=1, max=6)])
	name = TextField('Reading Name', validators=[Length(min=1,max=40)])
	creation_time = DateTimeField('Creation Data', validators=[Length(min=4, max=10)])
	text = TextField('Description of Reading', validators=[Length(min=1, max=500)])
	BG_passage_reference = TextField('Passage Reference', validators=[Length(min=1,max=50)])
	submit = SubmitField('Add Reading to Database')

class IndivReading(Form):
	id = TextField('Reading Number')
	name = TextField('Reading Name')
	creation_time = DateTimeField('Creation Data')
	text = TextField('Description of Reading')
	BG_passage_reference = TextField('Passage Reference')
	submit = SubmitField('Done Reading')