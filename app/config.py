import os

class Config:
    SECRET_KEY = "123456789"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///events.db"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/event_management_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
