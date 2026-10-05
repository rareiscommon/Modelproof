"""One-shot: expand golden_dataset_v1.json to v2 with 48 new cases."""
import json
from pathlib import Path

DATA = Path("data")
V1 = DATA / "golden_dataset_v1.json"
V2 = DATA / "golden_dataset_v2.json"
MANIFEST = DATA / "manifest.json"
WORKSHEET = DATA / "verification_worksheet.md"
CREATED = "2026-10-05"

NEW = [
    # ---- BILLING (12) ----
    {"text": "We upgraded from Pro to Enterprise mid-month and were charged the full Enterprise price twice. I expected a prorated charge. Please review.",
     "category": "billing", "summary": "Customer reports duplicate full-price charge after mid-cycle upgrade and requests proration review.",
     "difficulty": "medium", "tags": ["upgrade", "proration", "duplicate charge"]},
    {"text": "I cancelled my subscription on the 1st but was still billed on the 5th. Can you refund that charge?",
     "category": "billing", "summary": "Customer reports charge after cancellation and requests refund.",
     "difficulty": "easy", "tags": ["cancellation", "refund"]},
    {"text": "My card was declined for this month's invoice. It works everywhere else. Can you check what's going on?",
     "category": "billing", "summary": "Customer reports card decline on invoice despite valid card elsewhere.",
     "difficulty": "medium", "tags": ["payment", "decline"]},
    {"text": "Can you re-issue invoice INV-2048 with our updated VAT number? The current one won't clear our finance department.",
     "category": "billing", "summary": "Customer requests invoice re-issue with updated VAT number for finance approval.",
     "difficulty": "easy", "tags": ["invoice", "vat", "reissue"]},
    {"text": "I'm being charged in USD but my account is set to EUR. The conversion fee is eating my margin. How do I switch billing currency?",
     "category": "billing", "summary": "Customer requests billing currency change from USD to EUR.",
     "difficulty": "medium", "tags": ["currency", "billing"]},
    {"text": "We paid for the annual plan upfront in March but have only used it for two months. Are partial refunds available for unused time?",
     "category": "billing", "summary": "Customer requests partial refund for unused annual plan time.",
     "difficulty": "medium", "tags": ["refund", "annual plan"]},
    {"text": "I see three invoices for the same month on my account. That can't be right. Can someone look?",
     "category": "billing", "summary": "Customer reports multiple invoices for the same billing period.",
     "difficulty": "easy", "tags": ["invoice", "duplicate"]},
    {"text": "My free trial converted to a paid plan without any email warning. I'd like to cancel and refund that first charge.",
     "category": "billing", "summary": "Customer reports trial auto-converted without notice and requests refund.",
     "difficulty": "medium", "tags": ["trial", "refund", "auto-charge"]},
    {"text": "I applied promo code SAVE20 at checkout but was charged full price. Can you apply the discount retroactively?",
     "category": "billing", "summary": "Customer reports promo code not applied and requests retroactive discount.",
     "difficulty": "easy", "tags": ["promo code", "discount"]},
    {"text": "I accidentally opened a chargeback with my bank. Please cancel it and just bill me normally. Sorry for the hassle.",
     "category": "billing", "summary": "Customer requests cancellation of mistakenly filed chargeback.",
     "difficulty": "hard", "tags": ["chargeback", "billing"]},
    {"text": "Our billing contact left the company. How do we update who receives invoices?",
     "category": "billing", "summary": "Customer requests invoice recipient change after staff departure.",
     "difficulty": "easy", "tags": ["billing contact", "invoices"]},
    {"text": "The amount on my statement doesn't match what the dashboard shows I owe. Off by about $40. Which is correct?",
     "category": "billing", "summary": "Customer reports discrepancy between statement and dashboard billing amounts.",
     "difficulty": "medium", "tags": ["discrepancy", "statement"]},
    # ---- TECHNICAL (12) ----
    {"text": "Our integration started hitting rate limits at 4pm today. We haven't changed anything. Did you lower the limits?",
     "category": "technical", "summary": "Customer reports sudden API rate limit changes without configuration change.",
     "difficulty": "medium", "tags": ["api", "rate limit"]},
    {"text": "Webhooks stopped firing around 2am UTC. Our logs show nothing received for six hours. Any known issues?",
     "category": "technical", "summary": "Customer reports webhook delivery stopped unexpectedly overnight.",
     "difficulty": "hard", "tags": ["webhook", "delivery"]},
    {"text": "The dashboard takes 15-20 seconds to load each page today. Yesterday it was instant. Is something wrong?",
     "category": "technical", "summary": "Customer reports severe dashboard performance degradation.",
     "difficulty": "medium", "tags": ["performance", "dashboard"]},
    {"text": "Large file uploads (over 50MB) are timing out. Smaller files work fine. This is blocking our monthly data import.",
     "category": "technical", "summary": "Customer reports upload timeouts for files over 50MB.",
     "difficulty": "medium", "tags": ["upload", "timeout"]},
    {"text": "Login redirects in a loop between /login and /dashboard. Clearing cookies didn't help.",
     "category": "technical", "summary": "Customer reports login redirect loop persisting after cookie clear.",
     "difficulty": "medium", "tags": ["login", "redirect"]},
    {"text": "Search is returning results from last week instead of today's data. Indexing delay?",
     "category": "technical", "summary": "Customer reports stale search results suggesting indexing delay.",
     "difficulty": "easy", "tags": ["search", "indexing"]},
    {"text": "The iOS app crashes immediately on launch after the latest update. iPhone 15, iOS 18.3.",
     "category": "technical", "summary": "Customer reports iOS app crash on launch after recent update.",
     "difficulty": "easy", "tags": ["mobile", "crash"]},
    {"text": "Slack integration stopped posting notifications about three hours ago. The connection shows as active on our end.",
     "category": "technical", "summary": "Customer reports Slack integration not posting notifications despite active connection.",
     "difficulty": "medium", "tags": ["slack", "integration"]},
    {"text": "I'm not receiving 2FA codes by SMS. Tried three times over the last hour. Can you check delivery logs?",
     "category": "technical", "summary": "Customer reports SMS 2FA codes not being delivered.",
     "difficulty": "medium", "tags": ["2fa", "sms"]},
    {"text": "Data export from our 200k record account times out after 5 minutes. Needs to work for our compliance audit next week.",
     "category": "technical", "summary": "Customer reports data export timeout on large account ahead of compliance audit.",
     "difficulty": "hard", "tags": ["export", "timeout", "compliance"]},
    {"text": "CSV import is silently dropping rows with special characters in the name column. About 5% of each file goes missing.",
     "category": "technical", "summary": "Customer reports CSV import dropping rows with special characters.",
     "difficulty": "hard", "tags": ["csv", "import", "data loss"]},
    {"text": "Emails from your system are landing in our spam folder. Can you check SPF/DKIM on your sending domain?",
     "category": "technical", "summary": "Customer reports delivery emails routed to spam, requests SPF/DKIM check.",
     "difficulty": "medium", "tags": ["email", "deliverability"]},
    # ---- ACCOUNT (12) ----
    {"text": "My password reset email never arrives. I've tried three times and checked spam.",
     "category": "account", "summary": "Customer reports password reset emails not arriving despite retries.",
     "difficulty": "easy", "tags": ["password reset"]},
    {"text": "I need to change my account email from an old work address I no longer have access to.",
     "category": "account", "summary": "Customer requests account email change away from inaccessible old address.",
     "difficulty": "medium", "tags": ["email change"]},
    {"text": "Please delete my account and all associated data. I'm moving to a competitor.",
     "category": "account", "summary": "Customer requests account and data deletion.",
     "difficulty": "easy", "tags": ["deletion", "gdpr"]},
    {"text": "The account owner has left the company. How do we transfer ownership to me?",
     "category": "account", "summary": "Customer requests account ownership transfer after owner departure.",
     "difficulty": "medium", "tags": ["ownership", "transfer"]},
    {"text": "We have two accounts from an old acquisition. Can they be merged into one with consolidated billing?",
     "category": "account", "summary": "Customer requests account merge with consolidated billing.",
     "difficulty": "hard", "tags": ["merge", "acquisition"]},
    {"text": "I'm trying to add three new team members but the invite button is greyed out. We're on the Team plan.",
     "category": "account", "summary": "Customer reports team invite button disabled on Team plan.",
     "difficulty": "medium", "tags": ["team", "invite"]},
    {"text": "How do I update the company name and billing address on file? The current details are wrong.",
     "category": "account", "summary": "Customer requests company name and billing address update.",
     "difficulty": "easy", "tags": ["billing info", "update"]},
    {"text": "We want to enable SSO with Okta for our whole org. What's the setup process?",
     "category": "account", "summary": "Customer requests SSO setup process for Okta integration.",
     "difficulty": "medium", "tags": ["sso", "okta"]},
    {"text": "A user needs to be promoted to admin but only sees Member in the role dropdown. Plan limitation or bug?",
     "category": "account", "summary": "Customer reports role dropdown missing admin option for user.",
     "difficulty": "medium", "tags": ["roles", "permissions"]},
    {"text": "My account got locked after several failed logins. I'm the only admin. How do I recover access?",
     "category": "account", "summary": "Customer requests account unlock and recovery as sole admin.",
     "difficulty": "hard", "tags": ["locked", "recovery", "admin"]},
    {"text": "Profile picture uploads fail with a generic error. Tried PNG, JPG, under 1MB. Same result.",
     "category": "account", "summary": "Customer reports profile picture upload failures across formats.",
     "difficulty": "easy", "tags": ["profile", "upload"]},
    {"text": "A former employee deleted their account but we need to recover their data for a legal hold.",
     "category": "account", "summary": "Customer requests account data recovery for legal hold after deletion.",
     "difficulty": "hard", "tags": ["deletion", "legal hold", "recovery"]},
    # ---- GENERAL (12) ----
    {"text": "Do you offer discounted pricing for registered non-profits? We're a small environmental charity.",
     "category": "general", "summary": "Customer inquires about non-profit pricing.",
     "difficulty": "easy", "tags": ["pricing", "nonprofit"]},
    {"text": "We're a 500-person company evaluating platforms. Can we get a call with someone on your enterprise team?",
     "category": "general", "summary": "Prospect requests enterprise sales contact for evaluation.",
     "difficulty": "easy", "tags": ["enterprise", "sales"]},
    {"text": "Feature request: it would be great if scheduled reports could be exported to Google Sheets directly.",
     "category": "general", "summary": "Customer requests Google Sheets export for scheduled reports.",
     "difficulty": "easy", "tags": ["feature request"]},
    {"text": "We run a complementary analytics tool and would like to explore a partnership. Who should I talk to?",
     "category": "general", "summary": "Company proposes partnership and requests contact.",
     "difficulty": "medium", "tags": ["partnership"]},
    {"text": "Is there a Postman collection for your API? The docs are good but a collection would speed up our onboarding.",
     "category": "general", "summary": "Customer requests Postman collection for API onboarding.",
     "difficulty": "easy", "tags": ["api", "docs"]},
    {"text": "Small typo on the /webhooks page: \"occured\" should be \"occurred\". Flagging in case it's helpful.",
     "category": "general", "summary": "Customer reports documentation typo on webhooks page.",
     "difficulty": "easy", "tags": ["docs", "typo"]},
    {"text": "Just wanted to say your support team resolved my last ticket in 20 minutes. Best experience I've had with any SaaS. Keep it up.",
     "category": "general", "summary": "Customer sends positive feedback about support response time.",
     "difficulty": "easy", "tags": ["feedback", "positive"]},
    {"text": "I'm a journalist writing about AI evaluation tooling for The Register. Can I get a quote or a briefing?",
     "category": "general", "summary": "Journalist requests quote or briefing for article.",
     "difficulty": "medium", "tags": ["press", "media"]},
    {"text": "Our security team needs your latest SOC 2 report and pen test summary. Where can I find them?",
     "category": "general", "summary": "Customer requests SOC 2 report and pen test summary for security review.",
     "difficulty": "medium", "tags": ["security", "compliance", "soc2"]},
    {"text": "Is your platform HIPAA compliant? We're a healthcare startup and need to know before signing.",
     "category": "general", "summary": "Prospect inquires about HIPAA compliance before purchase.",
     "difficulty": "medium", "tags": ["compliance", "hipaa", "healthcare"]},
    {"text": "I'd love to join the beta for your new evaluation features. How do I get on the list?",
     "category": "general", "summary": "Customer requests access to beta program for new features.",
     "difficulty": "easy", "tags": ["beta", "early access"]},
    {"text": "Do you have a bug bounty program? I found an edge case in your API sandbox that might be worth reporting.",
     "category": "general", "summary": "Researcher inquires about bug bounty program and reports API edge case.",
     "difficulty": "medium", "tags": ["security", "bug bounty"]},
]

def main():
    v1 = json.loads(V1.read_text())
    assert isinstance(v1, list), "v1 must be a list"
    assert len(v1) == 15, f"expected 15 v1 cases, got {len(v1)}"

    v1_ids = {c["id"] for c in v1}
    next_id = 16
    v2 = list(v1)
    for case in NEW:
        cid = f"gd-{next_id:04d}"
        next_id += 1
        v2.append({
            "id": cid,
            "text": case["text"],
            "category": case["category"],
            "summary": case["summary"],
            "difficulty": case["difficulty"],
            "tags": case["tags"],
            "source": "ai-drafted",
            "verified": "pending",
            "verified_by": "",
            "created": CREATED,
            "notes": "",
        })

    V2.write_text(json.dumps(v2, indent=2) + "\n")

    counts = {}
    for c in v2:
        counts[c["category"]] = counts.get(c["category"], 0) + 1
    diff = {}
    for c in v2:
        diff[c["difficulty"]] = diff.get(c["difficulty"], 0) + 1

    m = json.loads(MANIFEST.read_text())
    m["version_id"] = "v2"
    m["parent_version"] = "v1"
    m["num_cases"] = len(v2)
    m["num_verified"] = 15
    m["categories_counts"] = counts
    m["difficulty_counts"] = diff
    m["generation_date"] = CREATED
    m["generation_notes"] = "48 cases ai-drafted on 2026-10-05; human verification pending"
    MANIFEST.write_text(json.dumps(m, indent=2) + "\n")

    lines = [
        "# Golden Dataset v2 - Verification Worksheet",
        "",
        f"Total cases: {len(v2)} (15 carried from v1, 48 new)",
        "",
        "Mark `verified` as `yes` for cases you have reviewed and approved.",
        "",
        "| id | category | difficulty | verified | summary | notes |",
        "|----|----------|------------|----------|---------|-------|",
    ]
    for c in v2:
        verified = "yes (v1 carryover)" if c["id"] in v1_ids else "no"
        summ = c["summary"].replace("|", "\\|")
        lines.append(f"| {c['id']} | {c['category']} | {c['difficulty']} | {verified} | {summ} | |")
    WORKSHEET.write_text("\n".join(lines) + "\n")

    print(f"Wrote {V2} ({len(v2)} cases)")
    print(f"Wrote {MANIFEST}")
    print(f"Wrote {WORKSHEET}")
    print(f"Category counts: {counts}")
    print(f"Difficulty counts: {diff}")

if __name__ == "__main__":
    main()
