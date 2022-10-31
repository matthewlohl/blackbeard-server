from game import db
from game.models.models import users

db.drop_all()

db.create_all()
