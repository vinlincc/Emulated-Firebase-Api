from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit
from .model import mongo
from flask import current_app
import json
import uuid
import threading
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
    by_value = request.args.get('byValue', default=None, type=int)

    path = myPath.split('/')
    path = check_path(path)

    if collection_name not in db.list_collection_names(): return jsonify({"message": "invalid collection"}), 400
    collection = db[collection_name]
    index = None
    try:
        if path != []: 
            index = collection.create_index('.'.join(path))
    except Exception as e:
        # return jsonify({"message": f"{e}"}), 400
        pass

    if by_value: path.append("$value")
    db['index'].update_one(
        {collection_name:{"$exists":True}},
        {"$push":{f"{collection_name}":"/".join(path)}}
    ) # add the path into and array 
    return jsonify({"message": f"Index '{'/'.join(path)}' created successfully"}), 201
    # if index is not None or path == []:
    #     if path == []: path.append("$value")
    #     db['index'].update_one(
    #         {collection_name:{"$exists":True}},
    #         {"$push":{f"{collection_name}":"/".join(path)}}
    #     ) # add the path into and array 
    #     return jsonify({"message": f"Index '{'/'.join(path)}' created successfully"}), 201
    # else:
    #     return jsonify({"message": f"Failed to create the index"}), 400


@post_bp.route('/.create_listener/<collection_name>', methods=['POST'])
@jwt_required()
def create_listener(collection_name):
    user = get_jwt_identity()
    user_database = f"db_{user}"
    db = mongo.cx[user_database]
    if collection_name not in db.list_collection_names(): return jsonify({"message": "invalid collection"}), 400
    collection = db[collection_name]
    socketio = current_app.config["socketio"]
    def change_stream_listener():
        print("Starting change stream listener")
        with collection.watch() as stream:
            print("Starting change stream listener")
            while stream.alive:
                change = stream.try_next()
                if change:
                    simplified_change = {
                        'operationType': change['operationType'],
                        # 'fullDocument': {k: v for k, v in change['fullDocument'].items() if k != '_id'},
                        'ns': change['ns'],
                        'wallTime': change['wallTime'].strftime('%Y-%m-%d %H:%M:%S.%f')
                    }
                    if 'fullDocument' in change:
                        simplified_change['fullDocument'] = {k: v for k, v in change['fullDocument'].items() if k != '_id'}
                    if 'updateDescription' in change:
                        simplified_change['updateDescription'] = change['updateDescription']

                    print(f"Change detected: {change}")
                    # Emit the change to all connected clients
                    # socketio.emit('change_detected', change)
                    socketio.emit('change_detected', simplified_change)
    # threading.Thread(target=change_stream_listener).start()
    socketio.start_background_task(change_stream_listener)
    return jsonify({"message": "Change stream listener started"}), 200
























