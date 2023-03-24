from flask import Flask

from .model import mongo
from .put import put_bp
from .get import get_bp
from .post import post_bp
from .patch import patch_bp
from .delete import delete_bp
from .test import test_bp

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
    mongo.init_app(app)

    app.register_blueprint(put_bp)
    app.register_blueprint(get_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(patch_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(test_bp)

    return app
