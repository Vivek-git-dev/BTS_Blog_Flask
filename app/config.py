import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    uri = os.getenv("DATABASE_URL", "sqlite:///blog.db")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_REGISTRATION_KEY = os.getenv("ADMIN_REGISTRATION_KEY")