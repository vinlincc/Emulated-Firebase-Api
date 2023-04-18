from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import mongo
import json
import uuid
from .put import process_put, check_path

post_bp = Blueprint('post', __name__)

@post_bp.route('/.json', defaults={'myPath': ''},methods=['POST'] )
@post_bp.route('/<path:myPath>.json', methods=['POST'])
@jwt_required()
def post(myPath):
    user = get_jwt_identity()
    user_database = f"db_{user}"
    db = mongo.cx[user_database]
    input_data = request.get_json(force=True)
    post_id = str(uuid.uuid4())
    new_path = f"{myPath}/{post_id}"
    response, status_code = process_put(db, new_path, input_data)
    if status_code == 400:
        return (response, status_code)
    else:
        response_data = response.get_json()
        response_data["name"] = post_id
        return jsonify(response_data), status_code
    
@post_bp.route('/.create_collection/<collection_name>', methods=['POST'])
@jwt_required()
def create_collection(collection_name):
    user = get_jwt_identity()
    user_database = f"db_{user}"
    db = mongo.cx[user_database]
    collection = None
    try:
        collection = db.create_collection(collection_name)
    except Exception as e:
        return jsonify({"message": f"{e}"}), 400
    if collection is not None:
        db['index'].insert_one({collection_name:[]})
        return jsonify({"message": f"Collection '{collection_name}' created successfully"}), 201
    else:
        return jsonify({"message": f"Failed to create collection '{collection_name}'"}), 400

@post_bp.route('/.create_index/<collection_name>/', defaults={'myPath': ''}, methods=['POST'])
@post_bp.route('/.create_index/<collection_name>/<path:myPath>', methods=['POST'])
@jwt_required()
def create_index(collection_name, myPath):
    user = get_jwt_identity()
    user_database = f"db_{user}"
    db = mongo.cx[user_database]

    path = myPath.split('/')
    path = check_path(path)
    if collection_name not in db.list_collection_names(): return jsonify({"message": "invalid collection"}), 400
    collection = db[collection_name]
    index = None
    try:
        if path != []: 
            index = collection.create_index('.'.join(path))
    except Exception as e:
        return jsonify({"message": f"{e}"}), 400

    if index is not None or path == []:
        if path == []: path.append("$value")
        db['index'].update_one(
            {collection_name:{"$exists":True}},
            {"$push":{f"{collection_name}":"/".join(path)}}
        ) # add the path into and array 
        return jsonify({"message": f"Index '{'/'.join(path)}' created successfully"}), 201
    else:
        return jsonify({"message": f"Failed to create the index"}), 400



























