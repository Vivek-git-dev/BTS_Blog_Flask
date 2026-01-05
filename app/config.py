import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    # Handle different database URL formats
    if database_url:
        # Replace old postgres:// scheme with postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback to SQLite only for local development
        SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_REGISTRATION_KEY = os.getenv("ADMIN_REGISTRATION_KEY")