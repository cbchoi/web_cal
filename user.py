from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


from datetime import datetime

import pymongo

conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('web_cal')

col_user = db.get_collection('user')

col_user.delete_many({})

user = [{'user_id':0, 'email': '21400488@handong.edu', 'username': 'yire', 'password_hash': '','member_since': '_', 'last_seen': '_', 'confirmed': True,'rank':0}]
col_user.insert_many(user)

results = col_user.find()
[print(result) for result in results] 

class User(UesrMixin, object):
	user_id = col_user.find().count() #회원탈퇴는 일단 고려하지 않음. 
	email = ""
	username = ""
	password_hash = ""
	member_since = ""
	last_seen = ""
	confirmed = False
	rank = None

	def __init__(self, email, username, password):
		self.email = email
		self.username = username
		self.password = password

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@login_manager.user_loader
	def load_user(user_email):
		col_user = db.get_collection('user')
		results = col_user.find_one({'email':email})
		if results is not None:
			user = User(results['email'], "", "") # 20191112
			user.from_dict(results)
			return user
		else:
			return None

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.email}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.email:
			return False
		self.confirmed = True
		collection = db.get_collection('user')
		results = collection.update_one({'email':self.email}, {'$set':{'confirmed':self.confirmed}})
		return True

	def ping(self):
		self.last_seen = datetime.utcnow()
		col_user = db.get_collection('user')
		results = col_user.update_one({'email': self.email}, {'$set':{'last_seen':self.last_seen}})

	def to_dict(self):
		dict_user = {
			'email': self.email, 
			'username':self.username,
			'password_hash':self.password_hash,
			'member_since':self.member_since,
			'last_seen':self.last_seen,
			'confirmed': self.confirmed
			'rank':self.rank
		}
		return dict_user

	def from_dict(self, data):
		if data is not None:
			self.email = data['email']
			self.username = data['username']
			self.password_hash = data['password_hash']
			self.member_since = data.get('member_since')
			self.last_seen = data.get('last_seen')
			self.rank = data["rank"],
			self.confirmed = data['confirmed']

