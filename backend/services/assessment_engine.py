"""
Assessment Engine Service
Handles validation of questionnaire responses and extraction of
structured numerical privacy features for downstream scoring and ML analysis.
"""

from typing import Dict, Any, Tuple, List
from backend.utils.questionnaire_data import QUESTIONS, QUESTION_MAP, CATEGORIES


def validate_responses(responses: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates user responses to ensure required answers are well-formed.
    Allows partial submissions by applying safe default assumptions.
    Returns (is_valid, error_messages).
    """
    errors = []
    if not isinstance(responses, dict):
        return False, ["Invalid payload: responses must be a dictionary."]

    for qid, val in responses.items():
        if qid not in QUESTION_MAP:
            # Skip unknown question IDs or log as warning
            continue
        valid_options = [opt["value"] for opt in QUESTION_MAP[qid]["options"]]
        if str(val).upper() not in valid_options:
            errors.append(f"Invalid value '{val}' for question '{qid}'. Valid options: {valid_options}")

    return len(errors) == 0, errors


def extract_privacy_features(responses: Dict[str, Any]) -> Dict[str, float]:
    """
    Extracts structured, normalized privacy-risk feature representations (0.0 to 1.0)
    from user questionnaire answers.

    Higher numerical value = HIGHER PRIVACY EXPOSURE / RISK.
    """
    features = {}

    for question in QUESTIONS:
        qid = question["id"]
        val = str(responses.get(qid, "")).upper()

        # Find matching option or assign neutral/safe default (30 risk points)
        matched = next((opt for opt in question["options"] if opt["value"] == val), None)
        if matched:
            points = matched["risk_points"]
        else:
            # Default fallback for unselected answers is 30/100 (moderate caution)
            points = 30.0

        feature_name = f"feat_{qid}"
        features[feature_name] = round(float(points) / 100.0, 4)

    # High-level aggregated domain features
    # Profile exposure feature
    features["feat_profile_public"] = 1.0 if responses.get("q1") == "PUBLIC" else (0.25 if responses.get("q1") == "FRIENDS" else 0.0)
    # Contact exposure features
    features["feat_phone_exposed"] = 1.0 if responses.get("q5") == "YES" else 0.0
    features["feat_email_exposed"] = 0.85 if responses.get("q6") == "YES" else 0.0
    features["feat_birthday_exposed"] = 0.95 if responses.get("q7") == "YES" else (0.40 if responses.get("q7") == "SOMETIMES" else 0.0)
    # Location features
    features["feat_realtime_location"] = 1.0 if responses.get("q10") == "YES" else (0.60 if responses.get("q10") == "SOMETIMES" else 0.0)
    features["feat_travel_announced"] = 0.90 if responses.get("q11") == "YES" else (0.50 if responses.get("q11") == "SOMETIMES" else 0.0)
    # Security controls
    features["feat_mfa_missing"] = 1.0 if responses.get("q26") == "NO" else (0.30 if responses.get("q26") == "SOMETIMES" else 0.0)
    features["feat_password_reused"] = 0.95 if responses.get("q27") == "YES" else (0.70 if responses.get("q27") == "SOMETIMES" else 0.0)
    features["feat_login_alerts_missing"] = 0.80 if responses.get("q28") == "NO" else 0.0
    # Social engineering and apps
    features["feat_unknown_contacts_accepted"] = 0.90 if responses.get("q18") == "YES" else (0.50 if responses.get("q18") == "SOMETIMES" else 0.0)
    features["feat_tag_review_disabled"] = 0.90 if responses.get("q22") == "NO" else 0.0
    features["feat_third_party_unreviewed"] = 0.85 if responses.get("q31") == "NO" else (0.45 if responses.get("q31") == "SOMETIMES" else 0.0)

    return features
