from flask import Flask, jsonify, render_template, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin


from config import ApplicationConfig

from models import db, users



app = Flask(__name__)

app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)

db.init_app(app)
CORS(app, supports_credentials=True)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST', 'GET'])
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

    return response

@app.route('/user')
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    user = users.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "username": user.username
    })

if __name__ == '__main__':
    app.run(debug=True)
