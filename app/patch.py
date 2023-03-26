from flask import Blueprint, request, jsonify
from .model import mongo
from pymongo.errors import WriteError
import json
from .put import input_data_check, input_data_transform, check_path, update_doc

patch_bp = Blueprint('patch', __name__)

def process_patch(db, myPath, input_data):
    if not input_data_check(input_data):
        return jsonify({"message": "dots in key are not allowed"}), 400
    if not isinstance(input_data, dict):
        return jsonify({"message": "only dict allowed in PATCH"}), 400
    input_data = input_data_transform(input_data)
    path = myPath.split('/')
    path = check_path(path)
    if path is None: return jsonify({"message": "invalid collection"}), 400
    if path[0] not in db.list_collection_names(): return jsonify({"message": "invalid collection"}), 400
    collection = db[path[0]]
    # --------------------------------------------------------------------------------
    if len(path) == 1:
        for k, v in input_data.items():
            result = collection.update_one({k: {"$exists": True}}, {"$set": {k: v}})
            if result.matched_count == 0:
                collection.insert_one({k:v})
        return jsonify({"message": "Resource updated successfully", "data": input_data}), 200
    # --------------------------------------------------------------------------------
    key = path[1]
    p = '.'.join(path[1:])
    update_fields = {f"{p}.{k}": v for k, v in input_data.items()}
    try:
        result = collection.update_one({p: {"$exists": True}}, {"$set": update_fields})
    except WriteError as e:
        print(f"An error occurred: {e}")
    else:
        if result.modified_count != 0:
            return jsonify({"message": "Resource updated successfully", "data": input_data}), 200
    # --------------------------------------------------------------------------------
    result = collection.find_one({key: {"$exists": True}})
    if result is None:
        collection.insert_one({key: {}})
        result = collection.find_one({key: {"$exists": True}})

    ud = update_doc(result, path[1:], input_data)
    collection.replace_one({"_id": ud["_id"]}, ud)
    return jsonify({"message": "Resource created successfully", "data": input_data}), 201

@patch_bp.route('/.json', defaults={'myPath': ''},methods=['PATCH'] )
@patch_bp.route('/<path:myPath>.json', methods=['PATCH'])
def patch(myPath):
    db = mongo.db
    input_data = request.get_json(force=True)
    return process_patch(db, myPath, input_data)
