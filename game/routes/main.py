# import dependencies
from flask import Flask, Blueprint, jsonify, request, session
from flask_bcrypt import Bcrypt

# import models, database
from ..database.db import db
from ..models.models import users

main_routes = Blueprint("main", __name__)

# --- using dependencies in app ---
app = Flask(__name__)
bcrypt = Bcrypt(app)


# --- ROUTES --- 

@main_routes.route("/")
def home():
    return "Welcome to Black Beard's Island API"


@main_routes.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user_exist = users.query.filter_by(username=username).first() is not None
        
    if user_exist:
        return jsonify({"error": "User already exists"}),409
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = users( username= username, password=hashed_password, games_won = 0)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
            "username": new_user.username
        })

@main_routes.route('/login', methods=['POST', 'GET'])
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = users.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.user_id
    session["username"] = user.username

    response = jsonify({
        "id": user.user_id,
        "username": user.username
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response, 201

@main_routes.route('/users')
def get_all_users():
    all_users = users.first()
    return jsonify({
        all_users
    }), 200

@main_routes.route('/user')
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    user = users.query.filter_by(user_id=user_id).first()
    return jsonify({
        "id": user.user_id,
        "username": user.username
    }), 201
