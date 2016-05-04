from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Email, Length

class AddReading(Form):
	#id = StringField('Reading Number', validators=[Length(min=1, max=6)])
	name = StringField('Reading Name', validators=[Length(min=1,max=40)])
	text = TextAreaField('Description of Reading', validators=[Length(min=1, max=500)])
	translation = SelectField('Translation', choices=[('KJV', 'KJV'), ('NKJV', 'NKJV')])
	submit = SubmitField('Add Reading to Database')

class AddPassage(Form):
	#reading_id = StringField('Reading ID')
	BG_passage_reference = StringField('Passage Reference', validators=[Length(min=1,max=50)])
	finished = SelectField('Would you like to add more passages besides this one?', choices=[('yes','yes'), ('no','no')])
	submit = SubmitField('Add Passage to Reading')

class AddContentToReading(Form):
    content_select = SelectField('Select Content')
    submit = SubmitField('Add Content to Reading')

    def set_choices(self):
        allContent=all_content()
        content = [[0,'select...']]
        for content in allContent:
            content.append([str(content["id"]),content["name"]])
        self.content_select.choices = content
