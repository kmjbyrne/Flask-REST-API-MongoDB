


from pymongo import MongoClient


client = MongoClient()
db = client.test


db = client['gamesdb']

db['games']
db['players']
db['scores']

db['games'].insert_one(
	{
		"name": "test_user",
		"description": "TEST DATA"
	}
)
