from flask import Flask, jsonify, render_template, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from flask_marshmallow import Marshmallow

from config import ApplicationConfig

from models import db, users


app = Flask(__name__)

app.config.from_object(ApplicationConfig)

# --- using dependencies in app ---

bcrypt = Bcrypt(app)
ma = Marshmallow(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
}, supports_credentials=True)

# --- Define your output format with marshmallow. --- 
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")

users_schema = UserSchema()
users_schema = UserSchema(many=True)

socketio = SocketIO(app, cors_allowed_origins = '*')

# --- create database ---

db.init_app(app)
with app.app_context():
    db.create_all()

# --- ROUTES --- 

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user_exist = users.query.filter_by(username=username).first() is not None
        
    if user_exist:
        return jsonify({"error": "User already exists"}),409
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = users( username= username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
            "username": new_user.username
        })

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = users.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id
    session["username"] = user.username

    response = jsonify({
        "id": user.id,
        "username": user.username
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response, 201

@app.route('/user')
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    user = users.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "username": user.username
    }), 201

# --- SOCKETS --- 

from utils.players import Players

player = Players()

@socketio.on('connect')
def connection():
    print('A new player just connected')

@socketio.on('create')
def createRoom(gameDetails):
    roomID = gameDetails["roomID"]
    host = gameDetails["host"]
    players = []
    join_room(roomID)
    print("Room ID "+ roomID + " has been created")
    print(host + " has created the room")
    player.addGame(roomID, host, players)
    emit(host, broadcast = True)

@socketio.on('join')
def joinRoom(gameDetails):
    roomID = gameDetails["roomID"]
    username = gameDetails["username"]
    print(roomID)
    join_room(roomID)
    print('Player ' + username + " just joined Room "+ roomID)
    player.addPlayer(roomID, username)

    emit(username, broadcast = True)

@socketio.on('lobby')
def lobby(gameDetails):
    host = player.grabHost(gameDetails["roomID"])
    players = player.grabPlayers(gameDetails["roomID"])
    print(host, players)
    send((host, players), broadcast = True)


if __name__ == '__main__':
    app.run(debug=True)
