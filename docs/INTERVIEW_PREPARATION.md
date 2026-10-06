# Cybersecurity Interview Preparation & Technical Defense Guide

This document contains 10 predicted technical interview questions and comprehensive, authentic answers demonstrating deep understanding of defensive cybersecurity, privacy engineering, risk modeling, and full-stack implementation.

---

### Question 1: "Explain your project."
**Candidate Answer:**  
"My project is titled the **Social Media Privacy Risk Assessment Framework**. It is an industry-oriented, defensive cybersecurity application designed to evaluate an individual's digital exposure footprint, account-security posture, and social-engineering vulnerability across social platforms. 

Instead of performing invasive web scraping or collecting personal credentials—which poses ethical and compliance concerns—my framework uses a structured 42-question self-reported privacy survey spanning 10 distinct security categories: Profile Visibility, Personal Information, Location Privacy, Posts and Content, Connection Hygiene, Tagging Controls, Authentication Security, Third-Party App Permissions, Social Engineering Awareness, and Historical Digital Footprint.

The backend extracts normalized numerical features, executes a weighted category scoring engine, classifies overall risk on a 0 to 100 scale into four tiers—Low, Moderate, High, and Critical—and pinpoints critical vulnerabilities such as missing MFA or public phone numbers. It delivers prioritized actionable remediation steps, an interactive *Privacy Improvement Simulator* that visualizes mathematical risk reduction when controls are hardened, a safe local EXIF metadata viewer/stripper, and exportable audit reports in HTML and PDF formats. I also created a synthetic dataset of 1,200 behavioral profiles to power aggregate SecOps telemetry in an interactive dashboard."

---

### Question 2: "What is the fundamental difference between Privacy and Security in the context of your framework?"
**Candidate Answer:**  
"In cybersecurity, **Security** is about *confidentiality, integrity, and availability*—protecting systems, sessions, and data against unauthorized access. For example, using a 20-character randomly generated password and hardware MFA creates a very secure account.

However, **Privacy** controls *what information is authorized to be shared, collected, or exposed to the world*. An account can have immaculate account security with zero risk of brute-force compromise, but if the user posts their boarding pass with an unblurred barcode, announces upcoming vacation dates, and has their personal phone number publicly displayed in their bio, their privacy exposure is severe.

Therefore, *Strong Security does not imply Strong Privacy*. My framework explicitly isolates these concepts: Category G assesses Authentication and Account Security, while Categories A through F assess Information Exposure and Privacy."

---

### Question 3: "How does oversharing personal information increase social engineering and phishing risk?"
**Candidate Answer:**  
"Social engineering attacks—specifically spear-phishing and business email compromise (BEC)—rely heavily on Open Source Intelligence (OSINT) gathering to establish pretext and build rapport. 

When a user publicly reveals seemingly harmless data—such as their workplace, university graduation year, pet's name, or vacation plans—threat actors exploit that context. For example, knowing a user's employer allows an attacker to craft a convincing HR or IT-support pretext email. Mentioning family members or birthdays enables credential recovery attacks by guessing common security question answers. In my framework, Category I assesses Social Engineering vulnerability, directly correlating exposed identity anchors with phishing susceptibility."

---

### Question 4: "Explain the mathematics behind your Privacy Risk Scoring Engine."
**Candidate Answer:**  
"In our scoring model, a **higher score represents higher exposure and risk** (0 = Hardened, 100 = Critical). 

Each question has options mapped to specific risk points based on empirical risk contribution (e.g., Public Profile = 100 points, Friends Only = 25, Private = 0; MFA Disabled = 100, SMS MFA = 30, TOTP App = 0).

First, the engine calculates the arithmetic mean of points within each of the 10 categories to generate isolated 0–100 category scores:
$$S_{cat} = \frac{1}{N_{cat}} \sum_{i=1}^{N_{cat}} \text{RiskPoints}_i$$

Second, the overall risk score is calculated as a normalized weighted sum across all 10 categories:
$$S_{overall} = \sum_{c=1}^{10} S_{cat, c} \times W_c$$

Default weights reflect threat severity: Location Privacy (15%), Personal Information (15%), and Account Security (15%) are weighted highest because direct exploitation leads to immediate physical stalking, identity theft, or account takeover. The overall score is then mapped to deterministic risk tiers: Low (0–20), Moderate (21–40), High (41–70), and Critical (71–100)."

---

### Question 5: "How does your project implement the principle of Data Minimization?"
**Candidate Answer:**  
"Under GDPR Article 5(1)(c), data controllers must collect only data that is adequate, relevant, and strictly limited to what is necessary.

My application implements Data Minimization by design:
1. **No Sensitive Input:** The questionnaire never asks users for their real phone number, actual date of birth, home address, or password. It asks only categorical indicator questions: *'Is your phone number publicly visible? YES / NO'*.
2. **Database Schema Design:** In our SQLite database (`assessments` table), we store only randomized `assessment_id`, normalized categorical choices, mathematical scores, and timestamps.
3. **Automated Verification:** I wrote unit test `test_29_sensitive_data_not_stored` in our automated test suite that queries SQLite `PRAGMA table_info` and asserts that no columns exist for raw identifiers like phone, email, SSN, or passwords."

---

### Question 6: "Why is SMS-based Multi-Factor Authentication scored as moderate risk compared to TOTP Authenticator apps?"
**Candidate Answer:**  
"While SMS MFA is vastly superior to having no MFA at all, it possesses well-documented architectural vulnerabilities. 

SMS relies on legacy telecommunications infrastructure (SS7 protocol) that lacks end-to-end encryption. Threat actors frequently bypass SMS 2FA via **SIM swapping**, where an attacker uses social engineering against telecom customer support to port the victim's phone number to a rogue SIM card, or via **SMS interception**. 

In contrast, Time-based One-Time Passwords (TOTP via RFC 6238) generate cryptographically salted tokens locally on the device with a 30-second epoch and never traverse the cellular carrier network. In our scoring engine, MFA disabled earns 100 risk points, SMS earns 30 points, and Authenticator App/Hardware Key earns 0 points."

---

### Question 7: "What threat vectors do third-party applications introduce, and how does your tool assess them?"
**Candidate Answer:**  
"Third-party applications connect via OAuth 2.0 grants or 'Sign in with Social Account' tokens. Over time, users authorize dozens of apps, quizzes, and productivity widgets.

The risks include:
1. **Stale Permissions & Token Hijacking:** Even if the user stops using the service, the application's OAuth token remains valid until explicitly revoked. If that developer's database suffers a breach, an attacker gains API access to the user's social profile.
2. **Scope Creep:** Quizzes often request overreaching scopes, such as permission to read contact lists or post status updates on the user's behalf.

Our Category H evaluates whether users perform quarterly permission audits and revoke unused third-party tokens, adhering to the Principle of Least Privilege."

---

### Question 8: "Explain how your Privacy Improvement Simulator works technically."
**Candidate Answer:**  
"The simulator operates on speculative state overwriting. When a user submits an assessment or loads our high-risk demo profile, the baseline questionnaire dictionary is maintained in state.

The user can toggle 14 independent hardening actions—such as *'Enable MFA'*, *'Hide Phone Number'*, or *'Cease Real-Time Location'*. Each toggle maps to specific question response overrides (e.g., `enable_mfa` sets `q26 = "YES"`). 

When actions are toggled, the simulator clones the baseline response dictionary, applies the selected overwrites, feeds the mutated dictionary back through `calculate_category_scores()` and `calculate_privacy_risk()`, and computes the score delta:
$$\Delta = S_{baseline} - S_{simulated}$$

This immediately updates the KPI cards and renders a dual-dataset comparative Chart.js bar chart showing the precise attack-surface reduction achieved across all categories."

---

### Question 9: "How does your local EXIF metadata tool work without compromising privacy?"
**Candidate Answer:**  
"Modern smartphone cameras write EXIF (Exchangeable Image File Format) headers directly into JPEG and TIFF images, including GPS IFD tags (tag ID `34853`) with latitude, longitude, and altitude rational tuples.

To audit this safely, my `metadata_inspector.py` service operates 100% in-memory using Python's Pillow library. The image stream is parsed locally: it converts EXIF degree/minute/second tuples into decimal coordinates, detects camera hardware models and timestamps, and returns privacy warnings.

For sanitization, `strip_image_metadata()` creates a clean in-memory canvas of the image's raw pixel buffer (`image.getdata()`) and saves it as a new PNG/JPEG stream without copying over the EXIF dictionary header. At no point is the photo sent to an external API or stored permanently on disk."

---

### Question 10: "How did you test this application to ensure reliability and defensive integrity?"
**Candidate Answer:**  
"I implemented a comprehensive automated test suite in `tests/test_privacy_assessment.py` containing **32 distinct unit and integration tests** executed via Python's `unittest` framework:

1. **Boundary & Tier Tests:** Tested score thresholds at boundaries 20 (Low), 40 (Moderate), 70 (High), and 70.1 (Critical).
2. **Extreme Case Profiles:** Validated that a fully private profile produces score $\le 20$ (Low) and a fully public profile produces $\ge 71$ (Critical).
3. **Specific Finding Triggers:** Tested that individual misconfigurations (e.g., `q5 = "YES"` for phone, `q26 = "NO"` for MFA) deterministically generate corresponding high/critical findings and recommendations.
4. **Data Minimization Integrity:** Queried SQLite schema via `PRAGMA table_info` to assert absence of forbidden sensitive columns.
5. **Report & EXIF Generation:** Tested that HTML report templates and ReportLab PDF document flows compile valid binary streams without memory faults.

All 32 tests pass in 0.4 seconds, validating both defensive logic and architectural stability."
