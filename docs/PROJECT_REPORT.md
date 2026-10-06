# Social Media Privacy Risk Assessment Framework
## Final Technical Project Report & Industry Documentation

---

### Abstract
Social media platforms serve as vital conduits for global connection, yet pervasive data collection and user oversharing create severe cybersecurity exposures, including identity theft, account takeover, SIM-swapping, physical stalking, and spear-phishing. Existing security solutions predominantly focus on perimeter network defense or post-breach intrusion monitoring, frequently overlooking pre-compromise behavioral exposure and configuration misconfigurations. 

This project presents the **Social Media Privacy Risk Assessment Framework**, an industry-aligned defensive platform designed to evaluate social platform posture without invasive account scraping or sensitive credential acquisition. The framework implements a 42-question self-reported audit model covering 10 critical privacy categories. It extracts normalized numerical vectors, computes weighted category risk indexes (0–100), classifies net exposure across four risk tiers (Low, Moderate, High, Critical), pinpoints specific vulnerabilities, and generates prioritized remediation roadmaps. Incorporating an interactive *Privacy Improvement Simulator*, an in-memory *EXIF Metadata Inspector & Stripper*, a 1,200-record synthetic cohort dataset, and exportable PDF/HTML audit reports, this framework delivers an end-to-end, Privacy-by-Design educational solution for students, hiring teams, and enterprise digital-risk management programs.

---

### 1. Introduction & Background
As digital interactions have centralized onto platforms like Instagram, LinkedIn, Facebook, and X, users routinely broadcast identity tokens, real-time whereabouts, and personal networks. Simultaneously, threat actors leverage Open Source Intelligence (OSINT) tools to aggregate distributed digital breadcrumbs into actionable exploitation profiles.

#### 1.1 Digital Footprints: Active vs. Passive
- **Active Digital Footprint:** The intentional data deliberately released by an individual (status updates, venue check-ins, tagged photographs, bio descriptions, and survey responses).
- **Passive Digital Footprint:** Involuntary telemetry harvested by services during platform engagement (IP addresses, device hardware identifiers, browser canvas hashes, and telemetry logs).
This framework evaluates an individual's active footprint and platform configuration posture to raise actionable awareness.

#### 1.2 Privacy vs. Account Security
A cornerstone conceptual distinction emphasized in this project is:
$$\text{Account Security} \neq \text{Information Privacy}$$
- **Security** enforces authentication barriers (cryptographic passphrases, FIDO2/TOTP multi-factor authentication, session token invalidation).
- **Privacy** dictates data access boundaries (who is authorized to view, correlate, or index shared attributes).
An account secured with a 24-character random password but displaying a public phone number and unblurred workplace security badge remains critically vulnerable to social engineering and physical threats.

---

### 2. Problem Statement & Objectives
Conventional approaches to personal cybersecurity either:
1. Require intrusive invasive scraping of third-party platforms, introducing ethical, legal, and Terms-of-Service violations.
2. Involve credential interception that violates data minimization standards.
3. Provide generic, high-level advice that fails to quantify risk or offer measurable remediation paths.

#### Project Objectives:
1. Engineer a purely **defensive, non-invasive risk assessment platform** requiring zero external scraping.
2. Design a **42-question questionnaire** spanning 10 holistic exposure categories.
3. Develop an **algorithmic Risk Scoring Engine** where higher scores represent higher exposure (0–100) mapped to four deterministic tiers.
4. Build a **Findings Engine** that identifies specific critical misconfigurations and a **Recommendation Engine** that groups actions by priority (*Immediate*, *Important*, *Good Practice*).
5. Deliver a **Speculative Privacy Hardening Simulator** showing instant mathematical risk reduction when configurations are tightened.
6. Provide a **Local EXIF Metadata Tool** that inspects GPS and camera tags in-memory without network transmission.
7. Generate a **1,200-profile synthetic dataset** and seed an SQLite database to power a live SecOps dashboard.
8. Enforce **Privacy by Design (GDPR Art. 25/17)** and write 30+ automated tests verifying zero PII leakage.

---

### 3. System Architecture & Workflow Pipeline

```
                               ┌─────────────────────────────────┐
                               │           User Client           │
                               └────────────────┬────────────────┘
                                                │
                                    1. 42-Question Survey
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │ Input Validation & Sanitization │
                               └────────────────┬────────────────┘
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │ Privacy Feature Vectorizer      │
                               │   (extract_privacy_features)    │
                               └────────────────┬────────────────┘
                                                │
                                                ▼
                ┌───────────────────────────────────────────────────────────────┐
                │             10 Modular Category Risk Analyzers                │
                │  Profile | Personal Info | Location | Content | Connections   │
                │  Tagging | Auth Security | Third-Party | Social Eng | Footprint │
                └───────────────────────────────┬───────────────────────────────┘
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │ Weighted Risk Scoring Engine    │
                               │   (calculate_privacy_risk)      │
                               └────────────────┬────────────────┘
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │ Overall Risk Score & Tier       │
                               │   (0–20 LOW, 21–40 MOD, etc.)   │
                               └───────┬─────────────────┬───────┘
                                       │                 │
                         ┌─────────────┴──┐           ┌──┴─────────────┐
                         ▼                ▼           ▼                ▼
                 Findings Engine    Rec. Engine   Report Gen.   Improvement Sim.
                         │                │           │                │
                         └─────────────┬──┘           └──┬─────────────┘
                                       │                 │
                                       ▼                 ▼
                          SQLite Safe Persistence   SecOps Analytics
                          (Zero Sensitive PII)      Telemetry Dashboard
```

---

### 4. Mathematical Modeling & Risk Scoring Logic

#### 4.1 Risk Polarity
Under our defensive risk model:
$$\text{Higher Score} = \text{Greater Vulnerability / Higher Exposure}$$
- **0–20: LOW** (Hardened profile; private audience; TOTP MFA active; minimal personal data exposed).
- **21–40: MODERATE** (Acceptable baseline; non-essential trivia or secondary controls absent).
- **41–70: HIGH** (Elevated exposure; unvetted connection requests, search indexing enabled, public email).
- **71–100: CRITICAL** (Severe vulnerability; public phone, real-time geolocation sharing, missing MFA).

#### 4.2 Category Risk Formulation
For each category $c \in \{1 \dots 10\}$, let $Q_c$ represent the set of questions within that category, and $R(q)$ denote the assigned risk points ($0 \le R(q) \le 100$):
$$S_c = \frac{1}{|Q_c|} \sum_{q \in Q_c} R(q)$$

#### 4.3 Weighted Overall Risk Formulation
Let $W_c$ represent the configurable category weight such that $\sum_{c=1}^{10} W_c = 1.0$:
$$S_{\text{overall}} = \sum_{c=1}^{10} \left( S_c \times W_c \right)$$

Default production weights reflect threat severity:
- **Location Privacy:** 15% (Physical stalking, robbery signals)
- **Personal Information:** 15% (Identity theft, financial fraud)
- **Authentication & Security:** 15% (Account takeover vectors)
- **Profile Visibility:** 10% (Automated web reconnaissance)
- **Friends & Connections:** 10% (Network infiltration, cloned profiles)
- **Posts & Content:** 10% (Workplace badge/screen exposure)
- **Social Engineering:** 10% (Spear-phishing & pretext susceptibility)
- **Tagging & Mentions:** 5% (External association without consent)
- **Third-Party Applications:** 5% (OAuth API token sprawl)
- **Digital Footprint:** 5% (Historical residue & abandoned accounts)
$$\sum W_c = 0.15 + 0.15 + 0.15 + 0.10 + 0.10 + 0.10 + 0.10 + 0.05 + 0.05 + 0.05 = 1.00$$

---

### 5. Synthetic Dataset Generation
To support aggregate SecOps analytics without harvesting data from real people, `data/generate_dataset.py` constructs **1,200 synthetic user records** distributed across four realistic behavioral personas:
1. **Privacy Champions (15%):** Strict private settings, TOTP MFA enabled, no public phone or location tags (Low risk).
2. **Average Internet Users (45%):** Mixed visibility, friends-only baseline, occasional location sharing, partial MFA (Moderate / High risk).
3. **Oversharers (30%):** Fully public profiles, real-time check-ins, advance vacation posts, public contact links (High / Critical risk).
4. **Vulnerable / Naive (10%):** Zero security controls, password reuse, open DMs, unreviewed apps (Critical risk).

The dataset is persisted to `data/social_media_privacy_assessments.csv` and partially seeded into the local SQLite database to populate dashboard analytics immediately upon installation.

---

### 6. Experimental Results & Verification

#### 6.1 Automated Test Suite
The framework incorporates **32 automated unit and integration tests** in `tests/test_privacy_assessment.py`. 
Key verified behaviors:
- **Test 1 & 2:** Extreme profile bounds verify low-risk baseline ($\le 20.0$) and high-risk baseline ($\ge 71.0$).
- **Test 3–20:** Deterministic trigger of individual critical findings (MFA missing, phone public, travel announced).
- **Test 23–25:** Boundary testing at 20.0 (Low), 40.0 (Moderate), 70.0 (High), and 70.1 (Critical).
- **Test 27:** Improvement simulator generates strictly positive risk reduction ($\Delta > 0$).
- **Test 29:** SQLite schema inspection confirms zero sensitive columns exist (`phone_number`, `password`, `ssn` absent).
- **Test 30:** ReportLab PDF generator builds binary streams without memory exceptions.
- **Test 31 & 32:** EXIF metadata inspector and stripper successfully parse and sanitize image buffers.

**Execution Result:**
```
Ran 32 tests in 0.438s
OK
```

---

### 7. Industry Relevance & Career Alignment
This project demonstrates proficiency across core domains sought by cybersecurity employers:
- **Cybersecurity / SOC Analyst:** Threat surface identification, vulnerability correlation, incident prevention.
- **Privacy Engineer:** Privacy-by-Design implementation, data minimization, GDPR compliance engineering.
- **Governance, Risk & Compliance (GRC) Analyst:** Quantitative risk scoring, compliance auditing, control benchmarking.
- **Security Awareness Specialist:** Actionable employee behavioral coaching, educational threat modeling.

---

### 8. Conclusion & Future Scope
The **Social Media Privacy Risk Assessment Framework** provides a practical, ethical, and mathematically sound approach to mitigating digital exposure. By avoiding invasive scraping and prioritizing defensive self-assessment, the platform empowers individuals and enterprises to systematically shrink their digital footprint.

Future defensive extensions include:
- Platform-specific deep links directly navigating to specific setting pages on Instagram, LinkedIn, and X.
- Enterprise multi-tenant reporting for anonymized employee security culture assessment.
- Client-side offline-first WebAssembly (Wasm) mode for zero-backend browser execution.
