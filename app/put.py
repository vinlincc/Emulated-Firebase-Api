from flask import Blueprint
from .model import mongo

put_bp = Blueprint('put', __name__)

@put_bp.route('/', defaults={'myPath': ''},methods=['PUT'] )
@put_bp.route('/<path:myPath>', methods=['PUT'])
def put(myPath):
    db = mongo.db
    pass