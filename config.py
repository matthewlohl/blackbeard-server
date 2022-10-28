class ApplicationConfig:
    SECRET_KEY = "be6865bf45c2fdf0a1997cc0f4e7c488"
    SQLALCHEMY_DATABASE_URI = r'sqlite:///db.sqlite3'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
