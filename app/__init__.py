from flask import Flask, jsonify
from config import Config
from app.extensions import db, migrate
from app.controllers.api import api_bp

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    migrate.init_app(app, db)
    from app import models  # register models
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.get("/")
    def index():
        return jsonify({"service": "CyberSOC API", "version": "1.0.0",
                        "description": "Security event monitoring and incident response API"})

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"success": False, "error": {
            "code": "NOT_FOUND", "message": "Resource or endpoint not found"}}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"success": False, "error": {
            "code": "METHOD_NOT_ALLOWED", "message": "HTTP method not allowed"}}), 405

    @app.errorhandler(500)
    def internal_error(_):
        db.session.rollback()
        return jsonify({"success": False, "error": {
            "code": "INTERNAL_SERVER_ERROR", "message": "Unexpected server error"}}), 500
    return app
