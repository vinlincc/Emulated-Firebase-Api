import bson.json_util
from flask import Blueprint, jsonify
from .model import mongo
from pymongo.errors import WriteError
from flask_jwt_extended import jwt_required, get_jwt_identity

delete_bp = Blueprint('delete', __name__)


def path_Converter(path):
    if "." in path:
        raise ValueError('The path cannot contain "."')
    return path.replace(" ","")


def remover(d, value):
    for k,v in list(d.items()):
        if v == value or k == value:
            del d[k]
        elif isinstance(v, dict):
            remover(v,value)

def remover2(d, value, motherEntry):
    for k,v in list(d.items()):
        if k == motherEntry:
            del v[value]
        elif isinstance(v, dict):
            remover2(v,value,motherEntry)






def delete_process(db, myPath):
    myPath = path_Converter(myPath)
    path = myPath.split('/')

    #NOTE: When we use delete, the program ignores input_data, and there will be no bug if you type in something

    #case1: path is None,we will delete all the tables
    #e.g. curl -X DELETE "http://127.0.0.1:5000/"
    if path == [""]:
        for collection in db.list_collection_names():
            db[collection].drop()
        return jsonify({"message": "All the tables are deleted successfully"}), 200


    #case 2: path is single element but table is not found
    # e.g. curl -X DELETE "http://127.0.0.1:5000/dwadawdhjawiudhawiu"
    if path[0] not in db.list_collection_names():
        return jsonify({"message": "This table name is not found", "path":path}), 400

    #case 3: Table is found, and delete the whole table
    # e.g. curl -X DELETE "http://127.0.0.1:5000/Mydata"
    collection = db[path[0]]
    if len(path) == 1:
        collection.drop()
        return jsonify({"message": f"The table --{str(path[0])}-- is deleted successfully", "path": path}), 201

    #case 4: Table is found, and we want to delete element
    else:
        p = '.'.join(path[1:])
        result = collection.find_one({p: {"$exists": True}})

        #if the path is wrong
        if result is None:
            return jsonify({"message": f"The element is not found, wrong path"}), 400
        else:
            # delete the primary element anyway
            id = list(collection.find({p: {"$exists": True}}))[0]
            collection.delete_one(id)
            #convert result to dict
            result_dict = dict(result)

        #case 4a: This is the special case which we delete the primary elements from the table
        # e.g. curl -X DELETE "http://127.0.0.1:5000/Mydata/school"
        if len(path) == 2:
            return jsonify({"message": f"The element --{str(path[1])}-- is deleted successfully"}), 202

        #case 4b: We delete child elements whrere the number in path is >=3
        # e.g. curl -X DELETE "http://127.0.0.1:5000/Mydata/school/USC/color"
        # my method here is to drop the primary element and add a shrunk one back
        else:
            #filter
            if path[-1].isdigit():
                remover2(result_dict, path[-1], path[-2])
            else:
                remover(result_dict, path[-1])

            insert_content = [result_dict]
            collection.insert_many(insert_content)
            return jsonify({"message":f"The element {path[-1]} is deleted successfully"}), 203




@delete_bp.route('/.json', defaults={'myPath': ''},methods=['DELETE'] )
@delete_bp.route('/<path:myPath>.json', methods=['DELETE'])
@jwt_required()
def delete(myPath):
    user = get_jwt_identity()
    user_database = f"db_{user}"
    db = mongo.cx[user_database]
    #db = mongo.db
    return delete_process(db, myPath)
