"""
Privacy Improvement Simulator Service
Allows users to toggle speculative privacy improvements (e.g., enabling MFA,
hiding phone number, enabling tag review) and immediately recalculates the projected
privacy score, showing delta reduction and new risk level.
"""

from typing import Dict, Any, List
from backend.services.scoring_engine import calculate_category_scores, calculate_privacy_risk

# Mapping of simulation toggles to questionnaire question overwrites
SIMULATION_ACTIONS = {
    "make_profile_private": {
        "label": "Restrict Profile Visibility to Friends or Private",
        "overwrites": {"q1": "PRIVATE", "q2": "NO", "q3": "NO", "q4": "NO"},
        "description": "Closes profile discoverability from general search engines and unknown users."
    },
    "hide_phone": {
        "label": "Hide / Remove Personal Phone Number",
        "overwrites": {"q5": "NO"},
        "description": "Sets phone visibility to 'Only Me', preventing smishing and SIM swap reconnaissance."
    },
    "hide_email": {
        "label": "Hide Personal Email Address",
        "overwrites": {"q6": "NO"},
        "description": "Conceals personal email, reducing phishing and automated contact scraping."
    },
    "hide_birthday": {
        "label": "Hide Full Birth Date (Day, Month, Year)",
        "overwrites": {"q7": "NO"},
        "description": "Removes birth year and date used as identity tokens in account recovery."
    },
    "stop_realtime_location": {
        "label": "Disable Real-Time Location Sharing & Check-ins",
        "overwrites": {"q10": "NO", "q12": "NO", "q13": "NO"},
        "description": "Halts live venue broadcasting and disables automatic camera GPS geotags."
    },
    "post_travel_retrospectively": {
        "label": "Share Travel Plans Only After Returning Home",
        "overwrites": {"q11": "NO"},
        "description": "Eliminates empty-home signals by posting vacation updates strictly post-travel."
    },
    "enable_mfa": {
        "label": "Enable Multi-Factor Authentication (TOTP App / Security Key)",
        "overwrites": {"q26": "YES"},
        "description": "Applies secondary cryptographic authentication, preventing account takeover from stolen passwords."
    },
    "use_unique_passwords": {
        "label": "Eliminate Password Reuse with Password Manager",
        "overwrites": {"q27": "NO"},
        "description": "Generates isolated 16+ char passwords for each platform to neutralize credential stuffing."
    },
    "enable_login_alerts": {
        "label": "Turn On Unrecognized Login Alerts",
        "overwrites": {"q28": "YES", "q29": "YES", "q30": "YES"},
        "description": "Activates instant alerts and routinely audits active device sessions."
    },
    "vet_connections": {
        "label": "Strictly Reject Unknown Connection Requests",
        "overwrites": {"q18": "NO", "q19": "YES", "q20": "NO", "q21": "NO"},
        "description": "Restricts social circle to verified real-world relationships and audits inactive friends."
    },
    "enable_tag_review": {
        "label": "Enable Tag Review and Restrict Tagged Post Visibility",
        "overwrites": {"q22": "YES", "q23": "NO", "q24": "PRIVATE"},
        "description": "Requires manual confirmation before external tags appear on your timeline."
    },
    "audit_third_party_apps": {
        "label": "Revoke Stale Third-Party App Permissions",
        "overwrites": {"q31": "YES", "q32": "NO", "q33": "NO", "q34": "YES"},
        "description": "Purges old OAuth tokens and enforces least-privilege for connected services."
    },
    "filter_dms": {
        "label": "Filter Direct Messages & Verify Unknown Links",
        "overwrites": {"q35": "NO", "q36": "NO", "q37": "NO", "q38": "NO"},
        "description": "Enforces DM request filters and strict verification for links and messages."
    },
    "audit_digital_footprint": {
        "label": "Limit Historical Public Posts & Prune Dormant Accounts",
        "overwrites": {"q39": "YES", "q40": "NO", "q41": "YES", "q42": "NO"},
        "description": "Runs retroactive post limiters and closes abandoned legacy accounts."
    }
}


def simulate_improvements(baseline_responses: Dict[str, Any], selected_actions: List[str]) -> Dict[str, Any]:
    """
    Computes baseline vs. simulated improved score based on user-selected actions.
    Returns comparative analytics, score delta, and applied changes.
    """
    # 1. Calculate baseline
    baseline_cat = calculate_category_scores(baseline_responses)
    baseline_overall = calculate_privacy_risk(baseline_cat)

    # 2. Clone responses and apply selected overwrites
    simulated_responses = dict(baseline_responses)
    applied_actions = []

    for action_key in selected_actions:
        if action_key in SIMULATION_ACTIONS:
            action_meta = SIMULATION_ACTIONS[action_key]
            simulated_responses.update(action_meta["overwrites"])
            applied_actions.append({
                "action_key": action_key,
                "label": action_meta["label"],
                "description": action_meta["description"]
            })

    # 3. Calculate simulated scores
    simulated_cat = calculate_category_scores(simulated_responses)
    simulated_overall = calculate_privacy_risk(simulated_cat)

    baseline_score = baseline_overall["overall_score"]
    improved_score = simulated_overall["overall_score"]
    risk_reduction = round(baseline_score - improved_score, 1)

    return {
        "baseline": {
            "overall_score": baseline_score,
            "risk_level": baseline_overall["risk_level"],
            "color": baseline_overall["color"],
            "category_scores": baseline_cat
        },
        "simulated": {
            "overall_score": improved_score,
            "risk_level": simulated_overall["risk_level"],
            "color": simulated_overall["color"],
            "category_scores": simulated_cat
        },
        "risk_reduction_points": risk_reduction,
        "percentage_improvement": round((risk_reduction / max(1.0, baseline_score)) * 100, 1),
        "applied_actions": applied_actions,
        "disclaimer": (
            "Simulation Disclaimer: This delta reflects simulated algorithmic score reduction under our educational "
            "defensive model. It illustrates how hardening configurations shrink your attack surface, but does not "
            "represent an absolute guarantee against targeted breaches."
        )
    }
