# - Author: Keith Michael Byrne
# - Date Completed: 19/02/2015
# - Aegis of: Institute of Technology Carlow

# - Synopsis: 	RESTful API for database schema gamesdb
# -				and can be easily configured for use on any
# -				database schema by reassigning db on global
# -				definitions under CONFIG SETTINGS

# - Date of Submission: 19/02/2015 00:00
# - Python Data: Version 3.4
# - Dependencies: Flask, mysql-connector-python
# - 	See also lib modules for errors and collection+JSON object

# - Supervisor: Paul Barry
# - Successful implementation on: Windows 7/8, Raspberry Pi (Debian) & Linux Mint



from flask import Flask,render_template,jsonify,url_for,request,session,flash, json, Response
from urllib.parse import urlparse
import lib, json
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from functools import wraps
import mysql.connector
from bson.objectid import ObjectId

from pymongo import MongoClient

from lib.collection import Structure
from lib.errors import *

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
mongo_db = client['gamesdb']

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


def mongoDBQuery(obj_name):
		db = client['games']
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
		db = client['gamesdb']
		cursor = db.collection_names()
		return cursor
	except Exception as e:
		return None

def mongoFindOne(table, uri):
	db = client['gamesdb']
	cursor = db[table].find({'_id': ObjectId(uri)})
	return cursor


def runSQLQuery(_sql, code):
	"""Allow for variation in how SQL connection models INSERT's and SELECT's"""
	"""Division of functionality simply using 0,1,2 code to decide route"""
	"""No need for commit on SELECT or UPDATE (code 2 -> later revision)"""
	"""For returning data relating to the structure of a table to order specific"""
	"""Insert queries on POST"""
	con = mysql.connector.connect(host=host, user=user, password=password, database=db)
	cursor = con.cursor()

	if code == 0:
    	# All select queries here
		try:
			cursor.execute(_sql)
			data = cursor.fetchall()
			return data
		except Exception as e:
			return e

	elif code == 1: 
    	#All insert queries here
		try:
			cursor.execute(_sql)
			con.commit()
			last_id = cursor.lastrowid
			return {'code': True, 'msg': last_id} 
		except Exception as e:
			return {'code': False, 'msg': e}
	elif code == 2:
		#All special describe queries here
		try:
			data = {}
			cursor.execute(_sql)
			data['rows'] = cursor.fetchall()
			data['columns'] = cursor.description
			return data
		except Exception as e:
			return False


	cursor.close()
	con.close()

def generateError(title, code, message):
	item = {}
	item["title"]= title
	item["code"]= code
	item["message"]= message

	return item

def generateDynamicItem(columns, data):
	items = []
	counter = 0
	outer = 0

	for i in data:
		for x in i:
			dict = {'value': x[0]}
			items.append(dict)

	return jsonify(items)

def packageResponse(data):
	resp = jsonify(data.getCollection())
	resp.status_code = 200
	resp.message ='OK'
	resp.content_type = content_type
	return resp

def returnTemplateFromData(table):

	description = mongo_db[table].find()
	template = {}
	for element in description:
		data = []
		for key, value in element.items():
			if(key == '_id'):
				pass
			else:
				item = {}
				item['prompt'] = ""
				item['name'] = key
				item['value'] = ""
				data.append(item)

		template['data'] = data

	print(template)
	return template

def generateTemplate(table_name):
	#Essentially describing table
	#Returning column types and 
	#Column names for INSERT reference
	template = {}
	data = []
	tables = [table_name]
	description = describeOne(table_name)

	for i in description:
		if(i[0] == 'id' or 'on update' in i[5] or 'auto_increment' in i[5]):
			pass
		else:
			item = {}
			item['prompt'] = "type " + i[1]
			item['name'] = i[0]
			item['value'] = ""
			data.append(item)

	template['data'] = data

	return template

def getTables():
	query = "SHOW TABLES"
	tables = runSQLQuery(query, 0)
	return tables

def describeOne(table):
	query = "DESCRIBE {0}".format(table)
	return runSQLQuery(query, 0)
	
def describeTables(url, list_of_tables):
	"""Returns a global set of info relating"""
	"""to tables given [parameter list]"""
	items = []
	data = []

	for x in list_of_tables:
		query = "DESCRIBE {0}".format(x)
		query_results = runSQLQuery(query, 2)
		headers = query_results['columns']

		item = {}
		item['href'] = url
		item['data'] = []
		
		for i in query_results['rows']:	
			counter = 0
			sub_item = {}
			sub_item['href'] = getCurrentPath(url, "/table/post/players/" + i[0])
			sub_item['data'] = []
			inner_data = []
			for col in i:
				sub_item['data'].append(generateNameValuePair(headers[counter][0], col))
				counter = counter + 1

			items.append(sub_item)
		#items.append(item)
	return items

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

	print(results)

	for i in results:
		item = {}
		mod_path = '/table/post/' + i
		item['href'] = getCurrentPath(url, mod_path)
		item['data'] = generateNameValuePair('collection', i)
		collection.appendItem(item)

	return packageResponse(collection)

@app.route('/table/post/<table>', methods=['GET', 'POST'])
def tableRoute(table):
	"""table/structure & table/post merged into one method"""
	url = request.url
	collection = Structure(url)

	if(request.method == 'GET'):
		dbs = [table]	
		collection.setItems(describeTables(url, dbs))
		link = getCurrentPath(url, '/table/post/' + table)

		collection.appendLink(generateLink(link, 'post'))
		collection.setPostTemplate(generateTemplate(table))

		return packageResponse(collection)

	elif(request.method == 'POST'):
		try:
			dict_data = None
			try:
				data = json.dumps(request.get_json())
				dict_data = json.loads(data)
				if(dict_data == None):
					raise Exception('Exception raised - JSON data package is None')

			except Exception as e:
				collection.setError(getError(1, e))
				collection.setPostTemplate(generateTemplate(table))
				return packageResponse(collection)

			columns = ""
			counter = 0
			for col in dict_data['template']['data']:
				if(counter == 0):
					columns += (col['name'])
				else:
					columns += (", " + col['name'] + "")
				counter = counter + 1

			query = ['INSERT ', 'INTO ', table, '(', columns, ')', ' values ', '(']

			inputs = 0
			for item in dict_data['template']['data']:
				if(item['name'] != 'id'):
					if(inputs == 0):
						query.append(appendByType(item))

					else:
						query.append(", " + appendByType(item))

					inputs = inputs + 1

			query.append(')')
			query = ''.join(query)
			status = ""
			try:
				status = runSQLQuery(query, 1)
			except Exception as e:
				collection.setError(getError(2, status['msg']))
				return packageResponse(collection)

			if(status['code'] != False):
				link = getCurrentPath(url, "/table/showall/" + table)
				collection.appendLink(generateLink(link, 'showall'))
				link = getCurrentPath(url, "/table/showone/" + table + "/" + str(status['msg']))
				collection.appendLink(generateLink(link, 'showone'))
				return packageResponse(collection)

			else:
				collection.setError(getError(2, str(status['msg'])))
				return packageResponse(collection)

		except Exception as e:
			collection.setError(getError(-1, e))
			collection.setPostTemplate(generateTemplate(table))
			return packageResponse(collection)

@app.route('/table/showone/<table>/<id>', methods=['GET'])
def showone(table, id):
	url = request.url
	collection = Structure(url)
	
	# API for RDBMS code - Deprecated for ORM MongoDB

	#column_query = "SHOW COLUMNS FROM {0}".format(table)
	#columns = runSQLQuery(column_query, 0)
	#query = "SELECT * FROM {0} WHERE {1} = {2}".format(table, columns[0][0], id)
	#rows = runSQLQuery(query, 0)


	print(id)

	rows = mongoFindOne(table, id)

	print(rows)

	item = {}
	data = []
	mod_path = '/table/showone/' + id
	item['href'] = getCurrentPath(url, mod_path)
	#row_item={}
	row_item_data = []
	counter=0

	if rows is None:
		collection.setError(getError(3, ""))
	else:
		for element in rows:
			for key, value in element.items():
				data_item = generateNameValuePair(key, str(value))
				row_item_data.append(data_item)

		link = getCurrentPath(url, mod_path)
		collection.appendLink(generateLink(link, 'showone'))
		link = getCurrentPath(url, '/table/showall/' + table)
		collection.appendLink(generateLink(link, 'showall'))
		link = getCurrentPath(url, '/table/post/' + table)
		collection.appendLink(generateLink(link, 'post'))

		item['data'] = row_item_data
		collection.appendItem(item)

	#collection.setPostTemplate(returnTemplateFromData(rows))
	
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

@app.route('/table/showall/<table>', methods=['GET'])
def showall(table):
	url = request.url
	collection = Structure(url)
	results = mongo_db[table].find()
	collections = mongoGetCollections()

	collection_exists = False
	data_exists = False

	for element in collections:
		if(element == table):
			collection_exists = True
			for element in results:
				data_exists =  True
				item = {}
				data = []

				unique_ref = str(element['_id'])
				mod_path = '/table/showone/' + table + "/" + unique_ref
				item['href'] = getCurrentPath(url, mod_path)

				try:
					for key, value in element.items():
						data.append(generateNameValuePair(key, str(value)))
				except Exception as e:
					pass

				item['data'] = data
				collection.appendItem(item)

	if(collection_exists == False):
		collection.setError(getError(-1, "Collection does not exist!"))
	else:
		if(data_exists == False):
			collection.setError(getError(-1, "No documents exist within collection!"))
		else:
			collection.setPostTemplate(returnTemplateFromData(table))
		
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
