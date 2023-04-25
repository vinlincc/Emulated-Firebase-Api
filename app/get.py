import pymongo
from flask import Blueprint, request, jsonify
from .model import mongo
from .put import check_path
from flask_jwt_extended import jwt_required, get_jwt_identity
import copy

get_bp = Blueprint('get', __name__)


def transferDocument(documents, paths):
    documents_dict = {}
    documents_copy = copy.deepcopy(documents)
    if (len(list(documents_copy))) == 0:
        return documents_dict
    if len(paths) < 1:
        for i in documents:
            documents_dict[list(i.keys())[0]] = list(i.values())[0]
    elif len(paths) == 1:
        document = next(documents)[paths[0]]
        if document == {}:
            return jsonify({"message": "none data"}), 400
        documents_dict = document
    else:
        document = next(documents)
        for path in paths:
            try:
                document = document[path]
            except:
                return jsonify({"message": "none data"}), 400
        documents_dict = document
    return documents_dict


def isCanSort(document,order_list):
    document = document[1]
    for i in order_list:
        try:
            document = document[i]
        except:
            return False
    return False if isinstance(document, dict) else True

def sortFunc(document,order_list):
    document = document[1]
    for i in order_list:
        document = document[i]
    return document
def filterDocuments(documents, equalToFlag, startAtFlag, endAtFlag, args_dict):
    startIndex = 0
    if isinstance(documents, str) or len(documents) < 1:
        pass
    else:
        if args_dict["orderBy"] == "\"$key\"":
            documents = sorted(documents.items())
            if equalToFlag:
                if args_dict["equalTo"].isdigit():
                    tmp = [document for document in documents if document[0] == int(args_dict["equalTo"])]
                else:
                    tmp = [document for document in documents if
                           document[0] == args_dict["equalTo"][1:-1]]
                documents = tmp
            elif startAtFlag:
                if args_dict["startAt"].isdigit():
                    tmp = [document for document in documents if document[0] >= int(args_dict["startAt"])]
                else:
                    tmp = [document for document in documents if
                           document[0] >= args_dict["startAt"][1:-1]]
                if endAtFlag:
                    if args_dict["endAt"].isdigit():
                        tmp = [document for document in tmp if document[0] <= int(args_dict["endAt"])]
                    else:
                        tmp = [document for document in tmp if
                               document[0] <= args_dict["endAt"][1:-1]]
                documents = tmp
            elif endAtFlag:
                if args_dict["endAt"].isdigit():
                    tmp = [document for document in documents if document[0] <= int(args_dict["endAt"])]
                else:
                    tmp = [document for document in documents if
                           document[0] <= args_dict["endAt"][1:-1]]
                documents = tmp
            else:
                pass
            print(documents)
        elif args_dict["orderBy"] == "\"$value\"":
            can_sort = []
            non_sort = []
            for document in documents.items():
                if isinstance(document[1], dict):
                    non_sort.append((document[0], document[1]))
                else:
                    can_sort.append((document[0], document[1]))
            can_sort = sorted(can_sort, key=lambda x: x[1])
            documents = can_sort
            startIndex = len(non_sort)
            if equalToFlag:
                if args_dict["equalTo"].isdigit():
                    tmp = [document for document in documents if
                           document[1] == int(args_dict["equalTo"])]
                else:
                    tmp = [document for document in documents if
                           document[1] == args_dict["equalTo"][1:-1]]
                documents = tmp
            elif startAtFlag:
                if args_dict["startAt"].isdigit():
                    tmp = [document for document in documents if
                           document[1] >= int(args_dict["startAt"])]
                else:
                    tmp = [document for document in documents if
                           document[1] >= args_dict["startAt"][1:-1]]
                if endAtFlag:
                    if args_dict["endAt"].isdigit():
                        tmp = [document for document in tmp if
                               document[1] <= int(args_dict["endAt"])]
                    else:
                        tmp = [document for document in tmp if
                               document[1] <= args_dict["endAt"][1:-1]]
                documents = tmp
            elif endAtFlag:
                if args_dict["endAt"].isdigit():
                    tmp = [document for document in documents if
                           document[1] <= int(args_dict["endAt"])]
                else:
                    tmp = [document for document in documents if
                           document[1] <= args_dict["endAt"][1:-1]]
                documents = tmp
            else:
                pass
            non_sort.extend(documents)
            documents = non_sort
        else:
            can_sort = []
            non_sort = []
            order_list = args_dict["orderBy"][1:-1].split("/")
            for document in documents.items():
                if isCanSort(document,order_list):
                    can_sort.append((document[0], document[1]))
                else:
                    non_sort.append((document[0], document[1]))
            can_sort = sorted(can_sort, key=lambda x: sortFunc(x,order_list))
            documents = can_sort
            startIndex = len(non_sort)
            if equalToFlag:
                if args_dict["equalTo"].isdigit():
                    tmp = [document for document in documents if
                           sortFunc(document,order_list) == int(args_dict["equalTo"])]
                else:
                    tmp = [document for document in documents if
                           sortFunc(document, order_list) == args_dict["equalTo"][1:-1]]
                documents = tmp
            elif startAtFlag:
                if args_dict["startAt"].isdigit():
                    tmp = [document for document in documents if
                           sortFunc(document,order_list) >= int(args_dict["startAt"])]
                else:
                    tmp = [document for document in documents if
                           sortFunc(document,order_list) >= args_dict["startAt"][1:-1]]
                if endAtFlag:
                    if args_dict["endAt"].isdigit():
                        tmp = [document for document in tmp if
                               sortFunc(document,order_list) <= int(args_dict["endAt"])]
                    else:
                        tmp = [document for document in tmp if
                               sortFunc(document,order_list) <= args_dict["endAt"][1:-1]]
                documents = tmp
            elif endAtFlag:
                if args_dict["endAt"].isdigit():
                    tmp = [document for document in documents if
                           sortFunc(document,order_list) <= int(args_dict["endAt"])]
                else:
                    tmp = [document for document in documents if
                           sortFunc(document,order_list) <= args_dict["endAt"][1:-1]]
                documents = tmp
            else:
                pass
            non_sort.extend(documents)
            documents = non_sort
    return documents, startIndex


def isHasIndex(args_dict, db, path):
    orderByField = args_dict["orderBy"]
    if orderByField.isdigit():
        pass
    else:
        orderByField = orderByField[1:-1]
    if orderByField == "$value":
        orderByField = "/".join(path[2:]) + "/$value"
    indexs = db["index"].find({path[0]: {"$exists": True}})
    indexs = next(indexs)[path[0]]
    print(indexs)
    print(orderByField)
    if orderByField == "$key":
        return True
    else:
        if orderByField in indexs:
            return True
        else:
            return False


def findDocuments(db, path, orderByFlag, limitToFirstFlag, limitToLastFlag, equalToFlag, startAtFlag,
                  endAtFlag, args_dict):
    length = len(path)
    if length == 1:
        documents = db[path[0]].find({}, {'_id': 0})
    elif length == 2:
        documents = db[path[0]].find({path[1]: {"$exists": True}}, {'_id': 0})
    else:
        documents = db[path[0]].find({path[1]: {"$exists": True}}, {'_id': 0})
    documents = transferDocument(documents, path[1:])
    if orderByFlag:
        if isHasIndex(args_dict, db, path):
            filter = filterDocuments(documents, equalToFlag, startAtFlag, endAtFlag, args_dict)
            documents = filter[0]
            startIndex = filter[1]
            if limitToLastFlag:
                if args_dict["limitToLast"].count(".") == 1 or int(args_dict["limitToLast"]) < 0:
                    return jsonify({"message": "number should be positive integer"}), 400
                documents = documents[max(-int(args_dict["limitToLast"]), -(len(documents) - startIndex)):]
            elif limitToFirstFlag:
                if args_dict["limitToFirst"].count(".") == 1 or int(args_dict["limitToFirst"]) < 0:
                    return jsonify({"message": "number should be positive integer"}), 400
                documents = documents[startIndex:int(args_dict["limitToFirst"]) + startIndex]
            else:
                pass
        else:
            return jsonify({"message": "This field has no index, please create index first"}), 400
        documents = dict(documents)
    else:
        if limitToLastFlag or limitToFirstFlag or equalToFlag or startAtFlag or endAtFlag:
            return jsonify({"message": "filter should not been done without orderBy operation"}), 400
        pass
    if isinstance(documents, str):
        pass
    elif isinstance(documents, int):
        documents = str(documents)
    return documents


@get_bp.route('/.json', defaults={'myPath': ''}, methods=['GET'])
@get_bp.route('/<path:myPath>.json', methods=['GET'])
@jwt_required()
def get(myPath):
    user = get_jwt_identity()
    user_database = f"db_{user}"
    db = mongo.cx[user_database]
    path = myPath.split('/')
    path = check_path(path)
    if path == []: return jsonify({"message": "invalid collection"}), 400
    if path[0] not in db.list_collection_names(): return jsonify({"message": "invalid collection"}), 400
    args_dict = request.args
    args_keys = args_dict.keys()
    orderByFlag = True if args_keys.__contains__("orderBy") else False
    limitToFirstFlag = True if args_keys.__contains__("limitToFirst") else False
    limitToLastFlag = True if args_keys.__contains__("limitToLast") else False
    equalToFlag = True if args_keys.__contains__("equalTo") else False
    startAtFlag = True if args_keys.__contains__("startAt") else False
    endAtFlag = True if args_keys.__contains__("endAt") else False
    documents = findDocuments(db, path, orderByFlag, limitToFirstFlag, limitToLastFlag, equalToFlag, startAtFlag,
                              endAtFlag, args_dict)
    print(documents)
    return documents
