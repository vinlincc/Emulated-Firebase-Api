from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import mongo
import json
import uuid
from .put import process_put

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
        return jsonify({"message": f"Collection '{collection_name}' created successfully"}), 201
    else:
        return jsonify({"message": f"Failed to create collection '{collection_name}'"}), 400




























