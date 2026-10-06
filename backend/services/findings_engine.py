"""
Findings Engine Service
Analyzes user answers and pinpoints specific privacy vulnerabilities,
oversharing vectors, and security misconfigurations.
"""

from typing import Dict, Any, List
from backend.utils.questionnaire_data import QUESTION_MAP

FINDING_RULES = [
    {
        "id": "FIND_PHONE_PUBLIC",
        "qid": "q5",
        "trigger": ["YES"],
        "category": "CAT_PERSONAL_INFO",
        "severity": "CRITICAL",
        "title": "Personal Phone Number Publicly Visible",
        "description": "Your phone number is exposed on your public profile or bio.",
        "risk_impact": "Direct vulnerability to SMS phishing (smishing), SIM-swap hijacking, and caller-ID spoofing."
    },
    {
        "id": "FIND_MFA_DISABLED",
        "qid": "q26",
        "trigger": ["NO"],
        "category": "CAT_AUTH_SECURITY",
        "severity": "CRITICAL",
        "title": "Multi-Factor Authentication (MFA) Disabled",
        "description": "Your account relies strictly on a single password factor for login authentication.",
        "risk_impact": "Account takeover if your password is breached, phished, or leaked in an external database."
    },
    {
        "id": "FIND_REALTIME_LOCATION",
        "qid": "q10",
        "trigger": ["YES"],
        "category": "CAT_LOCATION",
        "severity": "CRITICAL",
        "title": "Real-Time Location Sharing Enabled",
        "description": "You regularly broadcast live check-ins or real-time location tags.",
        "risk_impact": "Enables physical stalking, travel tracking, and informs malicious actors of an unoccupied residence."
    },
    {
        "id": "FIND_PASSWORD_REUSE",
        "qid": "q27",
        "trigger": ["YES", "SOMETIMES"],
        "category": "CAT_AUTH_SECURITY",
        "severity": "HIGH",
        "title": "Password Reuse across Online Services",
        "description": "You reuse the same password or slight variations across multiple platforms.",
        "risk_impact": "High exposure to automated credential stuffing campaigns from third-party breach dumps."
    },
    {
        "id": "FIND_FULL_BIRTHDAY",
        "qid": "q7",
        "trigger": ["YES"],
        "category": "CAT_PERSONAL_INFO",
        "severity": "HIGH",
        "title": "Full Birth Date (Day, Month, Year) Exposed",
        "description": "Your full date of birth is visible publicly on your profile.",
        "risk_impact": "Birth date is a foundational identity token used in financial verification and account recovery attacks."
    },
    {
        "id": "FIND_TRAVEL_ANNOUNCEMENTS",
        "qid": "q11",
        "trigger": ["YES"],
        "category": "CAT_LOCATION",
        "severity": "HIGH",
        "title": "Public Travel Announcements Ahead of Time",
        "description": "You announce departure dates and vacations publicly prior to or during travel.",
        "risk_impact": "Signals to threat actors that your primary home is unoccupied, increasing burglary risk."
    },
    {
        "id": "FIND_UNKNOWN_CONNECTIONS",
        "qid": "q18",
        "trigger": ["YES", "SOMETIMES"],
        "category": "CAT_CONNECTIONS",
        "severity": "HIGH",
        "title": "Accepting Unknown Connection Requests",
        "description": "You accept friend requests from unfamiliar profiles or unverified mutual contacts.",
        "risk_impact": "Defeats 'Friends Only' privacy boundaries and enables social-engineering pretexting and stalking."
    },
    {
        "id": "FIND_TAG_REVIEW_DISABLED",
        "qid": "q22",
        "trigger": ["NO"],
        "category": "CAT_TAGGING",
        "severity": "HIGH",
        "title": "Timeline Tag Review Disabled",
        "description": "Photos and posts where others tag you appear on your profile automatically without your approval.",
        "risk_impact": "Other users can unilaterally reveal your whereabouts, activities, and sensitive associations."
    },
    {
        "id": "FIND_EMAIL_PUBLIC",
        "qid": "q6",
        "trigger": ["YES"],
        "category": "CAT_PERSONAL_INFO",
        "severity": "HIGH",
        "title": "Personal Email Address Publicly Exposed",
        "description": "Your personal primary email address is openly visible on your public profile.",
        "risk_impact": "Target for automated scraping, targeted phishing emails, and spam bombardment."
    },
    {
        "id": "FIND_PROFILE_PUBLIC",
        "qid": "q1",
        "trigger": ["PUBLIC"],
        "category": "CAT_PROFILE",
        "severity": "HIGH",
        "title": "Fully Public Profile Visibility",
        "description": "Your primary social media profile is open to the entire global internet.",
        "risk_impact": "Enables automated reconnaissance, OSINT profiling, and identity cloning."
    },
    {
        "id": "FIND_WORK_BADGE_SCREENS",
        "qid": "q15",
        "trigger": ["YES"],
        "category": "CAT_CONTENT",
        "severity": "HIGH",
        "title": "Workplace Badges or Computer Screens Posted",
        "description": "You have posted imagery containing employee IDs, barcodes, or active monitor displays.",
        "risk_impact": "Leaks corporate credentials, internal hostnames, badge numbers, and facility layout."
    },
    {
        "id": "FIND_THIRD_PARTY_STALE",
        "qid": "q31",
        "trigger": ["NO", "SOMETIMES"],
        "category": "CAT_THIRD_PARTY",
        "severity": "MODERATE",
        "title": "Unreviewed Third-Party App Authorizations",
        "description": "Connected third-party applications and quizzes have not been audited or revoked.",
        "risk_impact": "Deprecated apps retain persistent OAuth access tokens capable of querying your account data."
    },
    {
        "id": "FIND_LOGIN_ALERTS_OFF",
        "qid": "q28",
        "trigger": ["NO"],
        "category": "CAT_AUTH_SECURITY",
        "severity": "MODERATE",
        "title": "Unrecognized Login Alerts Disabled",
        "description": "No notifications are configured when a new browser or foreign IP accesses your account.",
        "risk_impact": "Delays intrusion detection if an unauthorized session is initiated by an adversary."
    },
    {
        "id": "FIND_SEARCH_INDEXING",
        "qid": "q2",
        "trigger": ["YES"],
        "category": "CAT_PROFILE",
        "severity": "MODERATE",
        "title": "Search Engine Indexing Active",
        "description": "Search engines are permitted to index and link directly to your profile page.",
        "risk_impact": "Aggregates your account across global search indexes, even for people without platform accounts."
    },
    {
        "id": "FIND_HISTORICAL_POSTS",
        "qid": "q39",
        "trigger": ["NO"],
        "category": "CAT_FOOTPRINT",
        "severity": "MODERATE",
        "title": "Historical Public Posts Never Audited",
        "description": "Old public posts from prior years remain indefinitely exposed on your timeline.",
        "risk_impact": "Accumulated historical footprint leaves outdated opinions and locations visible to prospective employers."
    },
    {
        "id": "FIND_QUIZ_HONEYPOTS",
        "qid": "q17",
        "trigger": ["YES"],
        "category": "CAT_CONTENT",
        "severity": "MODERATE",
        "title": "Participation in Viral Trivia Quizzes",
        "description": "You have responded to public quizzes prompting for childhood streets, pet names, or birth years.",
        "risk_impact": "Provides threat actors with common answers to account password recovery security questions."
    },
    {
        "id": "FIND_OPEN_DMS",
        "qid": "q35",
        "trigger": ["YES"],
        "category": "CAT_SOCIAL_ENG",
        "severity": "MODERATE",
        "title": "Unfiltered Direct Messaging Permitted",
        "description": "Anyone on the platform can send you direct messages without connection verification.",
        "risk_impact": "Increases exposure to spear-phishing messages, malware links, and impersonation attempts."
    },
    {
        "id": "FIND_ABANDONED_ACCOUNTS",
        "qid": "q40",
        "trigger": ["YES"],
        "category": "CAT_FOOTPRINT",
        "severity": "LOW",
        "title": "Dormant / Abandoned Social Accounts Active",
        "description": "You maintain legacy accounts on platforms you no longer actively monitor.",
        "risk_impact": "Unmonitored accounts with outdated passwords can be hijacked for spam without your immediate knowledge."
    }
]


def generate_privacy_findings(responses: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Evaluates responses against rule set and generates a list of identified
    privacy weaknesses sorted by severity.
    """
    findings = []
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3}

    for rule in FINDING_RULES:
        val = str(responses.get(rule["qid"], "")).upper()
        if val in rule["trigger"]:
            findings.append({
                "finding_id": rule["id"],
                "question_id": rule["qid"],
                "category": rule["category"],
                "severity": rule["severity"],
                "title": rule["title"],
                "description": rule["description"],
                "risk_impact": rule["risk_impact"]
            })

    # Sort findings by severity (CRITICAL first, then HIGH, etc.)
    findings.sort(key=lambda f: severity_order.get(f["severity"], 4))
    return findings
