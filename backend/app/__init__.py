from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)

    # Load configuration
    if config is None:
        from backend.config import Config
        app.config.from_object(Config)
    elif isinstance(config, dict):
        app.config.update(config)
    else:
        app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
    }})

    # Configure Cloudinary
    import cloudinary
    cloudinary.config(
        cloud_name=app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=app.config.get("CLOUDINARY_API_KEY"),
        api_secret=app.config.get("CLOUDINARY_API_SECRET"),
    )

    # Initialize Groq client at startup (reserved for future AI features)
    from backend.app import groq_client as _groq_client  # noqa: F401

    # Import models and create tables
    with app.app_context():
        from backend.app.models import models  # noqa: F401 — registers models with SQLAlchemy
        db.create_all()

    # Register blueprints (placeholders — implemented in later tasks)
    _register_blueprints(app)

    # Global error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": str(e.description) if hasattr(e, "description") else "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": str(e.description) if hasattr(e, "description") else "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": str(e.description) if hasattr(e, "description") else "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e.description) if hasattr(e, "description") else "Not found"}), 404

    @app.errorhandler(409)
    def conflict(e):
        return jsonify({"error": str(e.description) if hasattr(e, "description") else "Conflict"}), 409

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


def _register_blueprints(app):
    """Register all application blueprints."""
    try:
        from backend.app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
    except ImportError:
        pass  # Auth routes not yet implemented

    try:
        from backend.app.routes.job_routes import jobs_bp
        app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
    except ImportError:
        pass  # Job routes not yet implemented

    try:
        from backend.app.routes.stats_routes import stats_bp
        app.register_blueprint(stats_bp, url_prefix="/api/stats")
    except ImportError:
        pass  # Stats routes not yet implemented

    try:
        from backend.app.routes.proxy_routes import proxy_bp
        app.register_blueprint(proxy_bp, url_prefix="/api/proxy")
    except ImportError:
        pass  # Proxy routes not yet implemented

    try:
        from backend.app.routes.profile_routes import profile_bp
        app.register_blueprint(profile_bp, url_prefix="/api/profile")
    except ImportError:
        pass  # Profile routes not yet implemented

    try:
        from backend.app.routes.chat_routes import chat_bp
        app.register_blueprint(chat_bp, url_prefix="/api/chat")
    except ImportError:
        pass  # Chat routes not yet implemented
