from flask import Flask
from flask_jwt_extended import JWTManager
import os

from .model import mongo, init_admindb
from .put import put_bp
from .get import get_bp
from .post import post_bp
from .patch import patch_bp
from .delete import delete_bp
from .auth import auth_bp
from .test import test_bp

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/"
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    jwt = JWTManager(app)
    mongo.init_app(app)
    init_admindb()

    app.register_blueprint(put_bp)
    app.register_blueprint(get_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(patch_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(auth_bp)

    return app
