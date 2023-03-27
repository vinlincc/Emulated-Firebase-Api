from flask import Blueprint,request,jsonify
from .model import mongo
from .put import check_path
get_bp = Blueprint('get', __name__)


# def findAll(documents,paths):
#     documents_list = []
#     if len(paths) != 0:
#         last = paths.pop()
#     for document in documents:
#         if len(paths) >= 1:
#             for path in paths:
#                 document = document[path]
#             for item in document.items():
#                 if last == item[0]:
#                     document = {item[0],[item[1]]}
#                     break
#                 else:
#                     continue
#         documents_list.append(str(document))
#     return documents_list

def findAll(documents,paths):
    documents_list = []
    if len(paths) <= 1:
        for i in documents:
             documents_list.append(str(i))
    else:
        last = paths.pop()
        document = next(documents)
        for path in paths:
            document = document[path]
        if (len(document) != 1):
            for item in document.items():
                if item[0] == last:
                    tmp = {}
                    tmp[item[0]] = item[1]
                    document = tmp
                    documents_list.append(str(document))
                    break
                else:
                    continue
        else:
            documents_list.append(str(document))
    return documents_list

# def projection(columns):
#     project_dict = {}
#     project_dict[".".join(columns)] = 1
#     project_dict["_id"] = 0
#     return project_dict


@get_bp.route('/.json', defaults={'myPath': ''},methods=['GET'])
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
    equalToFlag = True if args_keys.__contains__("equalToFirst") else False
    startAtFlag = True if args_keys.__contains__("startAtFirst") else False
    endAtFlag = True if args_keys.__contains__("endAtFirst") else False
    if orderByFlag:
        if equalToFlag:
            if limitToFirstFlag:
                pass
            elif limitToLastFlag:
                pass
            else:
                pass
        elif startAtFlag:
            if limitToFirstFlag:
                pass
            elif limitToLastFlag:
                pass
            else:
                pass
        elif endAtFlag:
            if limitToFirstFlag:
                pass
            elif limitToLastFlag:
                pass
            else:
                pass
        elif limitToFirstFlag:
            pass
        elif limitToLastFlag:
            pass
        else:
            pass
    else:
        length = len(path)
        if length == 1:
            documents = db[path[0]].find()
        elif length == 2:
            documents = db[path[0]].find({path[1]:{"$exists":True}})
        else:
            documents = db[path[0]].find({path[1]: {"$exists": True}})
        documents = findAll(documents,path[1:])
    return documents

