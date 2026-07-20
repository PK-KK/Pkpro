"""Flask application factory and configuration."""

import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def create_app():
    """Create and configure Flask application.
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config["DEBUG"] = os.getenv("APP_DEBUG", "False").lower() == "true"
    app.config["JSON_AS_ASCII"] = False  # Support Thai characters
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found", "status": 404}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error", "status": 500}, 500
    
    # Health check
    @app.route("/health")
    def health():
        return {"status": "healthy", "app": "AI IT Technician Assistant"}
    
    # Index
    @app.route("/")
    def index():
        return {
            "app": "AI IT Technician Assistant",
            "version": "0.1.0",
            "documentation": "/api/docs",
            "endpoints": {
                "chat": "POST /api/chat",
                "analyze_log": "POST /api/analyze-log",
                "generate_script": "POST /api/generate-script",
                "knowledge_base": "GET /api/knowledge-base",
                "health": "GET /health"
            }
        }
    
    return app
