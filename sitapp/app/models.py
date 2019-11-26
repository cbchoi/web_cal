from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 20191028
from . import login_manager, db

# 20191108
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

from datetime import datetime

class User(UserMixin, object):
	user_Id = 0 #회원탈퇴는 일단 고려하지 않음. 
	id = ""
	username = "yire"
	password_hash = ""
	member_since = ""
	last_seen = ""
	confirmed = False
	rank = ""

	def __init__(self, email, username, password):
		self.id = email
		self.username = username
		self.password = password

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@login_manager.user_loader
	def load_user(user_id):
		collection = db.get_collection('user')
		results = collection.find_one({'id':user_id})
		if results is not None:
			user = User("","","") # 20191112
			user.from_dict(results)
			return user
		else:
			return None

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		collection = db.get_collection('user')
		results = collection.update_one({'id':self.id}, {'$set':{'confirmed':self.confirmed}})
		return True

	def to_dict(self):
		dict_user = {
			'user_Id': db.get_collection('user').find().count(),
			'id': self.id, 
			'username':self.username,
			'password_hash':self.password_hash,
			'member_since':self.member_since,
			'last_seen':self.last_seen,
			'confirmed': self.confirmed,
			'rank': self.rank
		}
		return dict_user

	def from_dict(self, data):
		if data is not None:
			self.user_Id = data['user_Id']
			self.id = data['id']
			self.username = data['username']
			self.password_hash = data['password_hash']
			self.member_since = data.get('member_since')
			self.last_seen = data.get('last_seen')
			self.confirmed = data['confirmed'],
			self.rank = data["rank"]
			print(data)