#import dependencies
from dotenv import load_dotenv
from os import environ
from flask_cors import CORS
from flask import Flask

#import models, database
from .database.db import db
from .routes.main import app

#Load environment variables

load_dotenv()

database_uri = environ.get('DATABASE_URL')

if 'postgres:' in database_uri:
    database_uri = database_uri.replace("postgres:", "postgresql:")

# Set up the app

# app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
)

# --- using dependencies in app ---

cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
}, supports_credentials=True)

db.app=app
db.init_app(app)

# app.register_blueprint(main_routes)

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
