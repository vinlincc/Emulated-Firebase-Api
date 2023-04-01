from flask_pymongo import PyMongo

mongo = PyMongo()

def init_admindb():
	admindb = mongo.cx['admin']
	try:
		admindb.create_collection("users")
	except Exception as e:
		print(e)