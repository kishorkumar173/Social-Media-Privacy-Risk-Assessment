"""
Main Application Entrypoint
Flask Web Server for Social Media Privacy Risk Assessment Framework
Serves REST APIs and Static Frontend User Interfaces.
"""

import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, send_from_directory, jsonify
from backend.routes.assessment_routes import assessment_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.metadata_routes import metadata_bp
from backend.models.database import init_db

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

def create_app():
    """Application factory for Flask."""
    app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

    # Application configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-cyber-privacy-risk-framework-key-2026")
    app.config["MAX_CONTENT_LENGTH"] = 30 * 1024 * 1024  # 30 MB max upload limit

    # Initialize SQLite database
    init_db()

    # Register API Blueprints
    app.register_blueprint(assessment_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(metadata_bp)

    # Security Headers (Defensive Application Security)
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        return response

    # Frontend Static File Routes
    @app.route("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/assessment")
    def assessment_page():
        return send_from_directory(FRONTEND_DIR, "assessment.html")

    @app.route("/dashboard")
    def dashboard_page():
        return send_from_directory(FRONTEND_DIR, "dashboard.html")

    @app.route("/simulator")
    def simulator_page():
        return send_from_directory(FRONTEND_DIR, "simulator.html")

    @app.route("/metadata")
    def metadata_page():
        return send_from_directory(FRONTEND_DIR, "metadata.html")

    @app.route("/checklist")
    def checklist_page():
        return send_from_directory(FRONTEND_DIR, "checklist.html")

    # Health check endpoint
    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "healthy",
            "service": "Social Media Privacy Risk Assessment Framework",
            "version": "2.4.0",
            "framework_mode": "Defensive / Privacy-by-Design"
        })

    # Generic error handler
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Requested resource not found."}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "error": "Internal server error."}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print(f"\n==================================================================")
    print(f"🔒 Social Media Privacy Risk Assessment Framework")
    print(f"📡 Backend & Web Interface starting on http://127.0.0.1:{port}")
    print(f"🛡️  Mode: Defensive Evaluation (No scraping, No real PII stored)")
    print(f"==================================================================\n")
    app.run(host="0.0.0.0", port=port, debug=True)
