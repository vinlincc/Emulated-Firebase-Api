from flask import Blueprint, request, jsonify
from .model import mongo
import json
import uuid
from .put import process_put

post_bp = Blueprint('post', __name__)

@post_bp.route('/.json', defaults={'myPath': ''},methods=['POST'] )
@post_bp.route('/<path:myPath>.json', methods=['POST'])
def post(myPath):
    db = mongo.db
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
    

