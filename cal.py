import pymongo
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('web_cal')

col_user = db.get_collection('user')

col_user.delete_many({})

user = [{'user_id':0, 'email': 'cbchoi@handong.edu', 'rank':0}]
col_user.insert_many(user)
