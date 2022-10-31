# from flask_sqlalchemy import SQLAlchemy 
# db = SQLAlchemy()
# import sqlalchemy as sa
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref


from ..database.db import db
# Base = declarative_base()
# engine = sa.create_engine("sqlite:///:memory:")
# session = scoped_session(sessionmaker(bind=engine))

#create a model
class users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    games_won = db.Column(db.Integer)
