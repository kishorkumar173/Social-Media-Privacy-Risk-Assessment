"""Backend Services Package"""
from .assessment_engine import validate_responses, extract_privacy_features
from .scoring_engine import calculate_category_scores, calculate_privacy_risk, determine_risk_level
from .findings_engine import generate_privacy_findings
from .recommendation_engine import generate_recommendations
from .improvement_simulator import simulate_improvements, SIMULATION_ACTIONS
from .report_generator import generate_html_report, generate_pdf_report_bytes
from .metadata_inspector import inspect_image_metadata, strip_image_metadata

__all__ = [
    "validate_responses",
    "extract_privacy_features",
    "calculate_category_scores",
    "calculate_privacy_risk",
    "determine_risk_level",
    "generate_privacy_findings",
    "generate_recommendations",
    "simulate_improvements",
    "SIMULATION_ACTIONS",
    "generate_html_report",
    "generate_pdf_report_bytes",
    "inspect_image_metadata",
    "strip_image_metadata"
]
