# Social Media Privacy Risk Assessment Framework

[![Cybersecurity Defensive](https://img.shields.io/badge/Security-Defensive%20Posture-blue.svg)](https://github.com/)
[![Privacy by Design](https://img.shields.io/badge/Compliance-Privacy%20by%20Design-success.svg)](https://github.com/)
[![Zero PII Storage](https://img.shields.io/badge/GDPR-Article%2025%20%2F%2017-brightgreen.svg)](https://github.com/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-32%20Passed-emerald.svg)](https://github.com/)

> **Ethical & Defensive Disclaimer:**  
> This project is designed for defensive cybersecurity and privacy education. It uses synthetic or voluntarily provided assessment responses and does not scrape, track, or profile real social-media users.

---

## Overview
The **Social Media Privacy Risk Assessment Framework** is an industry-aligned cybersecurity application engineered to assess digital exposure, account configuration hygiene, social-engineering susceptibility, and historical footprint risk. 

Rather than executing invasive web scraping or collecting personal credentials—which presents severe ethical, legal, and privacy risks—this framework evaluates posture using a structured **42-question defensive survey** across **10 security categories**, a **deterministic Risk Scoring Engine (0–100)**, an interactive **Speculative Improvement Simulator**, an in-memory **EXIF Metadata Inspector & Stripper**, and a real-time **Cybersecurity Operations Dashboard** powered by **1,200 synthetic cohort profiles**.

---

## Problem Statement
Modern platforms encourage continuous sharing of identity anchors (birth dates, phone numbers, family links, employers) and real-time physical locations. Threat actors systematically weaponize Open Source Intelligence (OSINT) to orchestrate:
- **Spear-phishing & Pretexting:** Using employer details and personal context to craft high-conviction deceptive messages.
- **SIM-Swapping & ATO:** Exploiting exposed phone numbers and birth years to bypass SMS authentication and recovery questions.
- **Physical Burglary & Stalking:** Exploiting real-time check-ins and advance vacation announcements.
- **Third-Party API Token Abuse:** Stale OAuth authorizations providing persistent backdoor access to user data.

Conventional tools either invasively scrape profiles or offer generic, unquantified advice. This project provides a structured, quantitative, and privacy-preserving defensive framework.

---

## Objectives
1. **Defensive Posture:** Evaluate social media risks without scraping, account enumeration, or credential intercept.
2. **Comprehensive Coverage:** Audit 42 questions across 10 security domains.
3. **Quantitative Risk Engine:** Model exposure on a 0–100 scale (Higher score = Higher risk) mapped to 4 tiers: Low, Moderate, High, and Critical.
4. **Actionable Remediation:** Detect specific weaknesses and generate prioritized remediation steps (*Immediate*, *Important*, *Good Practice*).
5. **Speculative Simulation:** Enable users to simulate hardening actions and visualize instant risk reduction.
6. **Local Image Hygiene:** Inspect and strip EXIF GPS metadata 100% in-memory.
7. **Privacy by Design:** Enforce Data Minimization and verify via automated unit tests that zero sensitive PII is stored.

---

## Cybersecurity Relevance
This project directly reflects core capabilities utilized across cybersecurity roles:
- **Cybersecurity Analyst:** Threat modeling, attack surface discovery, configuration auditing.
- **Privacy Engineer:** Privacy by Design, GDPR Art. 25/17 compliance, data minimization.
- **Governance, Risk & Compliance (GRC) Analyst:** Quantitative risk scoring, control benchmarking.
- **Security Awareness Specialist:** Behavioral security coaching, phishing prevention training.

---

## Privacy vs Security

| Dimension | Account Security | Personal Privacy |
| :--- | :--- | :--- |
| **Core Objective** | Prevent unauthorized access & breach | Control what data is collected & exposed |
| **Key Controls** | MFA, Password Managers, Login Alerts | Hidden phone/email, private visibility, tag review |
| **Threat Neutralized** | Credential stuffing, brute force, session hijack | OSINT reconnaissance, stalking, identity theft |
| **Key Axiom** | *Strong Password $\neq$ Protected Identity* | *A secure account can still overshare* |

---

## Features
- **42-Question Assessment:** Categorized evaluation with contextual rationale and tips.
- **Deterministic Scoring Engine:** Mathematical normalization with configurable category weights.
- **Automated Findings Engine:** Pinpoints critical configuration flaws (e.g., public phone, absent MFA).
- **Prioritized Recommendations:** Actionable step-by-step guides grouped into Immediate, Important, and Good Practice.
- **Privacy Hardening Simulator:** Interactive toggles show instant before-and-after score deltas.
- **SecOps Analytics Dashboard:** KPI metrics, 10-axis Radar benchmark, Risk Tier Donut, Top Weaknesses bar chart.
- **Local EXIF Inspector & Stripper:** Audits GPS/camera tags and downloads sanitized PNG copies locally.
- **Audit Reports:** Exportable standalone HTML report and downloadable ReportLab PDF.
- **1,200-Record Synthetic Dataset:** Realistic personas generated via Python script.
- **32 Automated Unit Tests:** 100% test passing verifying scoring, boundaries, persistence, and zero-PII storage.

---

## Architecture

```
User Questionnaire (42 Questions)
          ↓
Input Validation & Feature Extraction (extract_privacy_features)
          ↓
10 Category Risk Analyzers (0–100 scale)
          ↓
Weighted Risk Scoring Engine (calculate_privacy_risk)
          ↓
Risk Classification (LOW, MODERATE, HIGH, CRITICAL)
    ├── Findings Engine (generate_privacy_findings)
    ├── Recommendation Engine (generate_recommendations)
    ├── Privacy Improvement Simulator (simulate_improvements)
    ├── SQLite Safe Storage (Zero raw PII)
    └── Printable Audit Reports (HTML & PDF)
```

---

## Technology Stack
- **Backend:** Python 3.13, Flask 3.1
- **Database:** SQLite 3 (Normalized relational schema, Privacy by Design)
- **PDF Generation:** ReportLab 4.5
- **Image Processing:** Pillow (PIL) 11.3 (In-memory EXIF parsing & stripping)
- **Frontend:** Semantic HTML5, CSS3 (Dark Cyber Slate theme), Vanilla JavaScript (ES6+)
- **Visualizations:** Chart.js (Radar, Donut, Bar charts)
- **Testing:** Python `unittest` (32 automated test cases)

---

## Risk Categories & Default Weights

| Category ID | Domain Name | Weight | Primary Threat Focus |
| :--- | :--- | :---: | :--- |
| `CAT_PROFILE` | **Profile Visibility** | 10% | External search engine indexing, friend list discoverability |
| `CAT_PERSONAL_INFO` | **Personal Information** | 15% | Public phone number, email, full birth date, workplace |
| `CAT_LOCATION` | **Location Privacy** | 15% | Real-time check-ins, advance vacation posts, camera geotags |
| `CAT_CONTENT` | **Posts & Content** | 10% | Default audience, work badges, computer screens, quizzes |
| `CAT_CONNECTIONS` | **Friends & Followers** | 10% | Unvetted friend requests, inactive contact pruning |
| `CAT_TAGGING` | **Tagging & Mentions** | 5% | Timeline tag review, third-party photo association |
| `CAT_AUTH_SECURITY`| **Authentication & Security** | 15% | Multi-Factor Authentication (MFA), password reuse, login alerts |
| `CAT_THIRD_PARTY` | **Third-Party Applications**| 5% | Stale OAuth tokens, overreaching app permissions |
| `CAT_SOCIAL_ENG` | **Social Engineering** | 10% | Direct message filters, suspicious giveaway links, fake urgency |
| `CAT_FOOTPRINT` | **Digital Footprint** | 5% | Retroactive post limits, dormant/abandoned accounts |

---

## Risk Scoring Model & Tiers
A higher score signifies greater vulnerability and attack-surface exposure:
- **0–20: LOW (Green):** Hardened posture. Restricted audience, TOTP MFA active, zero public contact data.
- **21–40: MODERATE (Blue):** Acceptable baseline. Minor secondary controls or non-essential trivia exposed.
- **41–70: HIGH (Amber):** Significant exposure. Search indexing on, public email, unvetted connections.
- **71–100: CRITICAL (Red):** Severe vulnerability. Public phone, live location broadcasting, missing MFA.

---

## Privacy by Design (GDPR Art. 25 & 17)
1. **Data Minimization:** No text inputs for actual phone numbers, email addresses, or passwords.
2. **Purpose Limitation:** Self-reported answers are used strictly for immediate risk calculation.
3. **Right to Erasure:** Assessments can be permanently wiped with one click (`DELETE /api/assessment/{id}`).
4. **Local Processing:** EXIF image metadata inspection runs 100% in-memory with zero cloud transmission.

---

## Installation & Local Execution

### Prerequisites
- Python 3.10 or higher installed and added to PATH.

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/Social-Media-Privacy-Risk-Assessment.git
cd Social-Media-Privacy-Risk-Assessment
```

### Step 2: Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Synthetic Dataset & Seed Database
```bash
python data/generate_dataset.py
```

### Step 5: Execute Automated Test Suite
```bash
python -m unittest tests/test_privacy_assessment.py
```

### Step 6: Start Application
```bash
python backend/app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

*(On Windows, you can also simply double-click `run.bat` to perform all steps automatically!)*

---

## REST API Documentation

| Endpoint | Method | Purpose |
| :--- | :---: | :--- |
| `/api/questions` | `GET` | Returns 42 questions, categories, and option weights |
| `/api/demo-profile` | `GET` | Returns high-exposure fictional demo profile for 1-click test |
| `/api/assessment` | `POST` | Submits answers, generates scores, findings, and persists record |
| `/api/assessment/{id}` | `GET` | Retrieves full assessment record by UUID |
| `/api/assessment/{id}` | `DELETE` | Permanently deletes assessment (Right to Erasure) |
| `/api/assessment/simulate-improvement` | `POST` | Evaluates speculative hardening toggles against baseline |
| `/api/dashboard/stats` | `GET` | Returns aggregate SecOps KPIs and chart distributions |
| `/api/assessment/{id}/report.html` | `GET` | View standalone printable HTML audit report |
| `/api/assessment/{id}/report.pdf` | `GET` | Download formal PDF audit report |
| `/api/metadata/inspect` | `POST` | In-memory EXIF GPS and camera tag inspection |
| `/api/metadata/strip` | `POST` | Strips all metadata and downloads sanitized image stream |

---

## Testing & Quality Assurance
The project includes 32 automated tests verifying:
- Boundary conditions (20.0 Low, 40.0 Moderate, 70.0 High, 70.1 Critical).
- Deterministic finding triggers (MFA missing, phone public).
- Score delta validity in the improvement simulator ($\Delta > 0$).
- Database schema inspection confirming absence of forbidden sensitive columns (`phone_number`, `password`).
- PDF and HTML report rendering integrity.

Execute the test suite at any time:
```bash
python -m unittest tests/test_privacy_assessment.py
```

---

## Screenshots Guide
See [`screenshots/README.md`](screenshots/README.md) for recommended captures:
1. `03_homepage_hero.png` — Dark cyber theme landing page.
2. `04_questionnaire_overview.png` — 42-question audit interface with 10-domain sidebar.
3. `10_results_score_hero.png` — Overall risk score and CRITICAL tier badge.
4. `12_results_radar_bar_charts.png` — Category risk radar and bar visualizers.
5. `17_simulator_score_delta.png` — Hardening simulator showing net reduction.
6. `18_dashboard_kpis.png` — SecOps privacy operations dashboard.
7. `22_audit_report_view.png` — Exportable HTML and PDF audit reports.
8. `24_automated_unit_tests.png` — 32 unit tests passing in terminal.

---

## Learning Outcomes & Career Proof

### Resume Bullet Points
- **Developed a defensive Cybersecurity Privacy Risk Assessment Framework** in Python/Flask analyzing 42 exposure controls across 10 domains with zero sensitive PII persistence.
- **Engineered an algorithmic Risk Scoring Engine and Simulator** projecting attack-surface reduction ($\Delta$ score reduction) and generating prioritized remediation roadmaps.
- **Synthesized a 1,200-profile behavioral dataset** and built an interactive SecOps analytics dashboard with Chart.js radar charts and GDPR Art. 25/17 compliance.

### LinkedIn Post Summary
> Excited to share my latest Cybersecurity project: the **Social Media Privacy Risk Assessment Framework**! 🛡️  
> Built as a defensive tool to evaluate digital exposure, oversharing, and account security hygiene without invasive web scraping. Features a 42-question audit model, mathematical risk engine (0–100), an interactive Hardening Simulator, an in-memory EXIF metadata inspector, and an aggregate SecOps dashboard backed by 1,200 synthetic profiles and 32 passing unit tests.  
> 🔗 GitHub: [https://github.com/your-username/Social-Media-Privacy-Risk-Assessment](https://github.com/)  
> #Cybersecurity #PrivacyByDesign #Python #SecOps #DefensiveSecurity #GRC #AppSec

---

## License
Distributed under the MIT License for educational and defensive security awareness.
