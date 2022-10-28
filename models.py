from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

#create a model
class users(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email
