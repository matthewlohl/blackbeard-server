# from flask_sqlalchemy import SQLAlchemy 
# db = SQLAlchemy()
from ..database.db import db

#create a model
class users(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    games_won = db.Column(db.Integer)
