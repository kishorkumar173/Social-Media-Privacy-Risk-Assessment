"""
Synthetic Profile Dataset Generator
Generates at least 1,000 realistic, fully fictional privacy assessment profiles
using defensive privacy attributes and probabilistic behavior distributions.
Computes privacy risk score (0-100) and risk level (LOW, MODERATE, HIGH, CRITICAL).
Saves output to data/social_media_privacy_assessments.csv and seeds the SQLite database.
"""

import os
import sys
import csv
import random
import uuid
import datetime

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.services.scoring_engine import calculate_category_scores, calculate_privacy_risk
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.assessment_engine import extract_privacy_features
from backend.models.database import init_db, save_assessment


def generate_synthetic_record(idx: int):
    """
    Generates a realistic fictional user response set across multiple persona distributions:
    - Privacy Champion (15%): Low risk
    - Average Internet User (45%): Moderate / High risk
    - Oversharer / High Exposure (30%): High / Critical risk
    - Tech Naive / Vulnerable (10%): Critical risk
    """
    persona = random.choices(
        ["CHAMPION", "AVERAGE", "OVERSHARER", "VULNERABLE"],
        weights=[0.15, 0.45, 0.30, 0.10],
        k=1
    )[0]

    if persona == "CHAMPION":
        p_vis = random.choices(["PRIVATE", "FRIENDS"], weights=[0.8, 0.2])[0]
        phone = "NO"
        email = random.choices(["NO", "SOMETIMES"], weights=[0.9, 0.1])[0]
        bday = "NO"
        loc_rt = "NO"
        travel = random.choices(["NO", "SOMETIMES"], weights=[0.85, 0.15])[0]
        mfa = "YES"
        pwd_reuse = "NO"
        alerts = "YES"
        unknown_conn = "NO"
        tag_rev = "YES"
        third_p = "YES"
        old_posts = "YES"
        review_sett = "YES"
    elif persona == "AVERAGE":
        p_vis = random.choices(["PUBLIC", "FRIENDS", "PRIVATE"], weights=[0.35, 0.55, 0.10])[0]
        phone = random.choices(["YES", "NO", "SOMETIMES"], weights=[0.20, 0.70, 0.10])[0]
        email = random.choices(["YES", "NO", "SOMETIMES"], weights=[0.35, 0.55, 0.10])[0]
        bday = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.30, 0.50, 0.20])[0]
        loc_rt = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.25, 0.45, 0.30])[0]
        travel = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.30, 0.40, 0.30])[0]
        mfa = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.40, 0.30, 0.30])[0]
        pwd_reuse = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.35, 0.40, 0.25])[0]
        alerts = random.choices(["YES", "NO", "NOT_SURE"], weights=[0.45, 0.35, 0.20])[0]
        unknown_conn = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.20, 0.45, 0.35])[0]
        tag_rev = random.choices(["YES", "NO", "NOT_SURE"], weights=[0.40, 0.40, 0.20])[0]
        third_p = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.25, 0.45, 0.30])[0]
        old_posts = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.20, 0.40, 0.40])[0]
        review_sett = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.30, 0.40, 0.30])[0]
    elif persona == "OVERSHARER":
        p_vis = "PUBLIC"
        phone = random.choices(["YES", "NO", "SOMETIMES"], weights=[0.60, 0.25, 0.15])[0]
        email = "YES"
        bday = random.choices(["YES", "SOMETIMES"], weights=[0.75, 0.25])[0]
        loc_rt = random.choices(["YES", "SOMETIMES"], weights=[0.70, 0.30])[0]
        travel = "YES"
        mfa = random.choices(["SOMETIMES", "NO"], weights=[0.30, 0.70])[0]
        pwd_reuse = random.choices(["YES", "SOMETIMES"], weights=[0.60, 0.40])[0]
        alerts = "NO"
        unknown_conn = random.choices(["YES", "SOMETIMES"], weights=[0.70, 0.30])[0]
        tag_rev = "NO"
        third_p = "NO"
        old_posts = "NO"
        review_sett = "NO"
    else:  # VULNERABLE
        p_vis = "PUBLIC"
        phone = "YES"
        email = "YES"
        bday = "YES"
        loc_rt = "YES"
        travel = "YES"
        mfa = "NO"
        pwd_reuse = "YES"
        alerts = "NO"
        unknown_conn = "YES"
        tag_rev = "NO"
        third_p = "NO"
        old_posts = "NO"
        review_sett = "NO"

    # Map to 42 questionnaire keys
    responses = {
        "q1": p_vis,
        "q2": "YES" if p_vis == "PUBLIC" else ("NO" if p_vis == "PRIVATE" else random.choice(["YES", "NO"])),
        "q3": "YES" if p_vis == "PUBLIC" else random.choice(["NO", "SOMETIMES"]),
        "q4": "YES" if phone == "YES" or email == "YES" else random.choice(["NO", "NOT_SURE"]),
        "q5": phone,
        "q6": email,
        "q7": bday,
        "q8": random.choice(["YES", "NO", "SOMETIMES"]),
        "q9": random.choice(["YES", "NO", "SOMETIMES"]),
        "q10": loc_rt,
        "q11": travel,
        "q12": random.choice(["YES", "NO"]),
        "q13": random.choice(["YES", "NO", "SOMETIMES"]),
        "q14": p_vis,
        "q15": random.choice(["YES", "NO", "SOMETIMES"]),
        "q16": random.choice(["YES", "NO", "SOMETIMES"]),
        "q17": random.choice(["YES", "NO", "NOT_SURE"]),
        "q18": unknown_conn,
        "q19": random.choice(["YES", "NO", "SOMETIMES"]),
        "q20": random.choice(["YES", "NO", "NOT_SURE"]),
        "q21": random.choice(["YES", "NO", "NOT_SURE"]),
        "q22": tag_rev,
        "q23": random.choice(["YES", "NO", "SOMETIMES"]),
        "q24": p_vis,
        "q25": random.choice(["YES", "NO", "NOT_SURE"]),
        "q26": mfa,
        "q27": pwd_reuse,
        "q28": alerts,
        "q29": random.choice(["YES", "NO", "SOMETIMES"]),
        "q30": random.choice(["YES", "NO", "NOT_SURE"]),
        "q31": third_p,
        "q32": random.choice(["YES", "NO", "SOMETIMES"]),
        "q33": random.choice(["YES", "NO", "NOT_SURE"]),
        "q34": random.choice(["YES", "NO", "SOMETIMES"]),
        "q35": random.choice(["YES", "NO", "NOT_SURE"]),
        "q36": random.choice(["YES", "NO", "SOMETIMES"]),
        "q37": random.choice(["YES", "NO", "SOMETIMES"]),
        "q38": random.choice(["YES", "NO", "SOMETIMES"]),
        "q39": old_posts,
        "q40": random.choice(["YES", "NO", "NOT_SURE"]),
        "q41": random.choice(["YES", "NO", "SOMETIMES"]),
        "q42": random.choice(["YES", "NO", "SOMETIMES"])
    }

    # Run scoring engine
    cat_scores = calculate_category_scores(responses)
    risk_data = calculate_privacy_risk(cat_scores)
    score = risk_data["overall_score"]
    level = risk_data["risk_level"]

    profile_id = f"SYNTH-PRF-{1000 + idx}"

    row = {
        "profile_id": profile_id,
        "profile_visibility": p_vis,
        "phone_public": phone,
        "email_public": email,
        "birthday_public": bday,
        "location_public": loc_rt,
        "workplace_public": responses["q8"],
        "education_public": responses["q8"],
        "relationship_public": responses["q9"],
        "posts_public": responses["q14"],
        "location_tagging": responses["q12"],
        "travel_posts": travel,
        "unknown_connections": unknown_conn,
        "tag_review_enabled": tag_rev,
        "third_party_apps_reviewed": third_p,
        "mfa_enabled": mfa,
        "login_alerts_enabled": alerts,
        "password_reuse_reported": pwd_reuse,
        "suspicious_link_awareness": responses["q37"],
        "old_posts_reviewed": old_posts,
        "privacy_settings_reviewed": review_sett,
        "risk_score": score,
        "risk_level": level
    }

    return row, responses, cat_scores, risk_data


def generate_dataset(num_records: int = 1200, seed_db: bool = True):
    """Generates synthetic dataset and outputs to CSV and SQLite."""
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "social_media_privacy_assessments.csv")

    random.seed(42)  # Deterministic reproducible synthetic generation
    print(f"[*] Generating {num_records} synthetic privacy assessment records...")

    rows = []
    if seed_db:
        init_db()

    for i in range(num_records):
        row, responses, cat_scores, risk_data = generate_synthetic_record(i)
        rows.append(row)

        # Seed first 60 records into SQLite database for dashboard demo analytics
        if seed_db and i < 60:
            features = extract_privacy_features(responses)
            findings = generate_privacy_findings(responses)
            recs = generate_recommendations(findings)
            assessment_payload = {
                "assessment_id": f"ASM-SYNTH-{1000 + i}",
                "overall_score": risk_data["overall_score"],
                "risk_level": risk_data["risk_level"],
                "features": features,
                "responses": responses,
                "category_scores": cat_scores,
                "findings": findings,
                "recommendations": recs,
                "created_at": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
            }
            try:
                save_assessment(assessment_payload)
            except Exception:
                pass

    fieldnames = list(rows[0].keys())
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] Synthetic dataset generated successfully: {csv_path}")
    print(f"[+] Total records: {len(rows)}")
    tiers = {}
    for r in rows:
        tiers[r["risk_level"]] = tiers.get(r["risk_level"], 0) + 1
    print(f"[+] Risk Level Distribution: {tiers}")


if __name__ == "__main__":
    generate_dataset()
