"""
Recommendation Engine Service
Generates targeted, prioritized, actionable remediation guidance
based on detected privacy findings.
"""

from typing import List, Dict, Any

RECOMMENDATION_CATALOG = {
    "FIND_PHONE_PUBLIC": {
        "priority": "IMMEDIATE",
        "action": "Remove or Hide Personal Phone Number",
        "category": "CAT_PERSONAL_INFO",
        "steps": [
            "Navigate to Profile > Edit Profile > Contact Information.",
            "Change phone number audience to 'Only Me' or remove it from public display.",
            "Ensure the platform does not allow phone lookup in 'Privacy & Safety' settings."
        ],
        "rationale": "Mitigates SIM-swap fraud, automated robocalls, and targeted SMS phishing (smishing)."
    },
    "FIND_MFA_DISABLED": {
        "priority": "IMMEDIATE",
        "action": "Enable Multi-Factor Authentication (Authenticator App / TOTP)",
        "category": "CAT_AUTH_SECURITY",
        "steps": [
            "Open Settings > Security & Login > Two-Factor Authentication.",
            "Choose 'Authentication App' (such as Google Authenticator, Aegis, or Bitwarden) over SMS.",
            "Scan the QR code, save emergency backup recovery codes in a secure vault."
        ],
        "rationale": "Guarantees that even if your password is stolen or breached, attackers cannot access your account."
    },
    "FIND_REALTIME_LOCATION": {
        "priority": "IMMEDIATE",
        "action": "Cease Real-Time Location Broadcasting and Live Check-ins",
        "category": "CAT_LOCATION",
        "steps": [
            "Revoke precise location permissions for social media apps in your phone OS settings.",
            "Adopt the 'post after departure' rule: upload venue photos only after you have vacated the location.",
            "Remove active location stamps from stories and recent status updates."
        ],
        "rationale": "Protects physical safety, prevents stalking, and keeps real-time habits private."
    },
    "FIND_PASSWORD_REUSE": {
        "priority": "IMPORTANT",
        "action": "Migrate to a Unique Password via Password Manager",
        "category": "CAT_AUTH_SECURITY",
        "steps": [
            "Install a verified password manager (Bitwarden, 1Password, or KeePassXC).",
            "Generate a random 16+ character alphanumeric passphrase for your social account.",
            "Never reuse this password on any other service or social network."
        ],
        "rationale": "Neutralizes automated credential stuffing attacks sourced from unrelated third-party data breaches."
    },
    "FIND_FULL_BIRTHDAY": {
        "priority": "IMPORTANT",
        "action": "Hide Birth Year or Restrict Birthday Visibility",
        "category": "CAT_PERSONAL_INFO",
        "steps": [
            "Go to Profile > About > Basic Info > Birth Date.",
            "Set the birth year to 'Only Me' or hide the entire birth date from public view.",
            "Leave at most only month and day if birthday greetings are desired."
        ],
        "rationale": "Deprives cybercriminals of the foundational identity anchor used in credit inquiries and identity theft."
    },
    "FIND_TRAVEL_ANNOUNCEMENTS": {
        "priority": "IMPORTANT",
        "action": "Post Travel and Vacation Content Retrospectively",
        "category": "CAT_LOCATION",
        "steps": [
            "Avoid posting countdowns, flight itineraries, or boarding passes.",
            "Share travel photos and albums only after returning home.",
            "Instruct travel companions not to tag your live location during the trip."
        ],
        "rationale": "Prevents broadcasting to potential burglars that your residence is currently empty."
    },
    "FIND_UNKNOWN_CONNECTIONS": {
        "priority": "IMPORTANT",
        "action": "Filter and Vet Inbound Connection Requests",
        "category": "CAT_CONNECTIONS",
        "steps": [
            "Set friend request permissions to 'Friends of Friends' where available.",
            "Decline requests from profiles with no mutual history or suspicious account age.",
            "Perform a quarterly prune to remove unknown or inactive contacts."
        ],
        "rationale": "Prevents adversaries from infiltrating your private circle to harvest friends-only updates."
    },
    "FIND_TAG_REVIEW_DISABLED": {
        "priority": "IMPORTANT",
        "action": "Enable Timeline Tag Review and Mention Approval",
        "category": "CAT_TAGGING",
        "steps": [
            "Open Settings > Profile and Tagging > Reviewing.",
            "Enable 'Review posts that you are tagged in before they appear on your profile'.",
            "Enable 'Review tags that people add to your posts before the tags appear'."
        ],
        "rationale": "Maintains unilateral control over what media and commentary is associated with your name."
    },
    "FIND_EMAIL_PUBLIC": {
        "priority": "IMPORTANT",
        "action": "Hide Personal Email or Use Alias",
        "category": "CAT_PERSONAL_INFO",
        "steps": [
            "Set personal email visibility to 'Only Me'.",
            "If business contact is required, use a separate masked email alias (e.g. SimpleLogin / Firefox Relay)."
        ],
        "rationale": "Shields your primary email address from automated crawlers and spear-phishing lists."
    },
    "FIND_PROFILE_PUBLIC": {
        "priority": "IMPORTANT",
        "action": "Restrict Profile Visibility to Approved Connections",
        "category": "CAT_PROFILE",
        "steps": [
            "Switch main profile setting to 'Private' or 'Friends Only'.",
            "Set future posts default audience to 'Friends'.",
            "Review public bio to eliminate personal trivia."
        ],
        "rationale": "Constrains your digital footprint to individuals you have directly consented to interact with."
    },
    "FIND_WORK_BADGE_SCREENS": {
        "priority": "IMPORTANT",
        "action": "Audit and Remove Media Displaying Badges or Workstations",
        "category": "CAT_CONTENT",
        "steps": [
            "Delete or blur past photos displaying employee badges, lanyard IDs, or desks.",
            "Ensure computer screens in background photos are powered off or cropped out."
        ],
        "rationale": "Prevents corporate reconnaissance, physical badge forgery, and internal network disclosure."
    },
    "FIND_THIRD_PARTY_STALE": {
        "priority": "GOOD PRACTICE",
        "action": "Audit and Revoke Stale Third-Party App Permissions",
        "category": "CAT_THIRD_PARTY",
        "steps": [
            "Open Settings > Apps and Websites / Connected Accounts.",
            "Review active OAuth integrations and delete any tool not used in the past 6 months.",
            "Check permissions granted to remaining apps and downgrade to least privilege."
        ],
        "rationale": "Eliminates lingering API access tokens from third-party services that may later be compromised."
    },
    "FIND_LOGIN_ALERTS_OFF": {
        "priority": "GOOD PRACTICE",
        "action": "Enable Unrecognized Login Alerts",
        "category": "CAT_AUTH_SECURITY",
        "steps": [
            "Go to Settings > Security and Login > Get alerts about unrecognized logins.",
            "Turn on Notifications and Email alerts."
        ],
        "rationale": "Enables rapid incident response if an unauthorized device accesses your account."
    },
    "FIND_SEARCH_INDEXING": {
        "priority": "GOOD PRACTICE",
        "action": "Disable Search Engine Indexing",
        "category": "CAT_PROFILE",
        "steps": [
            "Go to Settings > Privacy > How people find and contact you.",
            "Turn off 'Do you want search engines outside of the platform to link to your profile?'."
        ],
        "rationale": "Prevents your profile from appearing in public Google and Bing search results."
    },
    "FIND_HISTORICAL_POSTS": {
        "priority": "GOOD PRACTICE",
        "action": "Batch Limit Historical Public Posts",
        "category": "CAT_FOOTPRINT",
        "steps": [
            "Navigate to Privacy Settings > Your Activity.",
            "Select 'Limit Past Posts' to convert all past public posts to Friends-Only.",
            "Review and archive memories that you no longer wish to share."
        ],
        "rationale": "Minimizes historical digital footprints that could be taken out of context years later."
    },
    "FIND_QUIZ_HONEYPOTS": {
        "priority": "GOOD PRACTICE",
        "action": "Refrain from Social Quizzes & Update Security Questions",
        "category": "CAT_CONTENT",
        "steps": [
            "Do not participate in public trivia challenges or surveys asking for childhood memories.",
            "Update bank and email security questions to randomly generated answers stored in your password manager."
        ],
        "rationale": "Neutralizes OSINT collection attacks aimed at bypassing password reset workflows."
    },
    "FIND_OPEN_DMS": {
        "priority": "GOOD PRACTICE",
        "action": "Filter Inbound Direct Messages",
        "category": "CAT_SOCIAL_ENG",
        "steps": [
            "Change messaging preferences to 'Message Requests' or 'Friends Only'.",
            "Enable automated spam and scam filtering for incoming requests."
        ],
        "rationale": "Reduces exposure to malicious links, unsolicited extortion, and social-engineering bait."
    },
    "FIND_ABANDONED_ACCOUNTS": {
        "priority": "GOOD PRACTICE",
        "action": "Close or Delete Dormant Social Media Accounts",
        "category": "CAT_FOOTPRINT",
        "steps": [
            "Identify legacy platforms (old blogs, retired forums, unused social apps).",
            "Log in, export desired data, and permanently submit account deletion requests."
        ],
        "rationale": "Shrinks your attack surface by eliminating forgotten targets vulnerable to silent hijacking."
    }
}


def generate_recommendations(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms detected findings into a prioritized list of personalized recommendations.
    Grouped by priority: IMMEDIATE -> IMPORTANT -> GOOD PRACTICE.
    """
    recommendations = []
    priority_order = {"IMMEDIATE": 0, "IMPORTANT": 1, "GOOD PRACTICE": 2}

    for finding in findings:
        fid = finding["finding_id"]
        if fid in RECOMMENDATION_CATALOG:
            rec_info = RECOMMENDATION_CATALOG[fid]
            recommendations.append({
                "finding_id": fid,
                "priority": rec_info["priority"],
                "action": rec_info["action"],
                "category": rec_info["category"],
                "steps": rec_info["steps"],
                "rationale": rec_info["rationale"],
                "title": finding["title"]
            })

    recommendations.sort(key=lambda r: priority_order.get(r["priority"], 3))
    return recommendations
