from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class CreateForm(FlaskForm):
	date = StringField('date')
	#start = StringField('start')
	#end = StringField('end')
	#location = StringField('location')
	submit = SubmitField('Submit')
