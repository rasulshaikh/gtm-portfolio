#!/usr/bin/env python3
"""Generate GTM profile PDF from gtm-profile.json."""

import json
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen.canvas import Canvas

OUT = Path(__file__).parent / "gtm-profile.pdf"
DATA = Path(__file__).parent / "gtm-profile.json"

NAVY = HexColor("#0f1f38")
BLUE = HexColor("#2563eb")
ACCENT = HexColor("#06b6d4")
GRAY = HexColor("#64748b")
LIGHT = HexColor("#f8fafc")
TEXT = HexColor("#0f172a")
W, H = letter


def wrap_text(text, max_chars=90):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_header(c, title, subtitle=""):
    c.setFillColor(NAVY)
    c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, H - 133, W, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(48, H - 55, title)
    if subtitle:
        c.setFillColor(HexColor("#ffffff99"))
        c.setFont("Helvetica", 11)
        c.drawString(48, H - 78, subtitle)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(48, H - 110, "GTM PROFILE  ·  RASUL SHAIKH  ·  2026")


def draw_section(c, label, y):
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(48, y, label.upper())
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.5)
    c.line(48, y - 4, 564, y - 4)
    return y - 22


def draw_body(c, text, y, size=10, color=TEXT, leading=14):
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    for line in wrap_text(text, 88):
        c.drawString(48, y, line)
        y -= leading
    return y - 6


def draw_bullets(c, items, y, leading=13):
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 9.5)
    for item in items:
        c.drawString(56, y, f"•  {item}")
        y -= leading
    return y - 4


def page1(c, data):
    draw_header(c, data["name"], f"{data['title']}  ·  {data['location']}")
    y = H - 170
    y = draw_section(c, "Headline", y)
    y = draw_body(c, data["headline"], y)

    y = draw_section(c, "Key Metrics", y)
    metrics = data["metrics"]
    cols = [
        (metrics["revenue_generated"], "Revenue"),
        (metrics["pipeline_generated"], "Pipeline"),
        (metrics["deploy_time_improvement"], "Deploy Time"),
        (metrics["reply_rate"], "Reply Rate"),
        (metrics["qualification_time"], "Qualification"),
    ]
    col_w = (W - 96) / len(cols)
    c.setFillColor(LIGHT)
    c.roundRect(48, y - 58, W - 96, 58, 6, fill=1, stroke=0)
    for i, (val, label) in enumerate(cols):
        x = 48 + i * col_w + col_w / 2
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x, y - 22, val)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x, y - 38, label.upper())
    y -= 78

    y = draw_section(c, "Tech Stack", y)
    for group, tools in data["tech_stack"].items():
        label = group.replace("_", " ").title()
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(48, y, label)
        y -= 13
        y = draw_body(c, " · ".join(tools), y, size=9, color=GRAY, leading=12)
        y -= 2

    y = draw_section(c, "Contact", y)
    y = draw_body(c, f"Email: {data['email']}", y, size=10)
    y = draw_body(c, f"Portfolio: {data['links']['portfolio']}", y, size=9, color=GRAY)
    y = draw_body(c, f"GitHub: {data['links']['github']}", y, size=9, color=GRAY)
    y = draw_body(c, f"LinkedIn: {data['links']['linkedin']}", y, size=9, color=GRAY)


def page2(c, data):
    draw_header(c, "Workflow & Copy Library", "Signal-to-Pipeline Engine")
    y = H - 160

    y = draw_section(c, "6-Phase Workflow", y)
    for phase in data["workflow"]["phases"]:
        line = f"{phase['id']}. {phase['name']} — {', '.join(phase['tools'])} → {phase['output']}"
        y = draw_body(c, line, y, size=9, leading=12)

    y -= 4
    y = draw_section(c, "Where the Copy Lives", y)
    for key, lib in data["copy_library"].items():
        title = key.replace("_", " ").title()
        repo = lib.get("repo", "")
        path = lib.get("path", "")
        count = lib.get("count", "")
        engine = lib.get("personalization_engine", lib.get("description", ""))
        line = f"{title}: {repo}/{path}"
        if count:
            line += f" ({count} files)"
        y = draw_body(c, line, y, size=9, leading=12)
        if engine:
            y = draw_body(c, f"   Engine: {engine}", y, size=8.5, color=GRAY, leading=11)

    y = draw_section(c, "Open Source Repos", y)
    for repo in data["open_source_repos"]:
        y = draw_body(c, f"• {repo['name']}: {repo['description']}", y, size=9, leading=12)

    y = draw_section(c, "Case Studies", y)
    for cs in data["case_studies"]:
        metrics = " · ".join(f"{k}: {v}" for k, v in cs["metrics"].items())
        y = draw_body(c, f"{cs['company']} — {cs['title']}", y, size=9.5, leading=12)
        y = draw_body(c, f"   {metrics}", y, size=8.5, color=GRAY, leading=11)


def main():
    data = json.loads(DATA.read_text())
    c = Canvas(str(OUT), pagesize=letter)
    page1(c, data)
    c.showPage()
    page2(c, data)
    c.save()
    print(f"Generated {OUT}")


if __name__ == "__main__":
    main()