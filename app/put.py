from flask import Blueprint, request, jsonify
from pymongo.errors import WriteError
from .model import mongo
import json

put_bp = Blueprint('put', __name__)

def input_data_check(input_data):
    #input_data should be checked, mongodb does not support key containing dot correctly
    if isinstance(input_data, dict):
        for k, v in input_data.items():
            if '.' in k: return False
            if not input_data_check(v): return False
    return True

def input_data_transform(input_data):
    if isinstance(input_data, list):
        return {str(i):input_data_transform(n) for i, n in enumerate(input_data)}
    if isinstance(input_data, dict):
        return {k:input_data_transform(v) for k, v in input_data.items()}
    return input_data

def check_path(path):
    remove_indices = []
    for i in range(len(path)):
        if '.' in path[i]: return
        if path[i] == '': remove_indices.append(i)
    return [field for i, field, in enumerate(path) if i not in remove_indices]

def update_doc(doc, keys, data):
    if not keys:
        return data

    key = keys.pop(0)
    if key not in doc:
        doc[key] = {}

    if not isinstance(doc[key], dict):
        doc[key] = {}
        
    doc[key] = update_doc(doc[key], keys, data)
    return doc

def process_put(db, myPath, input_data):
    if not input_data_check(input_data):
        return jsonify({"message": "dots in key are not allowed"}), 400
    input_data = input_data_transform(input_data)
    path = myPath.split('/')
    path = check_path(path)
    if path is None: return jsonify({"message": "invalid collection"}), 400
    if path[0] not in db.list_collection_names(): return jsonify({"message": "invalid collection"}), 400
    collection = db[path[0]]
    # --------------------------------------------------------------------------------
    if len(path) == 1:
        if not isinstance(input_data, dict): return "element under root must be a dict"
        collection.drop()
        documents = [{k:v} for k, v in input_data.items()]
        collection.insert_many(documents)
        return jsonify({"message": "Resource created successfully", "data": input_data}), 201
    # --------------------------------------------------------------------------------
    key = path[1]
    p = '.'.join(path[1:])  #"yxj.aaa.bbb.ccc"

    try:
        result = collection.update_one({p:{"$exists": True}}, {"$set":{p:input_data}})
    except WriteError as e:
        print(f"An error occurred: {e}")
    else:
        if result.modified_count == 1:
            return jsonify({"message": "Resource created successfully", "data": input_data}), 201
    # --------------------------------------------------------------------------------
    if collection.count_documents({key:{"$exists": True}}) == 0:
        collection.insert_one({key:1})
    doc = next(collection.find({key:{"$exists": True}}))
    ud = update_doc(doc, path[1:], input_data)
    collection.replace_one({"_id":ud["_id"]}, ud)
    return jsonify({"message": "Resource created successfully", "data": input_data}), 201

@put_bp.route('/.json', defaults={'myPath': ''},methods=['PUT'] )
@put_bp.route('/<path:myPath>.json', methods=['PUT'])
def put(myPath):
    db = mongo.db
    input_data = request.get_json(force=True)
    return process_put(db, myPath, input_data)
