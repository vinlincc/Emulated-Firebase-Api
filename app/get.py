import pymongo
from flask import Blueprint, request, jsonify
from .model import mongo
from .put import check_path
from flask_jwt_extended import jwt_required, get_jwt_identity

get_bp = Blueprint('get', __name__)


def transferDocument(documents, paths):
    documents_dict = {}
    if len(paths) < 1:
        for i in documents:
            documents_dict[list(i.keys())[0]] = list(i.values())[0]
    elif len(paths) == 1:
        document = next(documents)[paths[0]]
        documents_dict = document
    else:
        document = next(documents)
        for path in paths:
            document = document[path]
        documents_dict = document
    return documents_dict


def filterDocuments(documents, equalToFlag, startAtFlag, endAtFlag, args_dict):
    startIndex = 0
    if isinstance(documents, str) or len(documents) < 1:
        pass
    else:
        print(args_dict)
        if args_dict["orderBy"] == "\"$key\"":
            documents = sorted(documents.items())
            if equalToFlag:
                try:
                    tmp = [document for document in documents if
                           document[0] == args_dict["equalTo"][1:-1]]
                except:
                    tmp = [document for document in documents if document[0] == args_dict["equalTo"]]
                documents = tmp
            elif startAtFlag:
                try:
                    tmp = [document for document in documents if
                           document[0] >= args_dict["startAt"][1:-1]]
                except:
                    tmp = [document for document in documents if document[0] >= args_dict["startAt"]]
                documents = tmp
            elif endAtFlag:
                try:
                    tmp = [document for document in documents if
                           document[0] <= args_dict["endAt"][1:-1]]
                except:
                    tmp = [document for document in documents if document[0] <= args_dict["endAt"]]
                documents = tmp
            else:
                pass
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
                try:
                    tmp = [document for document in documents if
                           document[1] == args_dict["equalTo"][1:-1]]
                except:
                    tmp = [document for document in documents if
                           document[1] == int(args_dict["equalTo"])]
                documents = tmp
            elif startAtFlag:
                try:
                    tmp = [document for document in documents if
                           document[1] >= args_dict["startAt"][1:-1]]
                except:
                    tmp = [document for document in documents if
                           document[1] >= int(args_dict["startAt"])]
                documents = tmp
            elif endAtFlag:
                try:
                    tmp = [document for document in documents if
                           document[1] <= args_dict["endAt"][1:-1]]
                except:
                    tmp = [document for document in documents if
                           document[1] <= int(args_dict["endAt"])]
                documents = tmp
            else:
                pass
            non_sort.extend(documents)
            documents = non_sort
        else:
            can_sort = []
            non_sort = []
            for document in documents.items():
                if isinstance(document[1][args_dict["orderBy"][1:-1]], dict):
                    non_sort.append((document[0], document[1]))
                else:
                    can_sort.append((document[0], document[1]))
            can_sort = sorted(can_sort, key=lambda x: x[1][args_dict["orderBy"][1:-1]])
            documents = can_sort
            startIndex = len(non_sort)
            if equalToFlag:
                try:
                    tmp = [document for document in documents if
                           document[1][args_dict["orderBy"][1:-1]] == args_dict["equalTo"][1:-1]]
                except:
                    tmp = [document for document in documents if
                           document[1][args_dict["orderBy"][1:-1]] == int(args_dict["equalTo"])]
                documents = tmp
            elif startAtFlag:
                try:
                    tmp = [document for document in documents if
                           document[1][args_dict["orderBy"][1:-1]] >= args_dict["startAt"][1:-1]]
                except:
                    tmp = [document for document in documents if
                           document[1][args_dict["orderBy"][1:-1]] >= int(args_dict["startAt"])]
                documents = tmp
            elif endAtFlag:
                try:
                    tmp = [document for document in documents if
                           document[1][args_dict["orderBy"][1:-1]] <= args_dict["endAt"][1:-1]]
                except:
                    tmp = [document for document in documents if
                           document[1][args_dict["orderBy"][1:-1]] <= int(args_dict["endAt"])]
                documents = tmp
            else:
                pass
            non_sort.extend(documents)
            documents = non_sort
    return documents, startIndex


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
        filter = filterDocuments(documents, equalToFlag, startAtFlag, endAtFlag, args_dict)
        documents = filter[0]
        startIndex = filter[1]
        if limitToLastFlag:
            documents = documents[max(-int(args_dict["limitToLast"]), -(len(documents) - startIndex)):]
        elif limitToFirstFlag:
            documents = documents[startIndex:int(args_dict["limitToFirst"]) + startIndex]
        else:
            pass
        documents = dict(documents)
    else:
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
    # db = mongo.db
    path = myPath.split('/')
    path = check_path(path)
    if path is None: return jsonify({"message": "invalid collection"}), 400
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
    return documents
