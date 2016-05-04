from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import Length

class AddContent(Form):
    name = StringField('Content Name', validators=[Length(min=1,max=40)])
    approved = SelectField('Approved?', choices=[('Approved','approved'), ('Not Approved', 'not approved')])
    description = StringField('Content Description', validators=[Length(min=1, max=500)])
    submit = SubmitField('Add Content to Database')

class UpdateContent(Form):
    name = StringField('Content Name', validators=[Length(min=1,max=40)],)
    approved = SelectField('Approved?', choices=[('Approved','approved'), ('Not Approved', 'not approved')])
    description = StringField('Content Description', validators=[Length(min=1, max=5000)])
    submit = SubmitField('Update Content')
    delete = SubmitField('Delete Content')
    cancel = SubmitField('Cancel')
