# Motion: Product Sign-Up Outreach

**Source:** [ Product Sign-Up Playbook](https://www./workflows/product-sign-up-outreach-playbook)  
**Production anchor:** `gtm-ai-lead-scorer`  
**Rasul:** `multi-signal`, `clay-enrichment-9step`

## When to use

PLG motion: product form submissions, trial sign-ups, or demo requests need enrichment, ICP scoring, CRM sync, and tiered outreach within SLA.

## 7 steps (implemented)

| # | Step | Implementation |
|---|------|----------------|
| 1 | Clay webhook on signup | Clay table trigger |
| 2 | Enrich contact | Findymail + LinkedIn (clay-enrichment-9step) |
| 3 | Classify email type | gtm-clay-formula-library work/personal classifier |
| 4 | Enrich company | Clay firmographics |
| 5 | Lead scoring tiers | gtm-ai-lead-scorer (0-100) |
| 6 | HubSpot sync | n8n HubSpot create/update |
| 7 | Tiered outreach | HeyReach T1, Instantly T2/T3 |

## Tier routing

| Tier | Score | Channel | Copy hook | SLA |
|------|-------|---------|-----------|-----|
| 1 | 80-100 | HeyReach 1:1 | problem-sniffing | 24h |
| 2 | 50-79 | Instantly personalized | billboard | 72h |
| 3 | 0-49 | Instantly nurture | billboard | 7d |

## Email type handling

| Type | Action |
|------|--------|
| Work email | Full enrich + score + outreach |
| Role email (info@, sales@) | Find decision-maker first |
| Personal email | Lower tier default, LinkedIn fallback |

## Gates

Run `gtm-list-quality-scorecard` before any Instantly upload. Trial sign-ups with score 100+ skip to Red Hot SLA (< 1h AE).

## Run

```bash
python3 context-engine/engine/route.py --motion product-signup --signal trial-signup --json
```