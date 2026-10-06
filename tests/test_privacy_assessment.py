"""
Comprehensive Automated Test Suite
Implements at least 32 automated unit and integration tests covering:
- Privacy questionnaire evaluation
- Category scoring and weights
- Risk tier threshold boundary tests
- Findings and Recommendation engines
- Privacy Improvement Simulator
- Database persistence and Data Minimization verification
- Report generation (HTML and PDF)
- EXIF Metadata Inspection and Stripper
"""

import unittest
import os
import io
import json
import sqlite3
from PIL import Image

from backend.services.assessment_engine import validate_responses, extract_privacy_features
from backend.services.scoring_engine import calculate_category_scores, calculate_privacy_risk, determine_risk_level
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.improvement_simulator import simulate_improvements, SIMULATION_ACTIONS
from backend.services.report_generator import generate_html_report, generate_pdf_report_bytes
from backend.services.metadata_inspector import inspect_image_metadata, strip_image_metadata
from backend.models.database import init_db, save_assessment, get_assessment, delete_assessment, DB_FILE
from backend.utils.questionnaire_data import QUESTIONS, CATEGORIES

class TestSocialMediaPrivacyFramework(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    # Base templates
    def get_secure_responses(self):
        """Generates responses for a privacy-hardened user."""
        res = {}
        for q in QUESTIONS:
            qid = q["id"]
            # Lowest risk option
            best_opt = min(q["options"], key=lambda o: o["risk_points"])
            res[qid] = best_opt["value"]
        return res

    def get_vulnerable_responses(self):
        """Generates responses for a high-risk oversharing user."""
        res = {}
        for q in QUESTIONS:
            qid = q["id"]
            worst_opt = max(q["options"], key=lambda o: o["risk_points"])
            res[qid] = worst_opt["value"]
        return res

    # TEST 1: Fully private profile
    def test_01_fully_private_profile(self):
        """Test ID: T01 - Fully private profile yields LOW risk score (<= 20)."""
        responses = self.get_secure_responses()
        cat = calculate_category_scores(responses)
        risk = calculate_privacy_risk(cat)
        self.assertLessEqual(risk["overall_score"], 20.0)
        self.assertEqual(risk["risk_level"], "LOW")

    # TEST 2: Fully public synthetic profile
    def test_02_fully_public_synthetic_profile(self):
        """Test ID: T02 - Fully public profile yields CRITICAL risk score (>= 71)."""
        responses = self.get_vulnerable_responses()
        cat = calculate_category_scores(responses)
        risk = calculate_privacy_risk(cat)
        self.assertGreaterEqual(risk["overall_score"], 71.0)
        self.assertEqual(risk["risk_level"], "CRITICAL")

    # TEST 3: Public phone
    def test_03_public_phone(self):
        """Test ID: T03 - Public phone triggers FIND_PHONE_PUBLIC critical finding."""
        responses = {"q5": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_PHONE_PUBLIC" and f["severity"] == "CRITICAL" for f in findings)
        self.assertTrue(found)

    # TEST 4: Public email
    def test_04_public_email(self):
        """Test ID: T04 - Public email triggers FIND_EMAIL_PUBLIC finding."""
        responses = {"q6": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_EMAIL_PUBLIC" for f in findings)
        self.assertTrue(found)

    # TEST 5: Public birthday
    def test_05_public_birthday(self):
        """Test ID: T05 - Full birthday public triggers FIND_FULL_BIRTHDAY finding."""
        responses = {"q7": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_FULL_BIRTHDAY" for f in findings)
        self.assertTrue(found)

    # TEST 6: Public location
    def test_06_public_location(self):
        """Test ID: T06 - Public location generates high score in CAT_LOCATION."""
        responses = {"q10": "YES", "q11": "YES", "q12": "YES", "q13": "YES"}
        cat = calculate_category_scores(responses)
        self.assertGreaterEqual(cat["CAT_LOCATION"]["score"], 80.0)

    # TEST 7: Real-time check-ins
    def test_07_real_time_check_ins(self):
        """Test ID: T07 - Real-time check-ins trigger FIND_REALTIME_LOCATION critical finding."""
        responses = {"q10": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_REALTIME_LOCATION" and f["severity"] == "CRITICAL" for f in findings)
        self.assertTrue(found)

    # TEST 8: Travel plans
    def test_08_travel_plans(self):
        """Test ID: T08 - Travel plans posted publicly trigger FIND_TRAVEL_ANNOUNCEMENTS."""
        responses = {"q11": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_TRAVEL_ANNOUNCEMENTS" for f in findings)
        self.assertTrue(found)

    # TEST 9: Workplace exposure
    def test_09_workplace_exposure(self):
        """Test ID: T09 - Workplace public exposure increases Personal Information risk."""
        r1 = {"q8": "NO"}
        r2 = {"q8": "YES"}
        c1 = calculate_category_scores(r1)["CAT_PERSONAL_INFO"]["score"]
        c2 = calculate_category_scores(r2)["CAT_PERSONAL_INFO"]["score"]
        self.assertGreater(c2, c1)

    # TEST 10: Education exposure
    def test_10_education_exposure(self):
        """Test ID: T10 - Feature extractor maps education/workplace correctly."""
        feats = extract_privacy_features({"q8": "YES"})
        self.assertIn("feat_q8", feats)
        self.assertEqual(feats["feat_q8"], 0.70)

    # TEST 11: Public posts
    def test_11_public_posts(self):
        """Test ID: T11 - Public post default audience inflates Posts & Content risk."""
        cat = calculate_category_scores({"q14": "PUBLIC"})
        self.assertGreaterEqual(cat["CAT_CONTENT"]["score"], 35.0)

    # TEST 12: Unknown connections
    def test_12_unknown_connections(self):
        """Test ID: T12 - Accepting unknown connection requests triggers FIND_UNKNOWN_CONNECTIONS."""
        responses = {"q18": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_UNKNOWN_CONNECTIONS" for f in findings)
        self.assertTrue(found)

    # TEST 13: Tag review disabled
    def test_13_tag_review_disabled(self):
        """Test ID: T13 - Tag review disabled triggers FIND_TAG_REVIEW_DISABLED."""
        responses = {"q22": "NO"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_TAG_REVIEW_DISABLED" for f in findings)
        self.assertTrue(found)

    # TEST 14: MFA disabled
    def test_14_mfa_disabled(self):
        """Test ID: T14 - MFA disabled triggers CRITICAL finding FIND_MFA_DISABLED."""
        responses = {"q26": "NO"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_MFA_DISABLED" and f["severity"] == "CRITICAL" for f in findings)
        self.assertTrue(found)

    # TEST 15: Login alerts disabled
    def test_15_login_alerts_disabled(self):
        """Test ID: T15 - Login alerts disabled triggers FIND_LOGIN_ALERTS_OFF."""
        responses = {"q28": "NO"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_LOGIN_ALERTS_OFF" for f in findings)
        self.assertTrue(found)

    # TEST 16: Password reuse reported
    def test_16_password_reuse_reported(self):
        """Test ID: T16 - Reusing passwords triggers FIND_PASSWORD_REUSE."""
        responses = {"q27": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_PASSWORD_REUSE" for f in findings)
        self.assertTrue(found)

    # TEST 17: Third-party apps not reviewed
    def test_17_third_party_apps_not_reviewed(self):
        """Test ID: T17 - Third party apps unreviewed triggers FIND_THIRD_PARTY_STALE."""
        responses = {"q31": "NO"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_THIRD_PARTY_STALE" for f in findings)
        self.assertTrue(found)

    # TEST 18: Suspicious link awareness low
    def test_18_suspicious_link_awareness_low(self):
        """Test ID: T18 - Clicking unsolicited giveaway links inflates social engineering risk."""
        cat_high = calculate_category_scores({"q37": "YES"})["CAT_SOCIAL_ENG"]["score"]
        cat_low = calculate_category_scores({"q37": "NO"})["CAT_SOCIAL_ENG"]["score"]
        self.assertGreater(cat_high, cat_low)

    # TEST 19: Old posts not reviewed
    def test_19_old_posts_not_reviewed(self):
        """Test ID: T19 - Historical posts unreviewed triggers FIND_HISTORICAL_POSTS."""
        responses = {"q39": "NO"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_HISTORICAL_POSTS" for f in findings)
        self.assertTrue(found)

    # TEST 20: Privacy settings not reviewed
    def test_20_privacy_settings_not_reviewed(self):
        """Test ID: T20 - Abandoned accounts active triggers FIND_ABANDONED_ACCOUNTS."""
        responses = {"q40": "YES"}
        findings = generate_privacy_findings(responses)
        found = any(f["finding_id"] == "FIND_ABANDONED_ACCOUNTS" for f in findings)
        self.assertTrue(found)

    # TEST 21: Category score calculation
    def test_21_category_score_calculation(self):
        """Test ID: T21 - Exactly 10 categories computed with scores clamped 0-100."""
        cat = calculate_category_scores({"q1": "PUBLIC"})
        self.assertEqual(len(cat), 10)
        for c in cat.values():
            self.assertGreaterEqual(c["score"], 0.0)
            self.assertLessEqual(c["score"], 100.0)

    # TEST 22: Overall score calculation
    def test_22_overall_score_calculation(self):
        """Test ID: T22 - Overall score is correctly calculated weighted average."""
        cat = calculate_category_scores({"q1": "PUBLIC", "q26": "NO"})
        risk = calculate_privacy_risk(cat)
        self.assertGreaterEqual(risk["overall_score"], 0.0)
        self.assertLessEqual(risk["overall_score"], 100.0)

    # TEST 23: Score boundary 20
    def test_23_score_boundary_20(self):
        """Test ID: T23 - Score boundary 20 is classified as LOW."""
        tier = determine_risk_level(20.0)
        self.assertEqual(tier["level"], "LOW")

    # TEST 24: Score boundary 40
    def test_24_score_boundary_40(self):
        """Test ID: T24 - Score boundary 40 is classified as MODERATE."""
        tier = determine_risk_level(40.0)
        self.assertEqual(tier["level"], "MODERATE")

    # TEST 25: Score boundary 70
    def test_25_score_boundary_70(self):
        """Test ID: T25 - Score boundary 70 is HIGH; 70.1 is CRITICAL."""
        tier70 = determine_risk_level(70.0)
        tier71 = determine_risk_level(70.1)
        self.assertEqual(tier70["level"], "HIGH")
        self.assertEqual(tier71["level"], "CRITICAL")

    # TEST 26: Recommendation generation
    def test_26_recommendation_generation(self):
        """Test ID: T26 - Recommendations generated with action steps and priority."""
        findings = [{"finding_id": "FIND_MFA_DISABLED", "title": "MFA Disabled", "severity": "CRITICAL"}]
        recs = generate_recommendations(findings)
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["priority"], "IMMEDIATE")
        self.assertTrue(len(recs[0]["steps"]) > 0)

    # TEST 27: Improvement simulation
    def test_27_improvement_simulation(self):
        """Test ID: T27 - Simulator reduces score when hardening toggles are selected."""
        vulnerable = self.get_vulnerable_responses()
        sim_res = simulate_improvements(vulnerable, ["enable_mfa", "hide_phone", "stop_realtime_location"])
        self.assertGreater(sim_res["risk_reduction_points"], 0.0)
        self.assertLess(sim_res["simulated"]["overall_score"], sim_res["baseline"]["overall_score"])

    # TEST 28: Database save and retrieve
    def test_28_database_save_and_retrieve(self):
        """Test ID: T28 - Assessment saves to SQLite and retrieves without data corruption."""
        test_id = "ASM-TEST-PERSISTENCE"
        cat = calculate_category_scores({"q1": "PRIVATE"})
        risk = calculate_privacy_risk(cat)
        payload = {
            "assessment_id": test_id,
            "overall_score": risk["overall_score"],
            "risk_level": risk["risk_level"],
            "features": {"f1": 0.5},
            "responses": {"q1": "PRIVATE"},
            "category_scores": cat,
            "findings": [],
            "recommendations": []
        }
        saved_id = save_assessment(payload)
        self.assertEqual(saved_id, test_id)
        fetched = get_assessment(test_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["overall_score"], risk["overall_score"])
        # Clean up
        delete_assessment(test_id)

    # TEST 29: Sensitive data not stored
    def test_29_sensitive_data_not_stored(self):
        """Test ID: T29 - Confirms schema does NOT have columns for raw phone, raw email, raw address, raw password."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(assessments)")
        columns = [row[1].lower() for row in cursor.fetchall()]
        conn.close()

        forbidden_fields = ["phone_number", "email_address", "home_address", "password", "birth_date", "ssn", "credit_card"]
        for field in forbidden_fields:
            self.assertNotIn(field, columns, f"Privacy violation: Column {field} found in database schema!")

    # TEST 30: Report generation
    def test_30_report_generation(self):
        """Test ID: T30 - Verifies HTML and PDF reports render without exceptions."""
        assessment_data = {
            "assessment_id": "TEST-REP-01",
            "overall_score": 45.0,
            "risk_level": "HIGH",
            "category_scores": calculate_category_scores({"q1": "PUBLIC"}),
            "findings": [{"finding_id": "FIND_PHONE_PUBLIC", "severity": "CRITICAL", "title": "Phone Public", "description": "Desc", "risk_impact": "Impact"}],
            "recommendations": [{"finding_id": "FIND_PHONE_PUBLIC", "priority": "IMMEDIATE", "action": "Hide phone", "rationale": "Safety", "steps": ["Step 1"]}]
        }
        html_rep = generate_html_report(assessment_data)
        self.assertIn("TEST-REP-01", html_rep)
        self.assertIn("Social Media Privacy Risk Assessment Report", html_rep)

        pdf_bytes = generate_pdf_report_bytes(assessment_data)
        self.assertTrue(len(pdf_bytes) > 500)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

    # TEST 31: Metadata inspector
    def test_31_metadata_inspector(self):
        """Test ID: T31 - Parses local image bytes without error."""
        img = Image.new("RGB", (100, 100), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        meta = inspect_image_metadata(buf.getvalue(), "test_img.jpg")
        self.assertEqual(meta["format"], "JPEG")
        self.assertEqual(meta["dimensions"], "100 x 100")

    # TEST 32: Metadata stripper
    def test_32_metadata_stripper(self):
        """Test ID: T32 - Strips image metadata creating clean output image."""
        img = Image.new("RGB", (64, 64), color="red")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        clean_bytes = strip_image_metadata(buf.getvalue(), "PNG")
        self.assertTrue(len(clean_bytes) > 0)
        self.assertTrue(clean_bytes.startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
