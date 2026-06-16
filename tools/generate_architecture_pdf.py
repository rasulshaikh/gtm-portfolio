#!/usr/bin/env python3
"""Generate architecture.pdf from architecture.md content."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen.canvas import Canvas

OUT = Path(__file__).parent.parent / "docs" / "architecture.pdf"

NAVY = HexColor("#0f1f38")
BLUE = HexColor("#2563eb")
ACCENT = HexColor("#06b6d4")
GRAY = HexColor("#64748b")
TEXT = HexColor("#0f172a")
W, H = letter

PAGES = [
    {
        "title": "GTM Signal-to-Pipeline",
        "subtitle": "End-to-End Architecture · 8 Repos · 5 n8n Workflows",
        "sections": [
            ("Overview", "Two signal paths converge into one send pipeline. QA gates before and after outbound. Content loop compounds at the end. Signal in → enrich → score → personalize → list gate (B+) → n8n → Smartlead/HeyReach/HubSpot → weekly audit → mine calls → loop restarts."),
            ("8 phases", "1. Capture Signal - LinkedIn engagers, funding, hiring (PhantomBuster, HeyReach, Trigify)\n2. Enrich - Apollo, Clay, Prospeo, Deepline\n3. Score & Route - gtm-ai-lead-scorer + founder-led-loop/02 → Hot/Warm/Nurture\n4. Personalize - MiniMax hooks, 23 cadences, 60-col Omnibound Clay\n5. Pre-Send Gate - list scorecard grade B+ required\n6. Send - Smartlead + HeyReach + HubSpot via n8n\n7. Post-Send Health - deliverability audit, 1% reply rule\n8. Mine & Loop - content_miner.py → next post"),
        ],
    },
    {
        "title": "Motion A - Omnibound Clay",
        "subtitle": "60 Columns · Purple-Safe · 144 Email Variants",
        "sections": [
            ("Clay flow", "Inputs (6) → Intel (7-13) → Citation (14-26) → News (27-33) → Email waterfall (34-40) → Context+PS (41-47) → Persona (51) → Copy (52-59) → Validator (60 PASS only) → n8n push."),
            ("Purple safety", "Layer 1: extraction filters strip purple sentinel. Layer 2: copy guards return empty if fields missing. Layer 3: validator 12-check gate. Export filter: validator = PASS."),
            ("n8n", "clay-push-pipeline.json - HMAC webhook, HubSpot upsert, tier routing to Smartlead/HeyReach.\nretry-failed-pushes.json - cron 30min, retries from Google Sheet."),
            ("Repo", "github.com/rasulshaikh/gtm-omnibound-clay-workflow"),
        ],
    },
    {
        "title": "Motion B + C + n8n",
        "subtitle": "Founder Loop · Cold Cadences · Orchestration",
        "sections": [
            ("Founder-led loop", "Publish post → 01_signal_capture → enrich → 02_score_route (Hot 80+/Warm 50-79/Nurture <50) → 03_outbound MiniMax warm copy → calls → 04_content_miner → next post. Repo: gtm-founder-led-loop"),
            ("Cold cadences", "23 YAML sequences: 8 signal, 7 persona, 4 vertical, 4 stage. cadence_runner.py + MiniMax-Text-01 hooks. Repo: gtm-email-cadences"),
            ("n8n orchestration", "1. pre-send-list-gate.json - blocks below grade B\n2. clay-push-pipeline.json - tier routing\n3. retry-failed-pushes.json - 30min cron\n4. weekly-deliverability-audit.json - Monday SPF/DMARC + 1% rule\n5. gtm-full-pipeline.json - master orchestrator"),
            ("All 8 repos", "gtm-portfolio · gtm-omnibound-clay-workflow · gtm-email-cadences · gtm-founder-led-loop · gtm-ai-lead-scorer · gtm-clay-formula-library · gtm-list-quality-scorecard · gtm-deliverability-audit"),
        ],
    },
    {
        "title": "Copy Map + QA Gates",
        "subtitle": "Where Copy Lives · Pre/Post-Send Checks",
        "sections": [
            ("Copy locations", "Production sequences: Omnibound cols 52-59 (Claygent)\n23 cadences: gtm-email-cadences/cadences/ (MiniMax hooks)\nWarm outbound: founder-led-loop/03_outbound.py (MiniMax)\nSingle-lead: gtm-cold-email-personalizer (Claude+Playwright)\nScoring: gtm-ai-lead-scorer (Claude Haiku)\nFormulas: gtm-clay-formula-library (6 IIFEs)"),
            ("Pre-send gate", "gtm-list-quality-scorecard - 8 dimensions. Verification, duplicates, titles, catch-all, ICP fit, names. Grade B+ required. n8n pre-send-list-gate.json blocks bad lists."),
            ("Post-send health", "gtm-deliverability-audit - SPF/DKIM/DMARC per domain. 1% reply rule after 200 sends. Bounce >3% flag. Weekly n8n cron → Slack."),
            ("Downloads", "docs/architecture.pdf · docs/gtm-pipeline-overview.pdf · profile/gtm-profile.pdf · profile/gtm-profile.json · profile/workflow.json · n8n/gtm-full-pipeline.json"),
        ],
    },
]


def wrap(text, width=88):
    lines, cur = [], ""
    for word in text.split():
        test = f"{cur} {word}".strip()
        if len(test) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_page(c, page_num, total, title, subtitle, sections):
    c.setFillColor(NAVY)
    c.rect(0, H - 110, W, 110, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, H - 113, W, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(48, H - 48, title)
    c.setFillColor(HexColor("#ffffff99"))
    c.setFont("Helvetica", 10)
    c.drawString(48, H - 68, subtitle)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(48, H - 92, f"ARCHITECTURE  ·  PAGE {page_num}/{total}  ·  RASUL SHAIKH  ·  2026")

    y = H - 135
    for label, body in sections:
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(48, y, label.upper())
        c.setStrokeColor(ACCENT)
        c.line(48, y - 4, 564, y - 4)
        y -= 18
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 9.5)
        for line in body.split("\n"):
            for wrapped in wrap(line, 92):
                c.drawString(48, y, wrapped)
                y -= 13
        y -= 6


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = Canvas(str(OUT), pagesize=letter)
    total = len(PAGES)
    for i, page in enumerate(PAGES, 1):
        if i > 1:
            c.showPage()
        draw_page(c, i, total, page["title"], page["subtitle"], page["sections"])
    c.save()
    print(f"Generated {OUT}")


if __name__ == "__main__":
    main()