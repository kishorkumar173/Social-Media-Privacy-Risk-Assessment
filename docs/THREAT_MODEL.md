# Threat Model: Social Media User Privacy & Exposure

## 1. Executive Summary
This threat model assesses defensive exposure risks confronting typical social media users. It analyzes assets, threat agents, vulnerabilities, attack surfaces, and defensive countermeasures under STRIDE and NIST SP 800-30 frameworks.

---

## 2. Protected Assets

| Asset ID | Asset Name | Description | Sensitivity |
| :--- | :--- | :--- | :--- |
| **AST-01** | **Primary Account Access** | Social media account credentials and active sessions | High |
| **AST-02** | **Identity Anchor Data** | Full legal name, date of birth, phone number, personal email | Critical |
| **AST-03** | **Physical Geolocation** | Live venues, travel itineraries, home neighborhood, daily commute | Critical |
| **AST-04** | **Social Trust Graph** | Family linkages, friends lists, coworkers, professional affiliations | Medium |
| **AST-05** | **Private / Restricted Media** | Family photos, minor children images, workplace screens, badges | High |

---

## 3. Threat Actors

1. **Opportunistic Cybercriminals:** Script kiddies and automated crawlers harvesting public PII for credential stuffing, SIM-swap attacks, and bulk spam lists.
2. **Social Engineers / Spear Phishers:** Actors conducting targeted reconnaissance (OSINT) to craft high-conviction pretexting scenarios.
3. **Physical Threat Actors / Burglars:** Individuals monitoring real-time check-ins and vacation departure posts to identify empty residences.
4. **Data Aggregators & People Search Engines:** Commercial scrapers aggregating public social comments, photos, and handles into persistent cross-platform dossiers.

---

## 4. Threat Matrix & Defensive Countermeasures

| Asset | Threat | Exposure Vector | Potential Impact | Existing Common Weakness | Recommended Countermeasure |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AST-01** | Account Takeover (ATO) | Reused passwords breached on unrelated sites | Complete profile loss, spam propagation to contacts | Single password authentication, no MFA | Enforce TOTP / FIDO2 MFA; unique 16+ char password via password manager |
| **AST-02** | Identity Theft & Recovery Hijacking | Publicly visible birth year and personal phone number | Fraudulent credit lines, bypass of SMS security questions | Phone and birth date displayed on public bio | Set phone visibility to "Only Me"; hide birth year |
| **AST-03** | Burglary & Physical Stalking | Real-time check-ins, vacation announcements | Physical invasion of unoccupied residence | Posting stories live while away from home | Post trip media retrospectively after departure; disable GPS tags |
| **AST-04** | Impersonation & Cloned Account Scams | Public friends list combined with open follower access | Fraudulent financial requests sent to close relatives | Friend list visible to anyone on the web | Restrict friends list visibility to approved mutual connections |
| **AST-05** | Corporate Reconnaissance | Photos displaying office badges, visitor passes, screens | Barcode decoding leaks corporate IDs and internal systems | Uploading celebratory work anniversaries with visible badges | Crop or blur credentials; enforce workplace digital hygiene |

---

## 5. Privacy Risk Assessment Matrix

| Threat Scenario | Exposure Likelihood | Potential Impact | Inherent Risk Rating | Residual Risk with Countermeasure |
| :--- | :---: | :---: | :---: | :---: |
| **Public Phone Number** | High | High | **CRITICAL** | Low (Hidden from profile) |
| **MFA Disabled** | High | Critical | **CRITICAL** | Low (Hardware / TOTP MFA enabled) |
| **Real-Time Geolocation Check-in** | Medium | Critical | **HIGH** | Low (Retrospective sharing) |
| **Full Date of Birth Public** | High | Medium | **HIGH** | Low (Birth year concealed) |
| **Open Direct Messaging (DMs)** | High | Medium | **MODERATE** | Low (Filtered to message requests) |
| **Timeline Tag Review Disabled** | Medium | Medium | **MODERATE** | Low (Manual tag approval enabled) |
| **Dormant / Abandoned Accounts** | Medium | Low | **LOW** | Low (Permanent account closure) |
