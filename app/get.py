import pymongo
from flask import Blueprint, request, jsonify
from .model import mongo
from .put import check_path

get_bp = Blueprint('get', __name__)


def transferDocument(documents, paths):
    documents_list = []
    if len(paths) < 1:
        for i in documents:
            documents_list.append(i)
    elif len(paths) == 1:
        document = next(documents)[paths[0]]
        documents_list.append(document)
    else:
        document = next(documents)
        for path in paths:
            document = document[path]
        documents_list.append(document)
    return documents_list


def filterDocuments(documents, equalToFlag, startAtFlag, endAtFlag, args_dict):
    if len(documents) == 0:
        pass
    elif len(documents) == 1:
        pass
    else:
        if args_dict["orderBy"] == "\"$key\"":
            if len(documents[0]) >= 2 or len(documents[0]) == 0:
                pass
            else:
                documents = sorted(documents, key=lambda x: list(x.keys())[0])
                if equalToFlag:
                    try:
                        tmp = [document for document in documents if
                               list(document.keys())[0] == args_dict["equalTo"][1:-1]]
                    except:
                        tmp = [document for document in documents if list(document.keys())[0] == args_dict["equalTo"]]
                    documents = tmp
                elif startAtFlag:
                    try:
                        tmp = [document for document in documents if
                               list(document.keys())[0] >= args_dict["startAt"][1:-1]]
                    except:
                        tmp = [document for document in documents if list(document.keys())[0] >= args_dict["startAt"]]
                    documents = tmp
                elif endAtFlag:
                    try:
                        tmp = [document for document in documents if
                               list(document.keys())[0] == args_dict["endAt"][1:-1]]
                    except:
                        tmp = [document for document in documents if list(document.keys())[0] == args_dict["endAt"]]
                    documents = tmp
                else:
                    pass
        elif args_dict["orderBy"] == "\"$value\"":
            if len(documents[0]) >= 2 or len(documents[0]) == 0:
                pass
            else:
                if (isinstance(list(documents[0].values())[0], dict)):
                    pass
                else:
                    documents = sorted(documents, key=lambda x: list(x.values())[0])
                    if equalToFlag:
                        try:
                            tmp = [document for document in documents if
                                   list(document.values())[0] == args_dict["equalTo"][1:-1]]
                        except:
                            tmp = [document for document in documents if
                                   list(document.values())[0] == args_dict["equalTo"]]
                        documents = tmp
                    elif startAtFlag:
                        try:
                            tmp = [document for document in documents if
                                   list(document.values())[0] >= args_dict["startAt"][1:-1]]
                        except:
                            tmp = [document for document in documents if
                                   list(document.values())[0] >= args_dict["startAt"]]
                        documents = tmp
                    elif endAtFlag:
                        try:
                            tmp = [document for document in documents if
                                   list(document.values())[0] == args_dict["endAt"][1:-1]]
                        except:
                            tmp = [document for document in documents if
                                   list(document.values())[0] == args_dict["endAt"]]
                        documents = tmp
                    else:
                        pass
        else:
            if (isinstance(list(documents[0].values())[0][args_dict["orderBy"][1:-1]], dict)):
                pass
            else:
                try:
                    documents = sorted(documents, key=lambda x: list(x.values())[0][args_dict["orderBy"][1:-1]])
                except:
                    documents = []
                if equalToFlag:
                    try:
                        tmp = [document for document in documents if
                               list(document.values())[0][args_dict["orderBy"][1:-1]] == args_dict["equalTo"][1:-1]]
                    except:
                        tmp = [document for document in documents if
                               list(document.values())[0][args_dict["orderBy"][1:-1]] == args_dict["equalTo"]]
                    documents = tmp
                elif startAtFlag:
                    try:
                        tmp = [document for document in documents if
                               list(document.values())[0][args_dict["orderBy"][1:-1]] >= args_dict["startAt"][1:-1]]
                    except:
                        tmp = [document for document in documents if
                               list(document.values())[0][args_dict["orderBy"][1:-1]] >= args_dict["startAt"]]
                    documents = tmp
                elif endAtFlag:
                    try:
                        tmp = [document for document in documents if
                               list(document.values())[0][args_dict["orderBy"][1:-1]] == args_dict["endAt"][1:-1]]
                    except:
                        tmp = [document for document in documents if
                               list(document.values())[0][args_dict["orderBy"][1:-1]] == args_dict["endAt"]]
                    documents = tmp
                else:
                    pass
    return documents


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
        documents = filterDocuments(documents, equalToFlag, startAtFlag, endAtFlag, args_dict)
        if limitToLastFlag:
            documents = documents[-int(args_dict["limitToLast"]):]
        elif limitToFirstFlag:
            documents = documents[0:int(args_dict["limitToFirst"])]
        else:
            documents = documents
    else:
        documents = documents
    return documents


@get_bp.route('/.json', defaults={'myPath': ''}, methods=['GET'])
@get_bp.route('/<path:myPath>.json', methods=['GET'])
def get(myPath):
    db = mongo.db
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
