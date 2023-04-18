from flask import Blueprint, request, jsonify
from .model import mongo
import json
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/.register', methods=['POST'])
def register():
    input_data = request.get_json(force=True)
    username = input_data.get("username")
    password = input_data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400
    admindb = mongo.cx['admin']
    existing_user = admindb.users.find_one({"username": username})

    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    admindb.users.insert_one({"username": username, "password": hashed_password})
    user_database = f"db_{username}"
    db = mongo.cx[user_database]
    db.create_collection("index")
    return jsonify({"result": "User created"}), 201

@auth_bp.route('/.login', methods=['POST'])
def login():
    input_data = request.get_json(force=True)
    username = input_data.get("username")
    password = input_data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400
    admindb = mongo.cx['admin']
    user = admindb.users.find_one({"username": username})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
















