"""Backend Routes Package"""
from .assessment_routes import assessment_bp
from .dashboard_routes import dashboard_bp
from .metadata_routes import metadata_bp

__all__ = ["assessment_bp", "dashboard_bp", "metadata_bp"]
