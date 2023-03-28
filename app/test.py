from flask import Blueprint
from .model import mongo

test_bp = Blueprint('test', __name__)


@test_bp.route('/test')
def test():
    db = mongo.db
    db.test.insert_one({"message": "Hello, MongoDB!"})
    document = mongo.db.test.find_one({"message": "Hello, MongoDB!"})
    # document = db.get_test.find_one({"yxj": {"$exists": True}},{'_id':0})
    return document