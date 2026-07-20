"""Updated Flask app with database, auth, and all routes."""

import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from src.database import init_db
from src.database.models import db

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def create_app(config_name='development'):
    """Create and configure Flask application.
    
    Args:
        config_name: Configuration name (development, testing, production)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config["DEBUG"] = os.getenv("APP_DEBUG", "False").lower() == "true"
    app.config["JSON_AS_ASCII"] = False  # Support Thai characters
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///pkpro.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "dev-secret-key-change-in-production"
    )
    
    # Enable CORS
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Initialize database
    with app.app_context():
        init_db(app)
    
    # Register blueprints
    from src.ui.routes import api_bp
    from src.ui.routes_auth import auth_bp
    from src.ui.routes_chat import chat_bp
    from src.ui.routes_logs import log_bp
    from src.ui.routes_scripts import script_bp
    from src.ui.routes_kb import kb_bp
    
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(script_bp)
    app.register_blueprint(kb_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found", "status": 404}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error", "status": 500}, 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {"error": "Unauthorized", "status": 401}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {"error": "Forbidden", "status": 403}, 403
    
    # Health check
    @app.route("/health")
    def health():
        return {"status": "healthy", "app": "AI IT Technician Assistant"}
    
    # Index
    @app.route("/")
    def index():
        return {
            "app": "AI IT Technician Assistant",
            "version": "1.0.0",
            "status": "running",
            "documentation": "/api/docs",
            "auth_required": "Most endpoints require JWT token",
            "get_started": {
                "1_register": "POST /api/auth/register",
                "2_login": "POST /api/auth/login",
                "3_chat": "POST /api/chat/send"
            }
        }
    
    return app
