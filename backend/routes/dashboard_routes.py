"""
Dashboard Routes
Provides aggregated privacy statistics, risk distributions, category averages,
and benchmark analytics for the Cybersecurity Privacy Operations Dashboard.
"""

from flask import Blueprint, jsonify
from backend.models.database import get_dashboard_aggregates, list_assessments

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/stats", methods=["GET"])
def get_stats():
    """Returns high-level KPI cards and chart data for the dashboard."""
    aggregates = get_dashboard_aggregates()
    return jsonify({
        "success": True,
        "data": aggregates
    })


@dashboard_bp.route("/recent", methods=["GET"])
def get_recent():
    """Returns list of recent privacy assessments."""
    recent = list_assessments(limit=25)
    return jsonify({
        "success": True,
        "assessments": recent
    })
