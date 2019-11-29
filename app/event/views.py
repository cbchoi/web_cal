from datetime import *
import pymongo


from ..models import User
from .forms import NameForm, UpdateForm, CreateButton
from . import event

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap

from flask_login import login_user, login_required, logout_user, current_user
from .. import db

'''
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database("events")
collection = db.get_collection('time')

conn2 = pymongo.MongoClient('mongodb://db:27017')
db1 = conn2.get_database("events")
collection2 = db.get_collection("location")


results = collection.find()
[print(result) for result in results]
print(results)
'''

# app = Flask(__name__)
# ######
# app.config['SECRET_KEY'] = 'hard to guess string'
# ######

# bootstrap = Bootstrap(app)


######


def set_Mongo():
	conn = pymongo.MongoClient('mongodb://db:27017')
	db = conn.get_database('web_cal')
	col_event = db.get_collection('event')
	#col_event.delete_many({})
	#print(col_event.find())
	return col_event

def Make_event(form):

	year = form.year.data
	month = form.month.data
	day = form.day.data
	date = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
	date_num = int(str(year) + str(month).zfill(2) + str(day).zfill(2))
	

	schedules = form.schedules.data
	location = form.location.data
	name = date+","+schedules

	return name, date, date_num, location, schedules


@event.route('/', methods=['GET', 'POST'])
@login_required
def index():
	form = CreateButton()
	col_event = set_Mongo()
	#col_event.delete_many({})
	results = [result for result in col_event.find({"username":current_user.username})]
	print(results)

	unsorted_results = [result for result in col_event.find({"username":current_user.username})]
	results = sorted(unsorted_results, key=lambda a: a['date_num'])
	#print(results)
	# today_date_num = date.today().year*10000 + date.today().month*100 + date.today().day
	# future_event = []
	# for i in results:
	# 	if i["date_num"] >= today_date_num:
	# 		future_event.append(i)

	names = [result["name"] for result in col_event.find({"username":current_user.username})]
	chk_lst = []
	n = len(results)


	if form.validate_on_submit():
		return redirect(url_for('.create'))

	if request.method == "POST":
		print("POST")
		if request.form['submit_button'] == "date range":
			results = date_range(results)
			n = len(results)
			#if n < 1:
			#	flash("Date range is wrong")
			#	return redirect(url_for('.index'))
		# elif request.form['submit_button'] == "show all":
		# 	future_event = results
		elif request.form['submit_button'] == "Delete":
			print("Delete")
			col_event.delete_one({'name':request.form.get("name")})
			return redirect(url_for('.index'))
		elif request.form['submit_button'] == "Revise":
			print("Revise")
			return redirect(url_for('.update', req_name=request.form.get("name")))
		else:
			pass
	return render_template('event/main.html', results = results, form = form, len = n, year = date.today().year)

def date_range(event):
	selected_date = []
	date_from = 0
	date_to = 0
	selected_event = []

	selected_date = request.form.getlist("date range")
	date_from = int(selected_date[0]) * 10000 + int(selected_date[1]) * 100 + int(selected_date[2])
	date_to = int(selected_date[3]) * 10000 + int(selected_date[4]) * 100 + int(selected_date[5])
	for i in event:
		if i["date_num"] >= date_from and i["date_num"] <= date_to:
			selected_event.append(i)
	return selected_event

@event.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	form = NameForm()
	#d_button = DeleteButton()
	#events = []
	if form.validate_on_submit():
		flash('added a new schedules')
		col_event = set_Mongo()
		name, date, date_num, location, schedules = Make_event(form)

		col_event.insert_one({"name": name, "date":date, "date_num":date_num, "location": location, "schedules": schedules, "username":current_user.username})
		results = col_event.find()
		return redirect(url_for('.index'))
	return render_template('event/create.html',  form = form,
		year = session.get('year'), month = session.get('month'),
		day = session.get('day'), location = session.get('location'), schedules = session.get('schedules'))

@event.route('/update/<req_name>', methods=['GET', 'POST'])
@login_required
def update(req_name):
	col_event = set_Mongo()
	form = UpdateForm()
	old_name = col_event.find_one({"name":req_name})
	if form.validate_on_submit():
		flash('revised a new schedules')	
		name, date, date_num, location, schedules = Make_event(form)

		#form.schedules.data = ''
		col_event.update_one({"name":req_name}, {'$set': {"name": name, "date":date, "date_num":date_num, "location": location, "schedules": schedules, "username":current_user.username}})
		results = col_event.find()

		return redirect(url_for('.index'))
	return render_template('event/update.html',  form = form, old_name = old_name,
		year = session.get('year'), month = session.get('month'),
		day = session.get('day'), location = session.get('location'), schedules = session.get('schedules'))



#@app.route('/user/<name>')
#def user(name):
#	return render_template('user.html', name=name)

# if __name__ == '__main__':
# 	app.run(debug=True, host='0.0.0.0')
