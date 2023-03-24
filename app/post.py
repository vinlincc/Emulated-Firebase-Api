from flask import Blueprint
from .model import mongo

post_bp = Blueprint('post', __name__)

@post_bp.route('/', defaults={'myPath': ''},methods=['POST'] )
@post_bp.route('/<path:myPath>', methods=['POST'])
def post(myPath):
    db = mongo.db
    pass

