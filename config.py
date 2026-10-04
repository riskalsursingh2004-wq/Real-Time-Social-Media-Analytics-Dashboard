import os
BASE = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-env")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE, "database", "social_analytics.db")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
