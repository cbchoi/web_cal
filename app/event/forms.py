from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, length

from datetime import *

year = []
for i in range(date.today().year-10,date.today().year+10):
    year.append((str(i),str(i)))
month = []
for i in range(1,13):
    month.append((str(i),str(i)))
day = []
for i in range(1,32):
    day.append((str(i),str(i)))

hour = []
for i in range(0,24):
    hour.append((str(i),str(i)))
minute = []
for i in range(0,60):
    minute.append((str(i),str(i)))

class CreateForm(FlaskForm):
	date = StringField('date')
	#start = StringField('start')
	#end = StringField('end')
	#location = StringField('location')
	submit = SubmitField('Submit')

class NameForm(FlaskForm):
	#name = StringField('What is your schedules', validators=[Required()])
	    #validators=[Required()]
	#year = SelectField("년",choices = year,validators=[Required()],default=date.today().year)
	#month = SelectField("월", choices=month,validators=[Required()],default=date.today().month)
	#day = SelectField("일",choices = day,validators=[Required()],default=date.today().day)
	dt = DateField('날짜', format='%Y-%m-%d')

	hour = SelectField("시간",choices = hour,validators=[Required()])
	minute = SelectField("분",choices = minute,validators=[Required()])

	schedules = StringField('이벤트를 입력하세요', validators=[Required()])
	location = StringField('장소를 입력하세요', validators=[Required()])
	submit = SubmitField('추가')

class UpdateForm(FlaskForm):
	#year = SelectField("년",choices = year,validators=[Required()],default=date.today().year)
	#month = SelectField("월", choices=month,validators=[Required()],default=date.today().month)
	#day = SelectField("일",choices = day,validators=[Required()],default=date.today().day)
	dt = DateField('날짜', format='%Y-%m-%d')

	hour = SelectField("시간",choices = hour,validators=[Required()])
	minute = SelectField("분",choices = minute,validators=[Required()])

	schedules = StringField('이벤트를 입력하세요', validators=[Required()])
	location = StringField('장소를 입력하세요', validators=[Required()])
	submit = SubmitField('추가')
######

class RangeForm(FlaskForm):
	start_date = DateField('시작날짜', format = '%y-%-m-%d')
	end_date = DateField('마침날짜', format = '%y-%-m-%d')

	submit = SubmitField("찾기")

class CreateButton(FlaskForm):
    submit = SubmitField("일정만들기")
    #delete = SubmitField("삭제하기")