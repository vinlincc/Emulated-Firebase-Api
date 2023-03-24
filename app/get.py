from flask import Blueprint
from .model import mongo

get_bp = Blueprint('get', __name__)

@get_bp.route('/', defaults={'myPath': ''},methods=['GET'] )
@get_bp.route('/<path:myPath>', methods=['GET'])
def get(myPath):
    db = mongo.db
    pass