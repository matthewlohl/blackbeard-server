# import dependencies
from flask import Flask, Blueprint, jsonify, request, session, make_response
from flask_bcrypt import Bcrypt
from functools import wraps
import jwt

from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()

class users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    games_won = db.Column(db.Integer)


# --- using dependencies in app ---
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY']='1ef10e845d42fa327de97f1991928bc5'

# --- ROUTES --- 

@app.route("/")
def home():
    return "Welcome to Black Beard's Island API"


@app.route('/register', methods=['POST'])
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
    response = jsonify({
            "username": new_user.username
        })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 201

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.json["username"]
    password = request.json["password"]
    user = users.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "User doesn't not exist"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401


    token = jwt.encode({
            'username': user.username
        }, app.config['SECRET_KEY'])
    session["user_id"] = user.user_id
    session["username"] = user.username

    print(token)
    token_decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    print(token_decoded)
    return jsonify({
        # "id": user.user_id,
        # "username": user.username,
        'token': token
    }), 201
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response, 201

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f( *args, **kwargs)
  
    return decorated

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = users.query.with_entities(users.username, users.games_won)
    players = []
    for user in all_users:
        players.append({
            "username": user.username,
            "games_won": user.games_won
            })
    return players, 200

@app.route('/token', methods=['GET'])
@token_required
def token_validation():
    all_users = users.query.with_entities(users.username, users.games_won)
    players = []
    for user in all_users:
        players.append({
            "username": user.username,
            "games_won": user.games_won
            })
    return players, 200

@app.route('/gameover', methods=['GET', 'POST'])
@token_required
def add_score():
    winner = request.json["username"]
    user = users.query.filter_by(username=winner).first()
    if user is None:
        return jsonify({"error": "User doesn't not exist"}), 401
    user.games_won += 1
    db.session.add(user)
    db.session.commit()
    response = jsonify({
            "username": user.username,
            "games_won": user.games_won
        })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 201

    
