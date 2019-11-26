from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from .. import db
from . import main
from .forms import NameForm
#from .. import db
from ..models import User
from flask_login import current_user

@main.route('/', methods=['GET', 'POST'])
def index():
	collection = db.get_collection('user')
	collection.update_one({'id':current_user.id},{'$set':{'last_seen':datetime.utcnow()}})
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('.index'))
	return render_template('index.html',
							form=form, name=session.get('name'),
							known=session.get('known', False),
							current_time=datetime.utcnow())


