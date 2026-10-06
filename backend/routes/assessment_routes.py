"""
Assessment Routes
Handles privacy assessment evaluation, retrieval, simulation, report export, and checklist endpoints.
"""

from flask import Blueprint, request, jsonify, Response
from backend.services.assessment_engine import validate_responses, extract_privacy_features
from backend.services.scoring_engine import calculate_category_scores, calculate_privacy_risk
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.improvement_simulator import simulate_improvements, SIMULATION_ACTIONS
from backend.services.report_generator import generate_html_report, generate_pdf_report_bytes
from backend.models.database import save_assessment, get_assessment, delete_assessment, list_assessments
from backend.utils.questionnaire_data import QUESTIONS, CATEGORIES

assessment_bp = Blueprint("assessment", __name__, url_prefix="/api")

# Safe Demonstration Profile (Section 32 of prompt)
DEMO_HIGH_RISK_PROFILE = {
    "q1": "PUBLIC",     # Profile public
    "q2": "YES",        # Search indexing enabled
    "q3": "YES",        # Friend list public
    "q4": "YES",        # Phone/email discoverable
    "q5": "YES",        # Phone number public
    "q6": "YES",        # Personal email public
    "q7": "YES",        # Full birthday public
    "q8": "YES",        # Workplace public
    "q9": "YES",        # Family relationships public
    "q10": "YES",       # Real-time checkins
    "q11": "YES",       # Travel plans posted in advance
    "q12": "YES",       # Geotagging enabled
    "q13": "YES",       # Home address deduced
    "q14": "PUBLIC",    # Everyday posts public
    "q15": "YES",       # Work badges/screens posted
    "q16": "YES",       # Kids photos public
    "q17": "YES",       # Quizzes answered
    "q18": "YES",       # Unknown connections accepted
    "q19": "NO",        # Contacts never pruned
    "q20": "YES",       # Open friend requests
    "q21": "YES",       # Accepted cloned profiles
    "q22": "NO",        # Tag review disabled
    "q23": "YES",       # Strangers can tag
    "q24": "PUBLIC",    # Tagged posts visible
    "q25": "YES",       # Open mentions
    "q26": "NO",        # MFA disabled
    "q27": "YES",       # Password reused
    "q28": "NO",        # Login alerts disabled
    "q29": "NO",        # Active sessions unreviewed
    "q30": "NO",        # Recovery email outdated
    "q31": "NO",        # Third party apps unreviewed
    "q32": "YES",       # Random social sign-ins
    "q33": "YES",       # Third party write permissions
    "q34": "NO",        # App reputations unverified
    "q35": "YES",       # Open DMs
    "q36": "YES",       # Urgent DM money/codes trusted
    "q37": "YES",       # Click giveaway links
    "q38": "YES",       # Sensitive info in chat
    "q39": "NO",        # Historical posts not audited
    "q40": "YES",       # Abandoned accounts active
    "q41": "NO",        # Never googled self
    "q42": "YES"        # Public comments under real name
}


@assessment_bp.route("/questions", methods=["GET"])
def get_questions():
    """Returns questionnaire structure and categories."""
    return jsonify({
        "success": True,
        "total_questions": len(QUESTIONS),
        "categories": CATEGORIES,
        "questions": QUESTIONS
    })


@assessment_bp.route("/demo-profile", methods=["GET"])
def get_demo_profile():
    """Returns the pre-configured high-exposure demonstration profile for quick testing."""
    return jsonify({
        "success": True,
        "profile_name": "High-Exposure Vulnerable Profile (Fictional Demo)",
        "responses": DEMO_HIGH_RISK_PROFILE
    })


@assessment_bp.route("/assessment", methods=["POST"])
def create_assessment():
    """
    Evaluates submitted questionnaire answers.
    Generates scores, findings, recommendations, saves to database, and returns results.
    """
    payload = request.get_json() or {}
    responses = payload.get("responses", {})
    custom_weights = payload.get("custom_weights", None)

    is_valid, errors = validate_responses(responses)
    if not is_valid:
        return jsonify({"success": False, "errors": errors}), 400

    # 1. Feature Extraction
    features = extract_privacy_features(responses)

    # 2. Category Scoring
    category_scores = calculate_category_scores(responses)

    # 3. Overall Risk Calculation
    overall_result = calculate_privacy_risk(category_scores, custom_weights)

    # 4. Findings Engine
    findings = generate_privacy_findings(responses)

    # 5. Recommendation Engine
    recommendations = generate_recommendations(findings)

    # Assemble structured object
    assessment_data = {
        "overall_score": overall_result["overall_score"],
        "risk_level": overall_result["risk_level"],
        "color": overall_result["color"],
        "description": overall_result["description"],
        "disclaimer": overall_result["disclaimer"],
        "features": features,
        "responses": responses,
        "category_scores": category_scores,
        "findings": findings,
        "recommendations": recommendations
    }

    # Persist in SQLite
    assessment_id = save_assessment(assessment_data)
    assessment_data["assessment_id"] = assessment_id

    return jsonify({
        "success": True,
        "assessment_id": assessment_id,
        "data": assessment_data
    }), 201


@assessment_bp.route("/assessment/<assessment_id>", methods=["GET"])
def retrieve_assessment(assessment_id: str):
    """Retrieves an existing assessment by ID."""
    record = get_assessment(assessment_id)
    if not record:
        return jsonify({"success": False, "error": "Assessment not found"}), 404
    return jsonify({"success": True, "data": record})


@assessment_bp.route("/assessment/<assessment_id>/recommendations", methods=["GET"])
def retrieve_recommendations(assessment_id: str):
    """Retrieves recommendations for a specific assessment."""
    record = get_assessment(assessment_id)
    if not record:
        return jsonify({"success": False, "error": "Assessment not found"}), 404
    return jsonify({
        "success": True,
        "assessment_id": assessment_id,
        "recommendations": record.get("recommendations", [])
    })


@assessment_bp.route("/assessment/<assessment_id>", methods=["DELETE"])
def remove_assessment(assessment_id: str):
    """Deletes an assessment record (Privacy by Design - Right to Erasure)."""
    success = delete_assessment(assessment_id)
    if not success:
        return jsonify({"success": False, "error": "Assessment not found"}), 404
    return jsonify({"success": True, "message": f"Assessment {assessment_id} permanently erased."})


@assessment_bp.route("/assessment/simulate-improvement", methods=["POST"])
def simulate_improvement_route():
    """Simulates impact of privacy hardening actions on baseline questionnaire responses."""
    payload = request.get_json() or {}
    baseline_responses = payload.get("responses", {})
    selected_actions = payload.get("actions", [])

    if not baseline_responses:
        # If no baseline provided, fall back to high-risk demo profile
        baseline_responses = DEMO_HIGH_RISK_PROFILE

    result = simulate_improvements(baseline_responses, selected_actions)
    result["available_actions"] = SIMULATION_ACTIONS
    return jsonify({"success": True, "data": result})


@assessment_bp.route("/simulation-actions", methods=["GET"])
def list_simulation_actions():
    """Lists all available simulation hardening actions."""
    return jsonify({"success": True, "actions": SIMULATION_ACTIONS})


@assessment_bp.route("/privacy-checklist", methods=["GET"])
def get_privacy_checklist():
    """Returns downloadable / printable privacy checklist items."""
    checklist = [
        {"id": "chk1", "category": "Profile", "task": "Set primary profile visibility to 'Friends' or 'Private'"},
        {"id": "chk2", "category": "Profile", "task": "Turn off search engine indexing in privacy settings"},
        {"id": "chk3", "category": "Contact", "task": "Hide personal phone number from public bio and lookup"},
        {"id": "chk4", "category": "Contact", "task": "Conceal personal email or configure a masked email alias"},
        {"id": "chk5", "category": "Identity", "task": "Hide birth year or full birth date to prevent identity theft"},
        {"id": "chk6", "category": "Location", "task": "Disable real-time venue check-ins and live location sharing"},
        {"id": "chk7", "category": "Location", "task": "Post travel updates and vacation photos only after returning home"},
        {"id": "chk8", "category": "Location", "task": "Turn off camera GPS geotagging in mobile OS settings"},
        {"id": "chk9", "category": "Content", "task": "Never post photos showing work badges, flight boarding passes, or screens"},
        {"id": "chk10", "category": "Content", "task": "Avoid answering viral social quizzes asking for childhood memories"},
        {"id": "chk11", "category": "Tagging", "task": "Enable Timeline Tag Review before tags appear on your profile"},
        {"id": "chk12", "category": "Tagging", "task": "Restrict who can tag you to approved friends only"},
        {"id": "chk13", "category": "Connections", "task": "Decline friend requests from unknown profiles or unverified clones"},
        {"id": "chk14", "category": "Authentication", "task": "Enable Multi-Factor Authentication using a TOTP Authenticator app"},
        {"id": "chk15", "category": "Authentication", "task": "Use a Password Manager to generate unique passwords for every site"},
        {"id": "chk16", "category": "Authentication", "task": "Enable alerts for unrecognized logins from new devices"},
        {"id": "chk17", "category": "Apps", "task": "Review and revoke permissions for stale third-party apps and games"},
        {"id": "chk18", "category": "Footprint", "task": "Use 'Limit Past Posts' to batch-restrict historical public shares"}
    ]
    return jsonify({"success": True, "checklist": checklist})


@assessment_bp.route("/assessment/<assessment_id>/report.html", methods=["GET"])
def export_html_report(assessment_id: str):
    """Renders printable, standalone HTML assessment report."""
    record = get_assessment(assessment_id)
    if not record:
        return "Assessment not found", 404
    html_content = generate_html_report(record)
    return Response(html_content, mimetype="text/html")


@assessment_bp.route("/assessment/<assessment_id>/report.pdf", methods=["GET"])
def export_pdf_report(assessment_id: str):
    """Generates direct downloadable PDF assessment report."""
    record = get_assessment(assessment_id)
    if not record:
        return jsonify({"success": False, "error": "Assessment not found"}), 404
    try:
        pdf_bytes = generate_pdf_report_bytes(record)
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=privacy_report_{assessment_id}.pdf"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
