# Privacy by Design & Data Minimization Implementation

## 1. Overview
The **Social Media Privacy Risk Assessment Framework** was engineered from inception according to the **7 Foundational Principles of Privacy by Design (Cavoukian)** and international regulatory standards including **GDPR Articles 5, 17, and 25**.

Rather than monitoring or spying on individuals, this application evaluates security postures defensively through **self-reported configuration telemetry** and **zero sensitive data persistence**.

---

## 2. Foundational Principles in Practice

### Principle 1: Proactive not Reactive; Preventative not Remedial
- The framework anticipates exposure vectors before adversaries exploit them.
- Instead of detecting breaches post-compromise, it audits open configurations (MFA status, search indexing, location broadcasting) to prevent initial access.

### Principle 2: Privacy as the Default Setting
- All simulation and questionnaire states default to conservative, hardened assumptions.
- Assessments are anonymous by default: no user registration, email entry, or social handle linking is required to execute a full risk audit.

### Principle 3: Privacy Embedded into Design
- **Zero Raw PII Storage:** The system architecture intentionally lacks database columns for real phone numbers, passwords, emails, street addresses, or payment cards.
- Questions are strictly formatted as categorical indicators (e.g., *"Is your phone number visible? YES / NO"*), allowing mathematical risk scoring without acquiring the sensitive token itself.

### Principle 4: Full Functionality – Positive-Sum, not Zero-Sum
- Users receive high-fidelity risk metrics, interactive category radar charts, and downloadable PDF audits without compromising their privacy in exchange for the service.

### Principle 5: End-to-End Security – Full Lifecycle Protection
- Responses are processed in-memory or persisted into normalized relational tables using randomized UUID identifiers (`ASM-XXXXXX`).
- Security response headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Permissions-Policy`) protect users against clickjacking and MIME sniffing.

### Principle 6: Visibility and Transparency – Keep it Open
- The mathematical scoring model, category weights, and risk thresholds are open and fully auditable in `backend/services/scoring_engine.py`.
- Users can inspect exactly how each answer influences category risk and net exposure score.

### Principle 7: Respect for User Privacy – Keep it User-Centric
- **Right to Erasure (GDPR Art. 17):** Users can permanently delete their assessment record with a single click via `DELETE /api/assessment/{id}`.
- **Local EXIF Inspector:** Images processed through the local metadata module are analyzed 100% in-memory and never transferred across the network.

---

## 3. Data Flow & Minimization Comparison

| Data Field | Conventional Profiling Tool | PrivacyGuard Framework | Rationale |
| :--- | :--- | :--- | :--- |
| **User Name** | Scraped / Stored | **Never Collected** | Not required for configuration evaluation |
| **Phone Number** | Collected in plaintext | **Boolean ("YES" / "NO")** | Knowing exposure status is sufficient |
| **Password** | Evaluated or hashed | **Never Requested** | Asks only about reuse habits & manager usage |
| **GPS Coordinates** | Tracked live | **Boolean ("YES" / "NO")** | Evaluates real-time check-in habits safely |
| **Images** | Scraped and indexed | **In-memory local inspection only** | Strips EXIF without persisting image |
