from flask import Blueprint
from .model import mongo

delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/', defaults={'myPath': ''},methods=['DELETE'] )
@delete_bp.route('/<path:myPath>', methods=['DELETE'])
def delete(myPath):
    db = mongo.db
    pass