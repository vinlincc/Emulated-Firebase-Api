from flask import Blueprint
from .model import mongo

patch_bp = Blueprint('patch', __name__)

@patch_bp.route('/', defaults={'myPath': ''},methods=['PATCH'] )
@patch_bp.route('/<path:myPath>', methods=['PATCH'])
def patch(myPath):
    db = mongo.db
    pass