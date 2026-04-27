import datetime

class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)