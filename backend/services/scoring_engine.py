"""
Scoring Engine Service
Calculates category-wise privacy scores (0-100) and weighted overall privacy risk.
Categorizes overall risk into LOW, MODERATE, HIGH, and CRITICAL tiers.
"""

from typing import Dict, Any, Optional
from backend.utils.questionnaire_data import CATEGORIES, QUESTIONS, QUESTION_MAP

DEFAULT_WEIGHTS = {cat_id: meta["weight"] for cat_id, meta in CATEGORIES.items()}

# Risk tier thresholds
# 0-20: LOW
# 21-40: MODERATE
# 41-70: HIGH
# 71-100: CRITICAL
RISK_LEVEL_THRESHOLDS = [
    (20.0, "LOW", "#10b981", "Well-contained exposure. Essential defenses and private settings are active."),
    (40.0, "MODERATE", "#3b82f6", "Acceptable baseline, but non-essential personal datapoints or weak secondary controls exist."),
    (70.0, "HIGH", "#f59e0b", "Significant exposure. High-risk vectors like contact leaks, public location, or absent MFA detected."),
    (100.0, "CRITICAL", "#ef4444", "Severe privacy vulnerability. Extensive public footprint, active location broadcasting, and missing defenses.")
]


def determine_risk_level(score: float) -> Dict[str, str]:
    """Returns classification dictionary for a given 0-100 score."""
    clamped = max(0.0, min(100.0, float(score)))
    for threshold, level, color, desc in RISK_LEVEL_THRESHOLDS:
        if clamped <= threshold:
            return {
                "level": level,
                "color": color,
                "description": desc
            }
    # Fallback to critical
    return {
        "level": "CRITICAL",
        "color": "#ef4444",
        "description": RISK_LEVEL_THRESHOLDS[-1][3]
    }


def calculate_category_scores(responses: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Computes 0-100 score for each of the 10 privacy assessment categories.
    Higher score indicates HIGHER RISK / GREATER EXPOSURE.
    """
    category_accumulators = {cat_id: {"total_points": 0.0, "count": 0} for cat_id in CATEGORIES}

    for question in QUESTIONS:
        cat_id = question["category"]
        qid = question["id"]
        val = str(responses.get(qid, "")).upper()

        matched = next((opt for opt in question["options"] if opt["value"] == val), None)
        if matched:
            points = float(matched["risk_points"])
        else:
            # Conservative midpoint if question was omitted
            points = 30.0

        category_accumulators[cat_id]["total_points"] += points
        category_accumulators[cat_id]["count"] += 1

    category_results = {}
    for cat_id, meta in CATEGORIES.items():
        acc = category_accumulators[cat_id]
        if acc["count"] > 0:
            avg_score = round(acc["total_points"] / acc["count"], 1)
        else:
            avg_score = 0.0

        clamped = max(0.0, min(100.0, avg_score))
        level_info = determine_risk_level(clamped)

        category_results[cat_id] = {
            "category_id": cat_id,
            "name": meta["name"],
            "score": clamped,
            "weight": meta["weight"],
            "icon": meta.get("icon", "bi-shield"),
            "risk_level": level_info["level"],
            "color": level_info["color"],
            "description": meta["description"]
        }

    return category_results


def calculate_privacy_risk(category_scores: Dict[str, Dict[str, Any]], custom_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Calculates weighted overall privacy risk score (0-100) and risk tier.
    Accepts optional custom category weights that are normalized to 1.0.
    """
    weights = custom_weights if custom_weights else DEFAULT_WEIGHTS

    total_weight = sum(weights.values())
    if total_weight <= 0:
        total_weight = 1.0

    weighted_score = 0.0
    for cat_id, cat_data in category_scores.items():
        score = cat_data["score"]
        w = weights.get(cat_id, DEFAULT_WEIGHTS.get(cat_id, 0.10))
        normalized_w = w / total_weight
        weighted_score += score * normalized_w

    overall_score = round(max(0.0, min(100.0, weighted_score)), 1)
    tier = determine_risk_level(overall_score)

    return {
        "overall_score": overall_score,
        "risk_level": tier["level"],
        "color": tier["color"],
        "description": tier["description"],
        "category_scores": category_scores,
        "disclaimer": (
            "Educational Risk Assessment: This score reflects self-reported privacy settings and "
            "exposure habits under a defensive evaluation model. It is not an empirical guarantee of safety "
            "or compromise."
        )
    }
