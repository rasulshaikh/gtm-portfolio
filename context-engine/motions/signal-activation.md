# Motion: Signal Activation

**Source:** [ Signal Activation Playbook](https://www./workflows/signal-activation-playbook)  
**Production anchor:** `gtm-omnibound-clay-workflow`  
**Rasul:** `multi-signal`, `clay-enrichment-9step`, `gtm-plays-11`

## When to use

You have buying signals from multiple sources (CRM, intent, LinkedIn, hiring, website) and need one Clay table that scores, tiers, and routes to outbound without manual stitching.

## 11 steps (implemented)

| # | Step | Tool | Rasul repo | Gate |
|---|------|------|------------|------|
| 1 | Capture signals | Trigify, PhantomBuster, RB2B | gtm-founder-led-loop | - |
| 2 | Aggregate in Clay | Clay webhook | gtm-clay-formula-library | - |
| 3 | Normalize fields | Clay formula | gtm-clay-formula-library | - |
| 4 | Enrich contact + company | Clay + Findymail | gtm-omnibound-clay-workflow cols 7-13 | - |
| 5 | CRM lookup | HubSpot API | n8n clay-push | DNC check |
| 6 | AI qualify | Claude | gtm-ai-lead-scorer | ICP fit |
| 7 | Tier score | Clay + Rasul weights | multi-signal skill | - |
| 8 | Segment | Persona routing | gtm-email-cadences | - |
| 9 | Route to reps | Slack | n8n signal-activation | - |
| 10 | CRM sync | HubSpot | n8n clay-push | - |
| 11 | Activate | Smartlead + HeyReach | gtm-list-quality-scorecard | **B+ gate** |

## Signal to play mapping

| Signal | Rasul play | Points | Default hook |
|--------|-------------|--------|--------------|
| job-change | Play 6 Leaving Employees | 75 | signal-led |
| new-hire | Play 1 New Team Members | 30 | signal-led |
| funding | - | 45 | signal-led |
| pricing-visit | Play 10 ServiceBell Allbound | 80 | problem-sniffing |
| competitor-review | Play 8 Bad Reviews | 60 | problem-sniffing |
| content-engagement | Play 11 Inbound Followers | 30 | signal-led |

## Tier actions

| Heat | Score | Channel | SLA |
|------|-------|---------|-----|
| Red Hot | 150+ | AE manual + phone | < 1h |
| Hot | 100-149 | HeyReach 1:1 | < 24h |
| Warm | 50-99 | Smartlead personalized | < 72h |
| Cool | 20-49 | Nurture sequence | This week |

## Run

```bash
python3 context-engine/engine/route.py --motion signal-activation --signal job-change
python3 context-engine/engine/route.py --motion signal-activation --signals job-change,funding --json
```

Import n8n: `context-engine/n8n/signal-activation-pipeline.json`