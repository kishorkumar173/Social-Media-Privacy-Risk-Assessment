"""
Questionnaire Metadata and Definitions
Defines all 42 questions across 10 defensive privacy categories,
response scoring weights, options, and security awareness tips.
"""

CATEGORIES = {
    "CAT_PROFILE": {
        "id": "CAT_PROFILE",
        "name": "Profile Visibility",
        "weight": 0.10,
        "description": "Evaluation of general account exposure, public discoverability, and profile searchability.",
        "icon": "bi-person-badge"
    },
    "CAT_PERSONAL_INFO": {
        "id": "CAT_PERSONAL_INFO",
        "name": "Personal Information",
        "weight": 0.15,
        "description": "Exposure of sensitive identifiers, contact details, birth date, and background info.",
        "icon": "bi-card-text"
    },
    "CAT_LOCATION": {
        "id": "CAT_LOCATION",
        "name": "Location Privacy",
        "weight": 0.15,
        "description": "Real-time location sharing, check-ins, routine patterns, and geotagging.",
        "icon": "bi-geo-alt"
    },
    "CAT_CONTENT": {
        "id": "CAT_CONTENT",
        "name": "Posts & Content",
        "weight": 0.10,
        "description": "Default audience for posts, sensitive content, family photos, and workplace mentions.",
        "icon": "bi-chat-square-quote"
    },
    "CAT_CONNECTIONS": {
        "id": "CAT_CONNECTIONS",
        "name": "Friends & Followers",
        "weight": 0.10,
        "description": "Audience vetting, connection acceptance hygiene, and visibility of friends lists.",
        "icon": "bi-people"
    },
    "CAT_TAGGING": {
        "id": "CAT_TAGGING",
        "name": "Tagging & Mentions",
        "weight": 0.05,
        "description": "Third-party tagging controls, timeline review, and unsolicited mentions.",
        "icon": "bi-tag"
    },
    "CAT_AUTH_SECURITY": {
        "id": "CAT_AUTH_SECURITY",
        "name": "Authentication & Account Security",
        "weight": 0.15,
        "description": "Multi-factor authentication (MFA), password uniqueness, login alerts, and session audits.",
        "icon": "bi-shield-lock"
    },
    "CAT_THIRD_PARTY": {
        "id": "CAT_THIRD_PARTY",
        "name": "Third-Party Apps",
        "weight": 0.05,
        "description": "Connected OAuth applications, social login tokens, and stale permission grants.",
        "icon": "bi-grid-3x3-gap"
    },
    "CAT_SOCIAL_ENG": {
        "id": "CAT_SOCIAL_ENG",
        "name": "Messaging & Social Engineering",
        "weight": 0.10,
        "description": "Vulnerability to spear phishing, suspicious DMs, link verification, and credential sharing.",
        "icon": "bi-exclamation-triangle"
    },
    "CAT_FOOTPRINT": {
        "id": "CAT_FOOTPRINT",
        "name": "Digital Footprint",
        "weight": 0.05,
        "description": "Archival post audits, forgotten public comments, and historical exposure management.",
        "icon": "bi-clock-history"
    }
}

QUESTIONS = [
    # CATEGORY A: Profile Visibility
    {
        "id": "q1",
        "category": "CAT_PROFILE",
        "text": "What is the primary visibility setting of your main social media profile?",
        "options": [
            {"label": "Public (visible to everyone on the internet)", "value": "PUBLIC", "risk_points": 100},
            {"label": "Friends / Connections Only", "value": "FRIENDS", "risk_points": 25},
            {"label": "Private / Restricted Account", "value": "PRIVATE", "risk_points": 0}
        ],
        "tip": "Restricting profile visibility reduces opportunistic profiling by unknown actors."
    },
    {
        "id": "q2",
        "category": "CAT_PROFILE",
        "text": "Can external search engines (Google, Bing) index and link directly to your profile?",
        "options": [
            {"label": "Yes (search engine indexing enabled)", "value": "YES", "risk_points": 80},
            {"label": "No (indexing disabled in privacy settings)", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 50}
        ],
        "tip": "Turning off search indexing prevents your profile from appearing in general search results."
    },
    {
        "id": "q3",
        "category": "CAT_PROFILE",
        "text": "Is your followers or friends list visible to anyone other than your approved connections?",
        "options": [
            {"label": "Publicly visible to all", "value": "YES", "risk_points": 75},
            {"label": "Only visible to me or approved connections", "value": "NO", "risk_points": 0},
            {"label": "Sometimes / Partially visible", "value": "SOMETIMES", "risk_points": 40},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 45}
        ],
        "tip": "Public friend lists enable attackers to map out your trusted network for targeted spear-phishing."
    },
    {
        "id": "q4",
        "category": "CAT_PROFILE",
        "text": "Can anyone find your account by searching your email address or phone number?",
        "options": [
            {"label": "Yes, anyone can look me up", "value": "YES", "risk_points": 85},
            {"label": "No, discoverability is restricted", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 50}
        ],
        "tip": "Restricting lookup by contact identifiers prevents automated scraping and phone-based correlation."
    },

    # CATEGORY B: Personal Information
    {
        "id": "q5",
        "category": "CAT_PERSONAL_INFO",
        "text": "Is your personal phone number visible on your public bio or profile overview?",
        "options": [
            {"label": "Yes, it is visible publicly", "value": "YES", "risk_points": 100},
            {"label": "No, it is hidden or strictly private", "value": "NO", "risk_points": 0},
            {"label": "Visible only to mutual friends", "value": "SOMETIMES", "risk_points": 35}
        ],
        "tip": "Public phone numbers expose individuals to SMS phishing (smishing), SIM swapping, and harassment."
    },
    {
        "id": "q6",
        "category": "CAT_PERSONAL_INFO",
        "text": "Is your personal email address publicly displayed on your profile?",
        "options": [
            {"label": "Yes, publicly visible", "value": "YES", "risk_points": 85},
            {"label": "No, completely hidden", "value": "NO", "risk_points": 0},
            {"label": "Only a generic/work business inquiry address", "value": "SOMETIMES", "risk_points": 25}
        ],
        "tip": "Public personal emails are harvested for credential stuffing, spam campaigns, and targeted phishing."
    },
    {
        "id": "q7",
        "category": "CAT_PERSONAL_INFO",
        "text": "Do you publicly display your full birth date (day, month, and year)?",
        "options": [
            {"label": "Yes, full date including year is public", "value": "YES", "risk_points": 95},
            {"label": "Only month and day (year is hidden)", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, birthday is completely private", "value": "NO", "risk_points": 0}
        ],
        "tip": "Full birth dates represent primary verification tokens used in identity theft and password recovery resets."
    },
    {
        "id": "q8",
        "category": "CAT_PERSONAL_INFO",
        "text": "Are your specific workplace, employer, or school name publicly listed?",
        "options": [
            {"label": "Yes, current workplace/school is public", "value": "YES", "risk_points": 70},
            {"label": "No, not listed or set to private", "value": "NO", "risk_points": 0},
            {"label": "Only industry or general field (no exact company/campus)", "value": "SOMETIMES", "risk_points": 20}
        ],
        "tip": "Specific workplace details allow attackers to craft convincing corporate pretexting emails."
    },
    {
        "id": "q9",
        "category": "CAT_PERSONAL_INFO",
        "text": "Do you publicly list family relationships or close relatives on your profile?",
        "options": [
            {"label": "Yes, family members are linked publicly", "value": "YES", "risk_points": 75},
            {"label": "No, family details are unlisted", "value": "NO", "risk_points": 0},
            {"label": "Occasionally mentioned in comments/photos", "value": "SOMETIMES", "risk_points": 35}
        ],
        "tip": "Family linkages reveal security question answers (e.g., mother's maiden name) and enable grandparent scams."
    },

    # CATEGORY C: Location Privacy
    {
        "id": "q10",
        "category": "CAT_LOCATION",
        "text": "Do you use real-time check-ins or live location sharing when visiting venues?",
        "options": [
            {"label": "Yes, regularly share real-time locations", "value": "YES", "risk_points": 100},
            {"label": "Sometimes / On special occasions", "value": "SOMETIMES", "risk_points": 60},
            {"label": "No, never broadcast live location", "value": "NO", "risk_points": 0}
        ],
        "tip": "Broadcasting live locations informs malicious observers of your exact physical whereabouts in real time."
    },
    {
        "id": "q11",
        "category": "CAT_LOCATION",
        "text": "Do you publicly post upcoming travel schedules or announce when you are away from home?",
        "options": [
            {"label": "Yes, post before or while on trip", "value": "YES", "risk_points": 90},
            {"label": "Only post photos after returning home safely", "value": "NO", "risk_points": 10},
            {"label": "Sometimes share travel updates live", "value": "SOMETIMES", "risk_points": 50}
        ],
        "tip": "Announcing empty residences creates burglary vulnerability and aids targeted physical security threats."
    },
    {
        "id": "q12",
        "category": "CAT_LOCATION",
        "text": "Is automatic geotagging / location stamping enabled for your camera or social app posts?",
        "options": [
            {"label": "Yes, posts automatically attach GPS coordinates", "value": "YES", "risk_points": 85},
            {"label": "No, camera/app location access is disabled", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 50}
        ],
        "tip": "GPS tags embedded in posts can reveal home neighborhoods, commuting routes, and sensitive safe havens."
    },
    {
        "id": "q13",
        "category": "CAT_LOCATION",
        "text": "Can someone easily deduce your home address or daily commute from your posts?",
        "options": [
            {"label": "Yes, recognizable landmarks/street signs are visible", "value": "YES", "risk_points": 85},
            {"label": "No, I actively avoid posting residential surroundings", "value": "NO", "risk_points": 0},
            {"label": "Possibly from recurring neighborhood check-ins", "value": "SOMETIMES", "risk_points": 45}
        ],
        "tip": "Even without explicit geotags, visual cues like building facades and street corners leak physical locations."
    },

    # CATEGORY D: Posts & Content
    {
        "id": "q14",
        "category": "CAT_CONTENT",
        "text": "What is the default audience setting for your everyday posts and stories?",
        "options": [
            {"label": "Public (visible to everyone)", "value": "PUBLIC", "risk_points": 85},
            {"label": "Friends / Followers only", "value": "FRIENDS", "risk_points": 25},
            {"label": "Custom close friends list or private", "value": "PRIVATE", "risk_points": 0}
        ],
        "tip": "Defaulting to Friends-only limits casual content surveillance by crawlers and unvetted third parties."
    },
    {
        "id": "q15",
        "category": "CAT_CONTENT",
        "text": "Do you post photos showing workplace badges, boarding passes, certificates, or desk screens?",
        "options": [
            {"label": "Yes, have posted work passes/tickets/screens", "value": "YES", "risk_points": 95},
            {"label": "No, strictly avoid posting sensitive documents/screens", "value": "NO", "risk_points": 0},
            {"label": "Rarely / Only with partial blur", "value": "SOMETIMES", "risk_points": 40}
        ],
        "tip": "Badges and boarding passes encode barcodes containing PII, corporate IDs, and flight PNR numbers."
    },
    {
        "id": "q16",
        "category": "CAT_CONTENT",
        "text": "Do you publicly share photos of children, minor family members, or school uniforms?",
        "options": [
            {"label": "Yes, family and kids photos are public", "value": "YES", "risk_points": 80},
            {"label": "No, strictly kept private or faces hidden", "value": "NO", "risk_points": 0},
            {"label": "Shared only with close circle of friends", "value": "SOMETIMES", "risk_points": 25}
        ],
        "tip": "Protecting minors' digital footprints defends against facial harvesting and unauthorized image reuse."
    },
    {
        "id": "q17",
        "category": "CAT_CONTENT",
        "text": "Have you ever participated in viral social media quizzes (e.g., 'First pet name', 'Street you grew up on')?",
        "options": [
            {"label": "Yes, have answered several trivia quizzes", "value": "YES", "risk_points": 75},
            {"label": "No, never answer personal trivia quizzes", "value": "NO", "risk_points": 0},
            {"label": "Not Sure / Maybe in the past", "value": "NOT_SURE", "risk_points": 40}
        ],
        "tip": "Viral 'fun' quizzes are classic open-source intelligence honeypots harvest security question answers."
    },

    # CATEGORY E: Friends / Followers
    {
        "id": "q18",
        "category": "CAT_CONNECTIONS",
        "text": "How do you handle friend or follow requests from accounts you do not personally recognize?",
        "options": [
            {"label": "Usually accept them to expand network", "value": "YES", "risk_points": 90},
            {"label": "Strictly decline or ignore unknown users", "value": "NO", "risk_points": 0},
            {"label": "Accept if we have multiple mutual connections", "value": "SOMETIMES", "risk_points": 50}
        ],
        "tip": "Accepting unfamiliar connections bypasses 'Friends-Only' boundaries, rendering private posts accessible."
    },
    {
        "id": "q19",
        "category": "CAT_CONNECTIONS",
        "text": "Do you regularly perform an audit to remove inactive or unfamiliar contacts from your friends list?",
        "options": [
            {"label": "No, I never remove contacts", "value": "NO", "risk_points": 70},
            {"label": "Yes, audit connections once or twice a year", "value": "YES", "risk_points": 0},
            {"label": "Occasionally when I notice a strange profile", "value": "SOMETIMES", "risk_points": 30}
        ],
        "tip": "Periodic friend pruning prevents compromised or repurposed legacy accounts from monitoring your life."
    },
    {
        "id": "q20",
        "category": "CAT_CONNECTIONS",
        "text": "Are your account connection requests open to anyone on the platform?",
        "options": [
            {"label": "Yes, anyone can send me a request", "value": "YES", "risk_points": 60},
            {"label": "Restricted to friends-of-friends only", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 35}
        ],
        "tip": "Restricting request permissions reduces automated bot spam and malicious mass-friend campaigns."
    },
    {
        "id": "q21",
        "category": "CAT_CONNECTIONS",
        "text": "Have you ever accepted a duplicate profile request from a person you are already friends with?",
        "options": [
            {"label": "Yes, without verifying with them first", "value": "YES", "risk_points": 85},
            {"label": "No, I verify out-of-band before accepting", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 40}
        ],
        "tip": "Cloned profiles are a primary vector for identity impersonation and urgent financial deception scams."
    },

    # CATEGORY F: Tagging & Mentions
    {
        "id": "q22",
        "category": "CAT_TAGGING",
        "text": "Is 'Tag Review' or timeline review enabled so you must approve tags before they appear on your profile?",
        "options": [
            {"label": "Disabled (anyone can tag me directly)", "value": "NO", "risk_points": 90},
            {"label": "Enabled (I manually approve all tags)", "value": "YES", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 50}
        ],
        "tip": "Tag review gives you control over whether photos or comments taken by others attach to your identity."
    },
    {
        "id": "q23",
        "category": "CAT_TAGGING",
        "text": "Can strangers or non-friends tag you in public photos, giveaways, or promotional posts?",
        "options": [
            {"label": "Yes, anyone can tag me", "value": "YES", "risk_points": 75},
            {"label": "Only approved friends can tag me", "value": "SOMETIMES", "risk_points": 25},
            {"label": "No one can tag me / Tagging completely blocked", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 45}
        ],
        "tip": "Restricting tagging prevents scammers from drawing you into malicious crypto or giveaway schemes."
    },
    {
        "id": "q24",
        "category": "CAT_TAGGING",
        "text": "Can other users see posts on your profile that you were tagged in by third parties?",
        "options": [
            {"label": "Publicly visible to all viewers", "value": "PUBLIC", "risk_points": 80},
            {"label": "Only visible to my friends", "value": "FRIENDS", "risk_points": 25},
            {"label": "Only visible to me (hidden from profile)", "value": "PRIVATE", "risk_points": 0}
        ],
        "tip": "Controlling tagged post visibility prevents collateral oversharing initiated by acquaintances."
    },
    {
        "id": "q25",
        "category": "CAT_TAGGING",
        "text": "Can unknown users mention or quote your handle in public comment threads?",
        "options": [
            {"label": "Yes, anyone can mention me", "value": "YES", "risk_points": 65},
            {"label": "Only people I follow or friends", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 35}
        ],
        "tip": "Restricting mentions protects against automated harassment brigading and spam bots."
    },

    # CATEGORY G: Authentication & Account Security
    {
        "id": "q26",
        "category": "CAT_AUTH_SECURITY",
        "text": "Is Multi-Factor Authentication (MFA / 2FA) enabled on your social media account?",
        "options": [
            {"label": "No, MFA is disabled", "value": "NO", "risk_points": 100},
            {"label": "Yes, via SMS / Text message code", "value": "SOMETIMES", "risk_points": 30},
            {"label": "Yes, via Authenticator App (TOTP) or Hardware Key", "value": "YES", "risk_points": 0}
        ],
        "tip": "Hardware keys and TOTP apps provide strong protection against automated credential stuffing and phishing."
    },
    {
        "id": "q27",
        "category": "CAT_AUTH_SECURITY",
        "text": "Do you reuse your social media password on other websites or services?",
        "options": [
            {"label": "Yes, I use the same password across multiple sites", "value": "YES", "risk_points": 95},
            {"label": "No, each account has a unique generated password", "value": "NO", "risk_points": 0},
            {"label": "Similar variation with minor character change", "value": "SOMETIMES", "risk_points": 70}
        ],
        "tip": "Password reuse means a breach on a low-security website instantly compromises your main social account."
    },
    {
        "id": "q28",
        "category": "CAT_AUTH_SECURITY",
        "text": "Are 'Unrecognized Login Alerts' enabled to notify you of logins from new devices or locations?",
        "options": [
            {"label": "Disabled / Not active", "value": "NO", "risk_points": 80},
            {"label": "Enabled (alerts sent via email/push)", "value": "YES", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 45}
        ],
        "tip": "Immediate login alerts provide critical early warning if an attacker gains unauthorized session access."
    },
    {
        "id": "q29",
        "category": "CAT_AUTH_SECURITY",
        "text": "Do you periodically review your active login sessions and logged-in devices?",
        "options": [
            {"label": "No, never check logged-in devices", "value": "NO", "risk_points": 70},
            {"label": "Yes, regularly terminate unfamiliar sessions", "value": "YES", "risk_points": 0},
            {"label": "Only when something strange happens", "value": "SOMETIMES", "risk_points": 35}
        ],
        "tip": "Session auditing terminates forgotten browser logins on shared PCs or compromised hotel terminals."
    },
    {
        "id": "q30",
        "category": "CAT_AUTH_SECURITY",
        "text": "Are your account recovery methods (backup email, recovery phone) current and privately secured?",
        "options": [
            {"label": "Outdated or linked to shared/inaccessible email", "value": "NO", "risk_points": 85},
            {"label": "Up-to-date and protected by MFA", "value": "YES", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 45}
        ],
        "tip": "Abandoned recovery emails are high-value targets for attackers seeking account takeover via password reset."
    },

    # CATEGORY H: Third-Party Apps
    {
        "id": "q31",
        "category": "CAT_THIRD_PARTY",
        "text": "Do you review and revoke permissions for connected third-party apps and games?",
        "options": [
            {"label": "Never review connected apps", "value": "NO", "risk_points": 85},
            {"label": "Regularly review and delete old permissions", "value": "YES", "risk_points": 0},
            {"label": "Occasionally / Rarely", "value": "SOMETIMES", "risk_points": 45}
        ],
        "tip": "Third-party apps retain API tokens that may grant access to your profile data even after you stop using them."
    },
    {
        "id": "q32",
        "category": "CAT_THIRD_PARTY",
        "text": "Do you use 'Sign in with Social Account' (Google, Facebook, Apple) for random online quizzes or tools?",
        "options": [
            {"label": "Frequently, without checking permissions requested", "value": "YES", "risk_points": 80},
            {"label": "Never, prefer dedicated accounts or masked emails", "value": "NO", "risk_points": 0},
            {"label": "Only with reputable trusted services", "value": "SOMETIMES", "risk_points": 30}
        ],
        "tip": "Unvetted social sign-ins often request overreaching scopes like contact lists and private messaging access."
    },
    {
        "id": "q33",
        "category": "CAT_THIRD_PARTY",
        "text": "Have you granted third-party productivity/scheduling apps full access to post on your behalf?",
        "options": [
            {"label": "Yes, multiple tools have posting permissions", "value": "YES", "risk_points": 75},
            {"label": "No, no external app has write access", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 45}
        ],
        "tip": "Compromised third-party scheduling platforms have frequently been abused to distribute spam and malware."
    },
    {
        "id": "q34",
        "category": "CAT_THIRD_PARTY",
        "text": "Do you verify the developer reputation before connecting an application to your profile?",
        "options": [
            {"label": "No, just click authorize immediately", "value": "NO", "risk_points": 75},
            {"label": "Yes, inspect developer name, privacy policy, and ratings", "value": "YES", "risk_points": 0},
            {"label": "Sometimes", "value": "SOMETIMES", "risk_points": 35}
        ],
        "tip": "Adhering to Principle of Least Privilege means declining requests that seek unnecessary data permissions."
    },

    # CATEGORY I: Messaging & Social Engineering
    {
        "id": "q35",
        "category": "CAT_SOCIAL_ENG",
        "text": "Can any user send you direct messages (DMs) without a connection request or message filter?",
        "options": [
            {"label": "Yes, direct messaging is open to everyone", "value": "YES", "risk_points": 80},
            {"label": "Restricted to friends or filtered to message requests", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 40}
        ],
        "tip": "Open DMs facilitate unsolicited social engineering, extortion attempts, and malicious attachment delivery."
    },
    {
        "id": "q36",
        "category": "CAT_SOCIAL_ENG",
        "text": "How do you respond if a contact asks for urgent financial help or a verification code via DM?",
        "options": [
            {"label": "Often help immediately if they seem distressed", "value": "YES", "risk_points": 95},
            {"label": "Always call them directly or verify out-of-band first", "value": "NO", "risk_points": 0},
            {"label": "Ask questions within the same DM chat", "value": "SOMETIMES", "risk_points": 60}
        ],
        "tip": "Never send verification codes or funds based on in-app messages without out-of-band voice confirmation."
    },
    {
        "id": "q37",
        "category": "CAT_SOCIAL_ENG",
        "text": "Do you click links sent via direct messages or comments promising giveaways, contests, or votes?",
        "options": [
            {"label": "Yes, frequently participate in contests/links", "value": "YES", "risk_points": 90},
            {"label": "Never click unsolicited promotional links", "value": "NO", "risk_points": 0},
            {"label": "Only if sent by someone I know", "value": "SOMETIMES", "risk_points": 45}
        ],
        "tip": "Even links from known friends may be automated phishing blasts from an already compromised account."
    },
    {
        "id": "q38",
        "category": "CAT_SOCIAL_ENG",
        "text": "Have you ever shared sensitive personal opinions or credentials in an unencrypted social chat?",
        "options": [
            {"label": "Yes, shared passwords or sensitive notes", "value": "YES", "risk_points": 85},
            {"label": "Never share credentials or sensitive info in chat", "value": "NO", "risk_points": 0},
            {"label": "Occasionally share account info temporarily", "value": "SOMETIMES", "risk_points": 50}
        ],
        "tip": "Social network chats are logged on corporate servers and are susceptible to account takeover extraction."
    },

    # CATEGORY J: Digital Footprint
    {
        "id": "q39",
        "category": "CAT_FOOTPRINT",
        "text": "Do you periodically audit and delete historical public posts from previous years?",
        "options": [
            {"label": "No, all posts since account creation remain public", "value": "NO", "risk_points": 80},
            {"label": "Yes, use 'Limit Past Posts' tool or delete old content", "value": "YES", "risk_points": 0},
            {"label": "Only delete posts when specifically reminded", "value": "SOMETIMES", "risk_points": 35}
        ],
        "tip": "Limiting past posts converts years of accumulated public shares into friends-only with a single click."
    },
    {
        "id": "q40",
        "category": "CAT_FOOTPRINT",
        "text": "Do you have unused or abandoned social media profiles on platforms you no longer check?",
        "options": [
            {"label": "Yes, multiple old accounts remain active/unattended", "value": "YES", "risk_points": 75},
            {"label": "No, closed or deleted unused legacy accounts", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 40}
        ],
        "tip": "Dormant accounts have outdated passwords and no active monitoring, making them easy targets for hijacking."
    },
    {
        "id": "q41",
        "category": "CAT_FOOTPRINT",
        "text": "Have you ever searched your own name in an incognito window to inspect your public exposure?",
        "options": [
            {"label": "Never checked my public digital footprint", "value": "NO", "risk_points": 70},
            {"label": "Yes, regularly self-audit my public presence", "value": "YES", "risk_points": 0},
            {"label": "Did it once years ago", "value": "SOMETIMES", "risk_points": 30}
        ],
        "tip": "Self-auditing reveals what data brokers, employers, and OSINT investigators see about you."
    },
    {
        "id": "q42",
        "category": "CAT_FOOTPRINT",
        "text": "Do you leave public comments on news articles, viral posts, or public forum threads under your real name?",
        "options": [
            {"label": "Frequently comment on public pages", "value": "YES", "risk_points": 70},
            {"label": "Rarely or never participate in public threads", "value": "NO", "risk_points": 0},
            {"label": "Occasionally on community groups", "value": "SOMETIMES", "risk_points": 35}
        ],
        "tip": "Public comments are indexed and permanently associated with your identity across public timelines."
    }
]

# Map of question ID to question dict for fast lookup
QUESTION_MAP = {q["id"]: q for q in QUESTIONS}
