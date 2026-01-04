from flask import Flask
from app.extensions import db, migrate, login_manager, ckeditor
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.blog import blog_bp
from app.config import Config

from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    # Context processors
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(blog_bp, url_prefix="/blog")

    return app