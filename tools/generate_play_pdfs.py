#!/usr/bin/env python3
"""Generate PDF play guides for GTM repos."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen.canvas import Canvas

NAVY = HexColor("#0f1f38")
BLUE = HexColor("#2563eb")
ACCENT = HexColor("#06b6d4")
GRAY = HexColor("#64748b")
LIGHT = HexColor("#f8fafc")
TEXT = HexColor("#0f172a")
W, H = letter

PLAYS = {
    "deliverability-audit": {
        "out": Path(__file__).parent.parent.parent / "gtm-deliverability-audit/docs/play-guide.pdf",
        "title": "Deliverability Audit",
        "subtitle": "SPF · DKIM · DMARC · Smartlead · 1% Reply Rule",
        "sections": [
            ("What it checks", "DNS authentication on every sending domain. Smartlead inbox health: warmup status, SMTP/IMAP, blocks. Campaign performance: reply rate and bounce rate per campaign. Flags anything below 1% reply after 200+ sends."),
            ("Commands", "python audit.py domains --domains send1.co,send2.co --out ./audit\npython audit.py full --out ./audit  # needs SMARTLEAD_API_KEY"),
            ("Output files", "auth.csv — per-domain SPF/DKIM/DMARC scores\ninboxes.csv — fleet health\nperformance.csv — campaign metrics with flags\nreport.md — action items"),
            ("n8n workflow", "Import n8n/weekly-deliverability-audit.json. Runs every Monday. Pulls Smartlead inboxes, checks DNS via Google DNS API, flags low-reply campaigns, posts summary to Slack."),
            ("When to run", "Reply rate drops >30% week-over-week. Bounces spike above 2%. Before scaling volume. Monthly hygiene. Taking over a new Smartlead account."),
        ],
    },
    "list-quality-scorecard": {
        "out": Path(__file__).parent.parent.parent / "gtm-list-quality-scorecard/docs/play-guide.pdf",
        "title": "List Quality Scorecard",
        "subtitle": "Pre-Send Grading · 8 Dimensions · A+ to F",
        "sections": [
            ("What it grades", "Email verification coverage. Duplicate emails and domains. Title relevance vs ICP. Bad-title patterns (intern, assistant). Catch-all density (info@, contact@). ICP fit on industry + headcount. Name quality."),
            ("Commands", "python scorecard.py --list leads.csv --out scorecard.md\npython scorecard.py --list leads.csv --icp-file client-profile.yaml --json scorecard.json"),
            ("Grade mapping", "A/A+ (90+): Ship it. B (80-89): Minor fixes then ship. C (70-79): Fix top 3 issues. D (60-69): Serious cleanup. F (<60): Rebuild the list."),
            ("n8n workflow", "Import n8n/pre-send-list-gate.json. Webhook receives leads from Clay export. Scores list in-code. Grade B+ routes to Smartlead push. Grade C or below blocks send and alerts Slack."),
            ("Pipeline position", "Run AFTER email enrichment, BEFORE Smartlead upload. Pair with gtm-deliverability-audit for post-send health."),
        ],
    },
    "omnibound-clay-workflow": {
        "out": Path(__file__).parent.parent.parent / "gtm-omnibound-clay-workflow/docs/play-guide.pdf",
        "title": "Omnibound Clay Workflow",
        "subtitle": "60 Columns · Purple-Safe · 144 Email Variants",
        "sections": [
            ("The flow", "Intel → Citation → News → Email waterfall → Context → PS lines → Routing → Persona → Copy → Validator → Export to Smartlead + HeyReach."),
            ("Key columns", "Col 8 intel: competitive research. Col 14-26 citation: live AI search proof. Col 51 persona: executive/director/general. Col 52-59 copy: hash-seeded variants. Col 60 validator: 12-check PASS/FAIL gate."),
            ("Purple safety", "Layer 1: extraction filters strip purple sentinel. Layer 2: copy guards return empty if fields missing. Layer 3: validator blocks export. Filter validator = PASS only."),
            ("n8n workflows", "clay-push-pipeline.json — webhook from Clay, HMAC verify, HubSpot upsert, route by tier to Smartlead/HeyReach.\nretry-failed-pushes.json — cron every 30min, retries failed pushes from Google Sheet."),
            ("Cost", "~12-18 Clay credits/row. ~6,000-10,000 credits for 500 prospects."),
        ],
    },
    "gtm-pipeline": {
        "out": Path(__file__).parent.parent / "docs/gtm-pipeline-overview.pdf",
        "title": "GTM Signal-to-Pipeline",
        "subtitle": "Full Motion · 8 Repos · n8n Orchestration",
        "sections": [
            ("6-phase workflow", "1. Capture signal (PhantomBuster, HeyReach). 2. Enrich (Apollo, Clay, Deepline). 3. Score & route (gtm-ai-lead-scorer). 4. Personalize (MiniMax cadences, Clay formulas). 5. Send (Smartlead, HeyReach). 6. Mine & loop (founder-led-loop)."),
            ("Pre-send gate", "gtm-list-quality-scorecard grades list A+ to F. n8n pre-send-list-gate.json blocks upload below grade B."),
            ("Production copy", "23 cadences (gtm-email-cadences). 60-col Omnibound Clay workflow. 6 Clay IIFE formulas. Warm outbound via founder-led-loop."),
            ("Post-send health", "gtm-deliverability-audit weekly via n8n. 1% reply rule. SPF/DKIM/DMARC checks."),
            ("n8n master workflow", "Import n8n/gtm-full-pipeline.json. Clay webhook → list gate → tier routing → Smartlead/HeyReach → failure logging → retry loop."),
            ("All repos", "gtm-portfolio · gtm-ai-lead-scorer · gtm-cold-email-personalizer · gtm-clay-formula-library · gtm-email-cadences · gtm-founder-led-loop · gtm-deliverability-audit · gtm-list-quality-scorecard · gtm-omnibound-clay-workflow"),
        ],
    },
}


def wrap(text, width=88):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if len(test) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_pdf(path: Path, title: str, subtitle: str, sections: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = Canvas(str(path), pagesize=letter)
    c.setFillColor(NAVY)
    c.rect(0, H - 120, W, 120, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, H - 123, W, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(48, H - 50, title)
    c.setFillColor(HexColor("#ffffff99"))
    c.setFont("Helvetica", 11)
    c.drawString(48, H - 72, subtitle)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(48, H - 100, "GTM PLAY GUIDE  ·  RASUL SHAIKH  ·  2026")

    y = H - 150
    for label, body in sections:
        if y < 100:
            c.showPage()
            y = H - 60
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(48, y, label.upper())
        c.setStrokeColor(ACCENT)
        c.line(48, y - 4, 564, y - 4)
        y -= 20
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 10)
        for line in body.split("\n"):
            for wrapped in wrap(line, 90):
                if y < 60:
                    c.showPage()
                    y = H - 60
                c.drawString(48, y, wrapped)
                y -= 14
        y -= 8

    c.save()
    print(f"Generated {path}")


def main():
    for play in PLAYS.values():
        draw_pdf(play["out"], play["title"], play["subtitle"], play["sections"])


if __name__ == "__main__":
    main()