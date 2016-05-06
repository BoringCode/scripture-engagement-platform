from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Length
from app.content.models import all_content, associated_content


class AddReading(Form):
	name = StringField('Reading Name', validators=[Length(min=1,max=40)])
	text = TextAreaField('Description of Reading', validators=[Length(min=1, max=500)])
	translation = SelectField('Translation', choices=[('KJV', 'KJV'), ('NKJV', 'NKJV')])
	submit = SubmitField('Add Reading to Database')

class AddPassage(Form):
	BG_passage_reference = StringField('Passage Reference', validators=[Length(min=1,max=50)])
	finished = SelectField('Would you like to add more passages besides this one?', choices=[('yes','yes'), ('no','no')])
	submit = SubmitField('Add Passage to Reading')

class UpdateReading(Form):
	name = StringField('Reading Name', validators=[Length(min=1,max=40)])
	text = TextAreaField('Description of Reading', validators=[Length(min=1, max=500)])
	translation = SelectField('Translation', choices=[('KJV', 'KJV'), ('NKJV', 'NKJV')])
	submit = SubmitField('Update Reading')
	delete = SubmitField('Delete Reading')
	cancel = SubmitField('Cancel')

class AddContentToReading(Form):
	content_select = SelectField('Select Content')
	submit = SubmitField('Add Content to Reading')

	def set_choices(self, reading_id):
		allContent=all_content()
		already_used = [ac['content_id'] for ac in associated_content(reading_id)]
		contents = [[0,'select...']]
		for content in allContent:
			if content['id'] not in already_used:
				contents.append([str(content["id"]),content["name"]])
		self.content_select.choices = contents
