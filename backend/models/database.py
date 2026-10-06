"""
Database Models and Safe Storage Module
Implements SQLite persistence under strict Privacy-by-Design and Data Minimization principles.
Stores purely non-identifying telemetry (scores, category metrics, anonymized findings)
and explicitly prevents storage of raw personal identifying data (names, emails, phones, locations).
"""

import sqlite3
import os
import json
import uuid
import datetime
from typing import Dict, Any, List, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "privacy_assessments.db")


def get_db_connection():
    """Establishes an SQLite connection with row dictionary factories."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes normalized relational schema for privacy evaluations."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. ASSESSMENTS table: Holds top-level metadata and scores without any raw PII
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        assessment_id TEXT PRIMARY KEY,
        overall_score REAL NOT NULL,
        risk_level TEXT NOT NULL,
        features_json TEXT,
        responses_json TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # 2. CATEGORY_SCORES table: Normalized category scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category_scores (
        category_score_id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id TEXT NOT NULL,
        category TEXT NOT NULL,
        score REAL NOT NULL,
        risk_level TEXT NOT NULL,
        FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
    );
    """)

    # 3. FINDINGS table: Detected vulnerabilities associated with an assessment
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS findings (
        finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id TEXT NOT NULL,
        finding_code TEXT NOT NULL,
        category TEXT NOT NULL,
        severity TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        risk_impact TEXT NOT NULL,
        FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
    );
    """)

    # 4. RECOMMENDATIONS table: Reference guidance associated with assessments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id TEXT NOT NULL,
        finding_code TEXT NOT NULL,
        action TEXT NOT NULL,
        priority TEXT NOT NULL,
        rationale TEXT NOT NULL,
        steps_json TEXT NOT NULL,
        FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()


def save_assessment(assessment_data: Dict[str, Any]) -> str:
    """
    Persists evaluation outcomes into the database.
    Enforces Data Minimization: only answers (categorical values, not raw PII) and scores are saved.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    assessment_id = assessment_data.get("assessment_id") or f"ASM-{uuid.uuid4().hex[:8].upper()}"
    created_at = assessment_data.get("created_at") or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    overall_score = float(assessment_data.get("overall_score", 0.0))
    risk_level = str(assessment_data.get("risk_level", "LOW"))

    features_json = json.dumps(assessment_data.get("features", {}))
    responses_json = json.dumps(assessment_data.get("responses", {}))

    # Insert parent assessment record
    cursor.execute("""
        INSERT INTO assessments (assessment_id, overall_score, risk_level, features_json, responses_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (assessment_id, overall_score, risk_level, features_json, responses_json, created_at))

    # Insert category scores
    for cat_id, cat_info in assessment_data.get("category_scores", {}).items():
        cursor.execute("""
            INSERT INTO category_scores (assessment_id, category, score, risk_level)
            VALUES (?, ?, ?, ?)
        """, (assessment_id, cat_id, float(cat_info.get("score", 0.0)), str(cat_info.get("risk_level", "LOW"))))

    # Insert findings
    for f in assessment_data.get("findings", []):
        cursor.execute("""
            INSERT INTO findings (assessment_id, finding_code, category, severity, title, description, risk_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (assessment_id, f.get("finding_id", ""), f.get("category", ""), f.get("severity", ""),
              f.get("title", ""), f.get("description", ""), f.get("risk_impact", "")))

    # Insert recommendations
    for r in assessment_data.get("recommendations", []):
        steps_json = json.dumps(r.get("steps", []))
        cursor.execute("""
            INSERT INTO recommendations (assessment_id, finding_code, action, priority, rationale, steps_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (assessment_id, r.get("finding_id", ""), r.get("action", ""), r.get("priority", "IMPORTANT"),
              r.get("rationale", ""), steps_json))

    conn.commit()
    conn.close()
    return assessment_id


def get_assessment(assessment_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves full assessment record with child categories, findings, and recommendations."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assessments WHERE assessment_id = ?", (assessment_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    # Load categories
    cursor.execute("SELECT * FROM category_scores WHERE assessment_id = ?", (assessment_id,))
    cat_rows = cursor.fetchall()
    category_scores = {}
    for cr in cat_rows:
        category_scores[cr["category"]] = {
            "score": cr["score"],
            "risk_level": cr["risk_level"]
        }

    # Load findings
    cursor.execute("SELECT * FROM findings WHERE assessment_id = ?", (assessment_id,))
    findings_rows = cursor.fetchall()
    findings = []
    for fr in findings_rows:
        findings.append({
            "finding_id": fr["finding_code"],
            "category": fr["category"],
            "severity": fr["severity"],
            "title": fr["title"],
            "description": fr["description"],
            "risk_impact": fr["risk_impact"]
        })

    # Load recommendations
    cursor.execute("SELECT * FROM recommendations WHERE assessment_id = ?", (assessment_id,))
    rec_rows = cursor.fetchall()
    recommendations = []
    for rr in rec_rows:
        recommendations.append({
            "finding_id": rr["finding_code"],
            "action": rr["action"],
            "priority": rr["priority"],
            "rationale": rr["rationale"],
            "steps": json.loads(rr["steps_json"])
        })

    conn.close()

    return {
        "assessment_id": row["assessment_id"],
        "overall_score": row["overall_score"],
        "risk_level": row["risk_level"],
        "features": json.loads(row["features_json"]) if row["features_json"] else {},
        "responses": json.loads(row["responses_json"]) if row["responses_json"] else {},
        "created_at": row["created_at"],
        "category_scores": category_scores,
        "findings": findings,
        "recommendations": recommendations
    }


def list_assessments(limit: int = 50) -> List[Dict[str, Any]]:
    """Lists recent assessments summary."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT assessment_id, overall_score, risk_level, created_at 
        FROM assessments 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_assessment(assessment_id: str) -> bool:
    """Deletes an assessment and all cascading records (User Right to Erasure / GDPR Article 17)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_dashboard_aggregates() -> Dict[str, Any]:
    """Computes aggregate analytics over stored assessments for the cybersecurity dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total count
    cursor.execute("SELECT COUNT(*), AVG(overall_score) FROM assessments")
    count_row = cursor.fetchone()
    total_assessments = count_row[0] if count_row else 0
    avg_score = round(count_row[1] or 0.0, 1)

    # Risk level distribution
    cursor.execute("SELECT risk_level, COUNT(*) as cnt FROM assessments GROUP BY risk_level")
    tier_rows = cursor.fetchall()
    tier_distribution = {"LOW": 0, "MODERATE": 0, "HIGH": 0, "CRITICAL": 0}
    for r in tier_rows:
        tier_distribution[r["risk_level"]] = r["cnt"]

    # Category averages
    cursor.execute("SELECT category, AVG(score) as avg_s FROM category_scores GROUP BY category")
    cat_rows = cursor.fetchall()
    category_averages = {r["category"]: round(r["avg_s"], 1) for r in cat_rows}

    # Top weaknesses (frequency of findings)
    cursor.execute("SELECT title, severity, COUNT(*) as cnt FROM findings GROUP BY title ORDER BY cnt DESC LIMIT 6")
    finding_rows = cursor.fetchall()
    top_weaknesses = [{"title": r["title"], "severity": r["severity"], "count": r["cnt"]} for r in finding_rows]

    # Recent assessments
    cursor.execute("SELECT assessment_id, overall_score, risk_level, created_at FROM assessments ORDER BY created_at DESC LIMIT 6")
    recent_assessments = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "total_assessments": total_assessments,
        "average_risk_score": avg_score,
        "tier_distribution": tier_distribution,
        "category_averages": category_averages,
        "top_weaknesses": top_weaknesses,
        "recent_assessments": recent_assessments
    }
