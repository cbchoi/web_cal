from datetime import *
import pymongo
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, length

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database("events")
collection = db.get_collection('time')

conn2 = pymongo.MongoClient('mongodb://db:27017')
db1 = conn2.get_database("events")
collection2 = db.get_collection("location")

'''
results = collection.find()
[print(result) for result in results]
print(results)
'''

app = Flask(__name__)

######
app.config['SECRET_KEY'] = 'hard to guess string'
######

bootstrap = Bootstrap(app)


######

year = []
for i in range(date.today().year-10,date.today().year+10):
    year.append((str(i),str(i)))
month = []
for i in range(1,13):
    month.append((str(i),str(i)))
day = []
for i in range(1,32):
    day.append((str(i),str(i)))

class NameForm(FlaskForm):
    #name = StringField('What is your schedules', validators=[Required()])
        #validators=[Required()]
    year = SelectField("년",choices = year,validators=[Required()],default=date.today().year)
    month = SelectField("월", choices=month,validators=[Required()],default=date.today().month)
    day = SelectField("일",choices = day,validators=[Required()],default=date.today().day)
    schedules = StringField('이벤트를 입력하세요', validators=[Required()])
    location = StringField('장소를 입력하세요', validators=[Required()])
    submit = SubmitField('추가')
######

class DeleteButton(FlaskForm):
    submit = SubmitField("일정삭제")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    d_button = DeleteButton()
    events = []
    if form.validate_on_submit():
        flash('added a new schedules')
        session['year'] = form.year.data
        session['month'] = form.month.data
        session['day'] = form.day.data
        year = session.get('year')
        month = session.get('month')
        day = session.get('day')
        date = str(year) + "-" + str(month) + "-" + str(day)
        session['schedules'] = form.schedules.data
        event = session.get('schedules')
        session['location'] = form.location.data
        location = session.get('location')
        form.schedules.data = ''
        collection.insert_one({"date":date, "event": event})
        collection2.insert_one({"date":date, "location": location})
        return redirect(url_for('index'))
    return render_template('index.html',  form = form,
                           year = session.get('year'), month = session.get('month'),
                           day = session.get('day'), location = session.get('location'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


collection.find()