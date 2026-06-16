#!/usr/bin/env python3
"""Generate 3 GTM case study PDFs using reportlab."""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUT_DIR = Path(__file__).parent

NAVY = HexColor("#0f1f38")
NAVY_LIGHT = HexColor("#1b3a5c")
BLUE = HexColor("#2563eb")
ACCENT = HexColor("#06b6d4")
GRAY = HexColor("#64748b")
LIGHT = HexColor("#f8fafc")
BORDER = HexColor("#e2e8f0")
TEXT = HexColor("#0f172a")

W, H = letter  # 612 x 792

def draw_page_bg(c):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_header_bar(c, company, title, subtitle=""):
    c.setFillColor(NAVY)
    c.rect(0, H - 160, W, 160, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, H - 163, W, 3, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff33"))
    c.setFont("Helvetica", 9)
    c.drawString(48, H - 30, company.upper())
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(48, H - 65, title)
    if subtitle:
        c.setFillColor(HexColor("#ffffff99"))
        c.setFont("Helvetica", 12)
        c.drawString(48, H - 90, subtitle)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(48, H - 140, "CASE STUDY  ·  RASUL SHAIKH  ·  GTM ENGINEER")

def draw_metrics_bar(c, metrics, y=580):
    cols = len(metrics)
    col_w = (W - 96) / cols
    c.setFillColor(LIGHT)
    c.roundRect(48, y, W - 96, 72, 8, fill=1, stroke=0)
    c.setStrokeColor(BORDER)
    c.setLineWidth(1)
    c.roundRect(48, y, W - 96, 72, 8, fill=0, stroke=1)
    for i, (val, label) in enumerate(metrics):
        x = 48 + i * col_w + col_w / 2
        if i > 0:
            c.setStrokeColor(BORDER)
            c.setLineWidth(1)
            c.line(48 + i * col_w, y + 12, 48 + i * col_w, y + 60)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x, y + 38, val)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(x, y + 22, label.upper())

def draw_section_label(c, label, y):
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(48, y, label.upper())
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.5)
    c.line(48, y - 4, 564, y - 4)

def draw_body_text(c, text, y, max_width=516, font_size=10.5, color=TEXT, leading=16):
    lines = []
    words = text.split()
    current = ""
    c.setFont("Helvetica", font_size)
    for word in words:
        test = (current + " " + word).strip()
        if c.stringWidth(test, "Helvetica", font_size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    c.setFillColor(color)
    for line in lines:
        c.drawString(48, y, line)
        y -= leading
    return y

def draw_bullet(c, text, y, max_width=496, indent=28):
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48, y + 1, "·")
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 10.5)
    words = text.split()
    current = ""
    lines = []
    for word in words:
        test = (current + " " + word).strip()
        if c.stringWidth(test, "Helvetica", 10.5) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for i, line in enumerate(lines):
        c.drawString(indent + 28, y, line)
        y -= 15
    return y - 3

def draw_footer(c, page_num):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff66"))
    c.setFont("Helvetica", 8)
    c.drawString(48, 13, "rasulshaikh.github.io/gtm-portfolio  ·  shaikhrasul02@gmail.com  ·  github.com/rasulshaikh")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(W - 48, 13, str(page_num))


def generate_omnibound(out_path):
    c = Canvas(str(out_path), pagesize=letter)

    # PAGE 1
    draw_page_bg(c)
    draw_header_bar(c,
        "Omnibound AI  ·  B2B SaaS",
        "Signal-to-Pipeline Engine",
        "How I built a full outbound system from scratch in 3 weeks and hit 1.5%+ reply rates at scale"
    )

    draw_metrics_bar(c, [
        ("2 Wks → 3 Days", "Deploy Time"),
        ("1.5%+", "Reply Rate"),
        ("48h → 4h", "Qualification Cycle"),
        ("6+ hrs → 30 min", "Research/Batch"),
    ], y=570)

    y = 545

    draw_section_label(c, "The Problem", y)
    y -= 22
    y = draw_body_text(c,
        "Omnibound needed to go from zero to a running outbound system - fast. No CRM data, no sequences, no enrichment pipeline. "
        "Manual research was taking 6+ hours per batch of 50 leads. Qualification required a senior rep to spend 48 hours per account. "
        "The team had no repeatable motion and no tooling to scale beyond 2 people.",
        y, leading=16)
    y -= 20

    draw_section_label(c, "The Architecture", y)
    y -= 22

    bullets_arch = [
        "Signal layer: 6 data sources unified - LinkedIn job postings, funding data, tech stack signals, news events, web traffic spikes, and intent scores - merged into a single enriched record per account.",
        "AI scoring: Claude API rubric scoring each account 0-100 on firmographic fit, technographic alignment, and behavioral signals. Accounts below 60 are automatically skipped.",
        "Clay pipeline: 7-stage LLM waterfall for hyper-personalization - company summary, pain hypothesis, relevant case study match, personalized subject line, email body v1, email body v2 variant, and objection pre-emption.",
        "Enrichment agent: Python script (Playwright + asyncio) scraping 100+ domains headlessly, scoring accounts via the Claude API rubric, and auto-pushing qualified accounts to HubSpot with full routing context.",
        "Sending infrastructure: Smartlead across 250+ sending domains with inbox rotation, warmup schedules, and reply detection feeding back into the CRM sequence stage.",
        "Qualification layer: n8n workflow parsing replies using Claude, routing positive replies to a Calendly link and flagging referrals for manual follow-up within 4 hours.",
    ]
    for b in bullets_arch:
        y = draw_bullet(c, b, y)
        y -= 4

    draw_footer(c, 1)
    c.showPage()

    # PAGE 2
    draw_page_bg(c)
    draw_header_bar(c,
        "Omnibound AI  ·  Case Study Continued",
        "Signal-to-Pipeline Engine",
        ""
    )

    y = H - 195

    draw_section_label(c, "The Results", y)
    y -= 22

    bullets_results = [
        "Reply rate: 1.5%+ sustained across 3 months and 12,000+ contacts - 3x the industry average for cold email.",
        "Deploy time: Full system (enrichment → scoring → Clay pipeline → Smartlead → CRM routing) from kick-off to first send in 3 weeks. Subsequent campaigns deploy in 3 days.",
        "Qualification speed: AI reply parsing + n8n routing cut manual qualification from 48 hours to 4 hours per positive reply.",
        "Research efficiency: Python enrichment agent replaced 6+ hours/batch of manual research with a sub-30-minute automated pass, running unattended.",
        "Pipeline generated: $3.5M+ in qualified pipeline from the system over the engagement period.",
    ]
    for b in bullets_results:
        y = draw_bullet(c, b, y)
        y -= 4

    y -= 16
    draw_section_label(c, "Key Learnings", y)
    y -= 22

    bullets_learn = [
        "Signal quality beats volume. A list of 500 accounts scored above 70 outperforms 5,000 unsegmented contacts every time.",
        "The personalization hook is the leverage point - not the email body. Getting the first line right (via Clay LLM + Playwright-scraped context) is what drives reply rates above 1%.",
        "Reply parsing is the bottleneck nobody talks about. Automating intent classification was what unlocked 4-hour qualification cycles.",
        "Infrastructure is GTM strategy. A rep working this system outperforms 3 reps without it.",
    ]
    for b in bullets_learn:
        y = draw_bullet(c, b, y)
        y -= 4

    y -= 20
    draw_section_label(c, "Stack", y)
    y -= 22
    stack_lines = [
        "Enrichment: Python (Playwright, asyncio), Supabase, Firecrawl, Prospeo",
        "AI / LLM: Claude API (scoring + copy), Claude Code (agent orchestration), OpenAI API",
        "Outbound: Clay (7-stage pipeline), Smartlead (250+ domains), HeyReach (LinkedIn)",
        "Automation: n8n (reply routing), HubSpot (CRM + routing), Webhooks",
    ]
    for line in stack_lines:
        y = draw_body_text(c, line, y, leading=15)
        y -= 3

    draw_footer(c, 2)
    c.showPage()

    c.save()
    print(f"Saved: {out_path}")


def generate_remotestate(out_path):
    c = Canvas(str(out_path), pagesize=letter)

    draw_page_bg(c)
    draw_header_bar(c,
        "RemoteState  ·  $12.2M ARR SaaS",
        "Greenfield GTM Engine",
        "How I built the entire outbound motion from zero and generated $180K+ ARR in 6 months"
    )

    draw_metrics_bar(c, [
        ("$180K+", "ARR in 6 Months"),
        ("40%", "Pipeline Efficiency Gain"),
        ("80%", "Qualification Time Cut"),
        ("1 → 4", "SDR Team Scaled"),
    ], y=570)

    y = 545

    draw_section_label(c, "The Problem", y)
    y -= 22
    y = draw_body_text(c,
        "RemoteState had $12.2M ARR and no outbound motion. All pipeline was coming from inbound and referrals. "
        "Leadership wanted to add $500K ARR in 12 months from outbound. They had zero tooling, zero sequences, and one SDR "
        "doing manual LinkedIn outreach with no system behind it. The qualification process was taking 2 full days per account.",
        y, leading=16)
    y -= 20

    draw_section_label(c, "What I Built", y)
    y -= 22

    bullets = [
        "Full sending infrastructure: 250+ sending domains across 3 inboxes per domain, warmup sequences across all, Smartlead configured with inbox rotation and daily limits that kept deliverability above 95%.",
        "Clay enrichment pipeline: Multi-source enrichment pulling from Apollo, LinkedIn, Clearbit, and web scraping. Custom OpenAI lead-scoring rubric ranking accounts by ICP fit before any human touches the list.",
        "SDR playbooks: Built sequence templates, objection handling guides, and reply classification rules that let the SDR team operate without hand-holding. Onboarded 3 new SDRs in week 4 using the same system.",
        "CRM architecture: HubSpot configured with custom deal stages, sequence-aware contact properties, and automated routing based on reply intent (Claude API parsing positive/negative/referral).",
        "Demand gen layer: LinkedIn Ads running retargeting to website visitors who matched the ICP. Google Ads capturing bottom-funnel search terms. Both feeding into the same HubSpot pipeline.",
        "Reporting: Weekly pipeline velocity dashboard showing reply rate, qualified pipeline per SDR, sequence performance by variant, and cost per SQL.",
    ]
    for b in bullets:
        y = draw_bullet(c, b, y)
        y -= 4

    draw_footer(c, 1)
    c.showPage()

    draw_page_bg(c)
    draw_header_bar(c,
        "RemoteState  ·  Case Study Continued",
        "Greenfield GTM Engine", ""
    )

    y = H - 195

    draw_section_label(c, "The Results", y)
    y -= 22

    results = [
        "$180K+ ARR generated from outbound in 6 months - on a $0 outbound budget at the start of the engagement.",
        "40% improvement in pipeline efficiency: the same number of leads produced more qualified opportunities after the scoring rubric filtered the list.",
        "80% reduction in qualification time: from 2 days to 4 hours per account, driven by AI reply parsing and automated routing.",
        "SDR team scaled 1 → 4 in 8 weeks using documented playbooks. New reps were productive in week 1 because the system did the heavy lifting.",
        "Inbound-to-outbound ratio shifted from 90/10 to 65/35 within 6 months - the outbound channel was generating nearly a third of all new pipeline.",
    ]
    for b in results:
        y = draw_bullet(c, b, y)
        y -= 4

    y -= 16
    draw_section_label(c, "Key Learnings", y)
    y -= 22

    learns = [
        "Infrastructure first, headcount second. Adding SDRs to a broken system produces mediocre results. Fixing the system first, then scaling headcount, compounds.",
        "Scoring before sending is not optional at scale. Without a rubric, SDRs spend 60% of their time on accounts that will never buy.",
        "Deliverability is a full-time job. 250+ domains sounds like overkill until you see what happens to reply rates when you skip warmup.",
        "The playbook is the asset, not the rep. A well-documented system means any competent rep can operate at senior-rep performance within a week.",
    ]
    for b in learns:
        y = draw_bullet(c, b, y)
        y -= 4

    y -= 20
    draw_section_label(c, "Stack", y)
    y -= 22
    stack_lines = [
        "Outbound: Clay, Smartlead (250+ domains), Apollo, HeyReach",
        "AI: OpenAI API (lead scoring rubric), Claude API (reply classification)",
        "CRM / Automation: HubSpot, n8n, Webhooks",
        "Demand Gen: LinkedIn Ads, Google Ads API, GA4, SEMrush",
    ]
    for line in stack_lines:
        y = draw_body_text(c, line, y, leading=15)
        y -= 3

    draw_footer(c, 2)
    c.showPage()
    c.save()
    print(f"Saved: {out_path}")


def generate_falconwise(out_path):
    c = Canvas(str(out_path), pagesize=letter)

    draw_page_bg(c)
    draw_header_bar(c,
        "FalconWise Tech  ·  Cybersecurity  ·  Dubai, UAE",
        "Zero-to-One MENA ABM Engine",
        "How I built enterprise ABM from scratch in the MENA cybersecurity market and hit 10+ SQLs/month"
    )

    draw_metrics_bar(c, [
        ("10+ SQLs/mo", "From Zero"),
        ("30%", "Avg Engagement Rate"),
        ("25%", "Pipeline from Partners"),
        ("3", "Co-Marketing Channels"),
    ], y=570)

    y = 545

    draw_section_label(c, "The Problem", y)
    y -= 22
    y = draw_body_text(c,
        "FalconWise Tech was selling enterprise cybersecurity solutions in the MENA market - UAE, Saudi Arabia, Egypt - "
        "with no outbound motion and no brand awareness outside of a few warm referrals. The enterprise sales cycle "
        "was 90+ days and required multi-stakeholder buy-in (CISO, IT Director, CFO). There was no ABM program, "
        "no content targeting enterprise buyers, and no partner channel. Starting from zero in a high-trust, "
        "relationship-driven market is the hardest possible starting point.",
        y, leading=16)
    y -= 20

    draw_section_label(c, "The ABM Architecture", y)
    y -= 22

    bullets = [
        "Account selection: Built a target account list of 180 enterprise organizations across UAE, KSA, and Egypt using Apollo + LinkedIn Sales Nav, filtered by employee count (500+), industry (BFSI, government, healthcare, telecom), and known cybersecurity spend signals.",
        "Multi-source enrichment: Clay pipeline pulling from LinkedIn, company websites, news sources, and procurement portals to identify buying signals - budget cycles, regulatory compliance deadlines, recent breaches, and executive changes.",
        "Persona mapping: Identified and enriched 3 buyer personas per account - CISO (economic buyer), IT Director (technical champion), and CFO (budget approver) - with personalized messaging for each.",
        "Co-marketing: Partnered with 3 regional cybersecurity vendors (non-competing) for joint webinars, co-authored whitepapers, and shared event sponsorships - pipeline from partners reached 25% of total within 4 months.",
        "LinkedIn Ads ABM: Targeted the account list + personas with LinkedIn matched audiences. Used engagement retargeting to serve case study content to accounts that had visited the website.",
        "Outbound sequences: Multi-touch sequences per persona: cold email (Clay-personalized) → LinkedIn connection → LinkedIn voice note → email follow-up with content asset. Sequences ran in Arabic and English.",
    ]
    for b in bullets:
        y = draw_bullet(c, b, y)
        y -= 4

    draw_footer(c, 1)
    c.showPage()

    draw_page_bg(c)
    draw_header_bar(c,
        "FalconWise Tech  ·  Case Study Continued",
        "Zero-to-One MENA ABM Engine", ""
    )

    y = H - 195

    draw_section_label(c, "The Results", y)
    y -= 22

    results = [
        "10+ SQLs per month within 5 months of building the program from scratch - pipeline previously averaged 1-2 inbound SQLs per month.",
        "30% average engagement rate across ABM content sequences - driven by Arabic-language personalization and region-specific regulatory framing (UAE NESA, Saudi Arabia NCA compliance).",
        "25% of pipeline sourced from the partner co-marketing channel within 4 months of launching the first joint webinar.",
        "3 strategic co-marketing partnerships closed with regional cybersecurity vendors, generating shared pipeline and joint content assets.",
        "Enterprise sales cycle reduced from 90+ days average to 60 days through earlier stakeholder mapping and multi-threaded outreach.",
    ]
    for b in results:
        y = draw_bullet(c, b, y)
        y -= 4

    y -= 16
    draw_section_label(c, "MENA-Specific GTM Notes", y)
    y -= 22

    learns = [
        "Language matters more than expected. Arabic-language email openings - even when the full email is English - increased reply rates by 40% with Arabic-speaking decision-makers.",
        "Regulatory triggers are the strongest signal in MENA. Framing outreach around UAE NESA, NCA, or SAMA compliance deadlines created urgency that standard pain-point messaging didn't.",
        "Relationship before pitch. MENA enterprise buyers expect 2-3 touchpoints of value delivery before a product conversation. The co-marketing model front-loaded this.",
        "LinkedIn penetration in MENA enterprise is higher than expected - especially in UAE. LinkedIn outreach worked better than cold email as the first touch in this market.",
    ]
    for b in learns:
        y = draw_bullet(c, b, y)
        y -= 4

    y -= 20
    draw_section_label(c, "Stack", y)
    y -= 22
    stack_lines = [
        "ABM / Enrichment: Clay, Apollo, LinkedIn Sales Navigator, Firecrawl",
        "Outbound: Instantly (cold email), HeyReach (LinkedIn), Trigify (signals)",
        "Advertising: LinkedIn Ads (matched audiences + retargeting), Meta Ads",
        "CRM / Reporting: HubSpot, n8n, Google Data Studio",
    ]
    for line in stack_lines:
        y = draw_body_text(c, line, y, leading=15)
        y -= 3

    draw_footer(c, 2)
    c.showPage()
    c.save()
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    cs_dir = OUT_DIR
    cs_dir.mkdir(exist_ok=True)

    generate_omnibound(cs_dir / "omnibound-signal-to-pipeline.pdf")
    generate_remotestate(cs_dir / "remotestate-gtm-engine.pdf")
    generate_falconwise(cs_dir / "falconwise-mena-abm.pdf")

    print("\nAll 3 case studies generated.")
