from flask import Flask
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test_mongodb')
def test_mongodb():
    # Insert a document into the 'test' collection
    mongo.db.test.insert_one({"message": "Hello, MongoDB!"})

    # Retrieve the document from the 'test' collection
    # document = mongo.db.test.find_one({"message": "Hello, MongoDB!"})
    document = mongo.db.get_test.find_one({"yxj": {"$exists": True}},{'_id':0})

    # Return the document content as a string
    return str(document)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)

