import pymongo
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('web_cal')

col_user = db.get_collection('user')
col_loc = db.get_collection('location')
col_part = db.get_collection('participant')
col_event = db.get_collection('event')
col_reserved = db.get_collection('reserved')


col_user.delete_many({})
col_loc.delete_many({})
col_part.delete_many({})
col_event.delete_many({})
col_reserved.delete_many({})

#불러오는 것
user = [{'user_id':0, 'email': 'cbchoi@handong.edu', 'rank':0}, 
{'user_id':1, 'email': '21900000@handong.edu', 'rank':0},
{'user_id':2, 'email': '21900001@handong.edu', 'rank':0},
{'user_id':3, 'email': '21900002@handong.edu', 'rank':0}]
col_user.insert_many(user)

reserved = [{'event_id': 10, 'date': '20191124', 'start_time': 2030, 'end_time': 2130, 'location_ID': 7, 'type': 2, 'user_id' : 1}]
col_reserved.insert_many(reserved)


#파일 안에 만들어져 있는것
loc = [ {'loc_id':0, 'loc_name':'Ebenezer', 'loc_capacity':4},
 {'loc_id':1, 'loc_name':'Ebenezer', 'loc_capacity':4}, {'loc_id':2, 'loc_name':'Ebenezer', 'loc_capacity':4}]
col_loc.insert_many(loc)






#일정 초기 생성
event = [{'event_id': 0, 'date':'_','start_time':0,'end_time':0, 'loc_id':'-','type':'-'}]
col_event.insert_many(event)

#일정 값 입력
col_event.update_one({'event_id':0}, { '$set': {'date' : '20191122'} })
col_event.update_one({'event_id':0}, { '$set': {'start_time' : 2130} })
col_event.update_one({'event_id':0}, { '$set': {'end_time' : 2230} })
col_event.update_one({'event_id':0}, { '$set': {'loc_id' : 1} })
col_event.update_one({'event_id':0}, { '$set': {'type' : 2} })



#print(col_event.find_one({'event_id' : 0}))

#일정 저장
col_reserved.insert_one(col_event.find_one({'event_id' : 0}))
col_reserved.update_one({'event_id':0}, { '$set' : {'user_id':0}})

results = col_reserved.find()
[print(result) for result in results] 


print(col_reserved.find().count())
