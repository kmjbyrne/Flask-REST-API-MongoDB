# - Author: Keith Michael Byrne
# - Date Completed: 19/02/2015
# - Aegis of: Institute of Technology Carlow

# - Synopsis: 	RESTful API for database schema gamesdb
# -				and can be easily configured for use on any
# -				database schema (Mongo) by reassigning db on global
# -				definitions under CONFIG SETTINGS

# - Date of Submission: 19/02/2015 00:00
# - Python Data: Version 3.4
# - Dependencies: Flask, pymongo
# - 	See also lib modules for errors and collection+JSON object

# - Supervisor: Paul Barry
# - Successful implementation on: Windows 7/8, Raspberry Pi (Debian) & Linux Mint



from flask import Flask,render_template,jsonify,url_for,request,session,flash, json, Response
from urllib.parse import urlparse
import lib, json
from functools import wraps
import mysql.connector
from bson.objectid import ObjectId
from pymongo import MongoClient
from lib.collection import Structure
from lib.errors import *
import datetime

# HTTP Request Detail
# TYPE : API Feature

# GET /table/list
# GET /table/structure (Deprecated from v1.x +)
# GET /table/showall
# POST /table/post
# GET /table/showone

app = Flask(__name__)

#######################
### CONFIG SETTINGS ###
#######################

host = 'localhost'
password = 'gamesadminpasswd'
user = 'gamesadmin'
db = 'GamesDB'


client = MongoClient()
mongo_db = client['FantasyDB']

#######################
### HTTP metadata	###
#######################

content_type = 'application/vnd.collection+json'

#######################
###	API root [home] ###
#######################

api_root = '/table'

###############################################
####	Test data functions from ex 	#######
###############################################

def testItems():
	friends = []
	item={}
	item['name'] = 'mildred'
	item['email'] = 'mildred@example.com'
	item['blog'] = 'http://example.com/blogs/mildred'
	friends.append(item);

	item['name'] = 'mildred'
	item['email'] = 'mildred@example.com'
	item['blog'] = 'http://example.com/blogs/mildred'
	friends.append(item)

	item['name'] = 'mildred'
	item['email'] = 'mildred@example.com'
	item['blog'] = 'http://example.com/blogs/mildred'
	friends.append(item)

	item['name'] = 'mildred'
	item['email'] = 'mildred@example.com'
	item['blog'] = 'http://example.com/blogs/mildred'
	friends.append(item)

	item['name'] = 'mildred'
	item['email'] = 'mildred@example.com'
	item['blog'] = 'http://example.com/blogs/mildred'
	friends.append(item)

	return friends

###############################################
##### 	Standard functions & Test Data ########
###############################################

def describeAPI(url):
	links = []
	links.append(generateLink(getCurrentPath(url, '/table/list'), 'list tables'))
	links.append(generateLink(getCurrentPath(url, '/table/<table>'), '[GET] post to table'))
	links.append(generateLink(getCurrentPath(url, '/table/showall/<table>'), 'show all from table'))
	links.append(generateLink(getCurrentPath(url, '/table/showone/<table>/<unique_href>'), 'show one from table'))
	links.append(generateLink(getCurrentPath(url, '/table/<table>'), '[POST] post to table'))

	return links

def generateLink(link, rel):
	link_item = {}
	link_item['href'] = link
	link_item['rel'] = rel
	return link_item

def getCurrentPath(url, mod_path):
	parsed = urlparse(url)
	href = ''
	if(mod_path is None):
		href = ''.join(parsed.scheme, "://", parsed.netloc, parsed.path)
	else:
		href = ''.join([parsed.scheme, '://', parsed.netloc, mod_path])
	return href

def linksDefault(path):
    links = []
    dict = {'rel': 'home', 'href': path + "/list"}
    links.append(dict)
    return links



###############################################################
###### MongoDB : PyMongo Query Functions ######################
###############################################################

"""

Below functions handle features of MongoDB Orm PyMongo

"""

def describeObject(obj_name):
	db = client['FantasyDB']
	documents = db[obj_name].find()
	exp = documents.explain()
	data = []

	for element in documents:
		for key, value in element.items():
			try:
				if('id' in key):
					data.append(generateNameValuePair(key, str(type(value))))
				else:
					data.append(generateNameValuePair(key, str(type(value))))
			except Exception as e:
				data.append(generateNameValuePair(key, str(type(value))))

		return data
	return data

def mongoDBQuery(obj_name):
		db = client['FantasyDB']
		cursor = db[obj_name].find()

		db['games'].insert_one(
			{
				"name": "test",
				"description": "test-test-test-test"
			})
		db['games'].insert_one(
			{
				"name": "2323",
				"description": "adsrgsdfgsdfg-test-test-test"
			})

		return cursor

def mongoGetCollections():
	try:
		db = client['FantasyDB']
		cursor = db.collection_names()
		return cursor
	except Exception as e:
		return None

def mongoInsertData(obj_name, input_data):
	db = client['FantasyDB']
	db = db[obj_name]
	insert_dict = {}
	for item in input_data['template']['data']:
		if('date' in item['prompt'] or 'time' in item['prompt']):
			print(item['value'])
			parse_out = item['value'].split(",")
			date_formed = [int(i) for i in parse_out]
			insert_dict["{0}".format(item['name'])] = datetime.datetime(*date_formed)

		elif(item['prompt'] == 'list'):
			my_list = item['value'].split(",")
			insert_dict["{0}".format(item['name'])] = my_list

		else:
			insert_dict["{0}".format(item['name'])] = item['value']
	
	return db.insert(insert_dict)
	
def mongoFindOne(collection, uri):
	db = client['FantasyDB']
	id = 0
	try:
		id = ObjectId(str(uri))
	except Exception as e:
		print(e)

	cursor = db[collection].find({'_id': id})
	return cursor

def mongoFindAll(obj_name):
	db = client['FantasyDB']
	cursor = db[obj_name].find()
	return cursor


##############################################################



def generateError(title, code, message):
	item = {}
	item["title"]= title
	item["code"]= code
	item["message"]= message

	return item

def packageResponse(data):
	resp = jsonify(data.getCollection())
	resp.status_code = 200
	resp.message ='OK'
	resp.content_type = content_type
	return resp

def returnTemplateFromData(obj_name):
	template = {}
	data = []
	db = client['FantasyDB']
	documents = db[obj_name].find()

	for element in documents:
		for key, value in element.items():
			if('id' in key):
				pass
			else:
				item = {}
				item['prompt'] = ""
				item['name'] = key

				if(type(value) is list):
					item['prompt'] = "list"
					item['value'] = '[]'
				elif(type(value) is tuple):
					item['prompt'] = "tuple"
					item['value'] = "()"
				elif(type(value) is dict):
					item['prompt'] = "dictionary"
					item['value'] = '{}'
				elif(type(value) is int):
					item['prompt'] = "int"
					item['value'] = 0
				elif(type(value) is float):
					item['prompt'] = "float"
					item['value'] = 0.0
				elif(type(value) is str):
					item['prompt'] = "text"
					item['value'] = ""
				elif(isinstance(value, datetime.datetime)):
					item['prompt'] = "datetime XXXX, XX, XX, XX, XX, XX"
					item['value'] = datetime.datetime(1700, 1, 1, 1, 1, 1)

				data.append(item)

		template['data'] = data
		return template
	return template

def generateNameValuePair(name, value):
	item = {}
	item['name'] = name
	item['value'] = value
	return item

def appendByType(item):
	if('varchar' in item['prompt']):
		return "'{0}'".format(item['value'])
	else:
		return "{0}".format(item['value'])

###########################################################################################
###########################################################################################
###########################################################################################
##### Python API Section 															#######
##### GET /table/list [Show's all tables in DB]										#######
##### GET /table/<table> 					[HTTP Parameter Value]					#######	
##### GET /table/showall/<table> 			[HTTP Parameter Value]					#######	
##### POST /table/<table>					[HTTP Parameter Value]					#######	
##### GET /table/showone/<table>/<uid> 		[HTTP Parameter  Table & Unique HREF]	#######
##### GET /db/list 																	#######	
###########################################################################################
###########################################################################################
###########################################################################################

"""API ROOT - Describes API links in return object """
@app.route('/test/<obj>', methods=['GET'])
def root(obj):
	url = request.url
	data = Structure(url)

	results = mongoDBQuery(obj)

	for item in results:
		
		entry = {}
		entry['href'] = ""
		entry['data'] = []
		for key, value in item.items():
			
			if(key == '_id'):
				mod_path = '/test/' + db + '/' + str(value)
				entry['href'] = getCurrentPath(url, mod_path)
				entry['data'].append(generateNameValuePair(key, str(value)))
			else:
				entry['data'].append(generateNameValuePair(key, str(value)))

		#entry['href'] = "/test/" + obj + "/" + item
		key = item 
		value = item
		data.appendItem(entry)	

	return packageResponse(data)

"""Worked from spec v1.0"""
@app.route('/db/list')
def showDatabases():
	url = request.url
	collection = Structure(url)
	query = "SHOW DATABASES"
	data = runSQLQuery(query, 0)
	for x in data:
		collection.appendItem(generateNameValuePair('database', x[0]))

	return packageResponse(collection)

"""Worked from spec v1.0"""
@app.route('/db/create/<db_name>')
def createDatabase(db_name):
	url = request.url
	query = "CREATE {0}".format(db_name)
	status = runSQLQuery(query, 1)
	collection = Structure(url)

@app.route('/table/list', methods=['GET'])
def getTableList():
	url = request.url
	collection = Structure(url)
	results = mongoGetCollections()

	for i in results:
		item = {}
		mod_path = '/table/post/' + i
		item['href'] = getCurrentPath(url, mod_path)
		item['data'] = generateNameValuePair('collection', i)
		collection.appendItem(item)

	return packageResponse(collection)

@app.route('/table/post/<input_collection>', methods=['GET', 'POST'])
def tableRoute(input_collection):
	"""table/structure & table/post merged into one method"""
	url = request.url
	collection = Structure(url)

	if(request.method == 'GET'):
		collection.setItems(describeObject(input_collection))
		link = getCurrentPath(url, '/table/post/' + input_collection)
		collection.appendLink(generateLink(link, 'post'))
		collection.setPostTemplate(returnTemplateFromData(input_collection))
		return packageResponse(collection)

	elif(request.method == 'POST'):
		try:
			collections = mongoGetCollections()
			if(input_collection not in collections):
				collection.setError(getError(-1, "Collection does not exist!"))
				return packageResponse(collection)

			data = None
			try:
				data = json.dumps(request.get_json())
				dict_data = json.loads(data)
				if(dict_data == None):
					raise Exception('Exception raised - JSON data package is None')

			except Exception as e:
				collection.setError(getError(1, e))
				collection.setPostTemplate(returnTemplateFromData(input_collection))
				return packageResponse(collection)

			#Insert to MongoDB - template data
			last_id = str(mongoInsertData(input_collection, dict_data))

			link = getCurrentPath(url, "/table/showall/" + input_collection)
			collection.appendLink(generateLink(link, 'showall'))
			link = getCurrentPath(url, "/table/showone/" + input_collection + "/" + last_id)
			collection.appendLink(generateLink(link, 'showone'))
			return packageResponse(collection)

		except Exception as e:
			collection.setError(getError(-1, e))
			#scollection.setPostTemplate(generateTemplate(input_collection))
			return packageResponse(collection)

@app.route('/table/showone/<input_collection>/<id>', methods=['GET'])
def showone(input_collection, id):
	url = request.url
	collection = Structure(url)
	
	# API for RDBMS code - Deprecated for ORM MongoDB

	#column_query = "SHOW COLUMNS FROM {0}".format(table)
	#columns = runSQLQuery(column_query, 0)
	#query = "SELECT * FROM {0} WHERE {1} = {2}".format(table, columns[0][0], id)
	#rows = runSQLQuery(query, 0)
	
	document = mongoFindOne(input_collection, id)

	item = {}
	mod_path = '/table/showone/' + input_collection + '/' + id
	item['href'] = getCurrentPath(url, mod_path)
	row_item_data = []
	counter=0

	if document is None:
		collection.setError(getError(3, ""))
	else:
		for element in document:
			for key, value in element.items():
				if('id' in key):
					row_item_data.append(generateNameValuePair(key, str(value)))
				else:
					row_item_data.append(generateNameValuePair(key, value))

		link = getCurrentPath(url, mod_path)
		collection.appendLink(generateLink(link, 'showone'))
		link = getCurrentPath(url, '/table/showall/' + input_collection)
		collection.appendLink(generateLink(link, 'showall'))
		link = getCurrentPath(url, '/table/post/' + input_collection)
		collection.appendLink(generateLink(link, 'post'))

		item['data'] = row_item_data
		collection.appendItem(item)

	collection.setPostTemplate(returnTemplateFromData(input_collection))
	
	return packageResponse(collection)

@app.route('/table/showall/<table>/<column>', methods=['GET'])
def showallByColumn(table, column):
	url = request.url
	collection = Structure(url)
	collection.setPostTemplate(generateTemplate(table))

	query = "SELECT {0} FROM {1}".format(column, table)
	query_result = runSQLQuery(query, 0)

	for item in query_result:
		collection.appendItem({'name': column, 'value': item[0]})

	return packageResponse(collection)

@app.route('/table/showall/<input_collection>', methods=['GET'])
def showall(input_collection):
	url = request.url
	collection = Structure(url)
	documents = mongoFindAll(input_collection)

	collection_exists = False
	data_exists = False

	for element in documents:
		collection_exists = True
		item = {}
		data = []
		for key, value in element.items():
			if('id' in key):
				mod_path = '/table/showone/' + input_collection + '/' + str(value)
				item['href'] = getCurrentPath(url, mod_path)
				data.append(generateNameValuePair('id', str(value)))
			
			elif(type(value) is list):
				list_values = ', '.join(map(str, value))
				data.append(generateNameValuePair(key, list_values))
			else:
				data.append(generateNameValuePair(key, value))

		item['data'] = data
		collection.appendItem(item)

	if(collection_exists == False):
		collection.setError(getError(-1, "Collection does not exist!"))
	else:
		collection.setPostTemplate(returnTemplateFromData(input_collection))
	        
	return packageResponse(collection)

@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
@app.route('/error')
def error(e):
	url = request.url
	collection = Structure(url)
	collection.appendLinks(describeAPI(url))

	if (e.code == 404):
		collection.setError(getHTTPError(404, request))
	elif(e.code == 405):
		collection.setError(getHTTPError(405, request))
	else:
		collection.setError(getHTTPError(5, e))
		return packageResponse(collection)

	collection.setError(getError(6, e))
	return packageResponse(collection)

if __name__ == '__main__':
    app.run(debug=True)
