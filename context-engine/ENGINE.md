# GTM Context Engine

**Owner:** Rasul Shaikh. All implementations run on production repos at github.com/rasulshaikh.  and Rasul provide structural inspiration; schemas, n8n, and generators live here.

Read this file at the start of any GTM session. It routes you to the right motion, Signal skill, Rasul repo, and copy framework.

## How routing works

```
Input:  motion + optional signal type
Output: steps + signal_skill + rasul_repo + tier_action + copy_hook + n8n_webhook
```

1. Pick a **motion** (signal-activation | gtm-flywheel | product-signup)
2. Optionally pass a **signal** (job-change, funding, website-visitor, trial-signup, etc.)
3. Engine returns a context bundle with executable steps, not external links

CLI: `python3 context-engine/engine/route.py --motion signal-activation --signal job-change`

## Motions

| Motion | Source playbook | Rasul anchor repo | When to use |
|--------|-----------------|-------------------|-------------|
| signal-activation | Signal Activation | gtm-omnibound-clay-workflow | Buying signals from CRM, intent, content, hiring |
| gtm-flywheel | GTM Flywheel 2026 | gtm-founder-led-loop | Full-funnel: traffic to retention |
| product-signup | Product Sign-Up | gtm-ai-lead-scorer | PLG sign-ups, trial starts, demo requests |
| outbound-attribution | Outbound Attribution | gtm-omnibound-clay-workflow | CRM attribution, silent conversions, channel reporting |
| cold-outreach-message | Rasul (inspired by ) | gtm-cold-email-personalizer | E1 copy: first line, body, CTA, P.S., 80-word gate |

Read the motion file in `motions/` before executing.

## Heat tiers (Multi-signal)

| Score | Heat | SLA | Channel | Owner |
|-------|------|-----|---------|-------|
| 150+ | Red Hot | < 1 hour | Manual + phone | AE |
| 100-149 | Hot | < 24 hours | HeyReach + personalized email | SDR |
| 50-99 | Warm | < 72 hours | Smartlead sequence + SDR monitor | SDR |
| 20-49 | Cool | This week | Nurture + content | Marketing |
| 0-19 | Cold | Ongoing | Monitor only | System |

3+ stacked signals target 35-40% reply rate vs 6-8% cold.

## Gates (always run before send)

1. **List gate** - `gtm-list-quality-scorecard` - grade B+ required
2. **Copy gate** - Omnibound col 60 PASS or campaign-copywriting 4-step
3. **Content gate** - `gtm-neevcloud-content-gate` - PASS/FLAG/FAIL for content motions

## Copy framework hooks

| Hook | When | Example opener |
|------|------|----------------|
| Signal-Led | Recent news, hiring, funding | "Post-raise, pipeline velocity matters..." |
| Problem Sniffing | Observable gap or audit data | "I asked ChatGPT [keyword] and you ranked 15th..." |
| Billboard | Clear offer, limited data | "We help customers reach their entire TAM every two months." |

Signal motions default to **Signal-Led**. Product signup uses **Problem Sniffing** for Tier 1, **Billboard** for Tier 2/3.

## Production repos (run order)

| Step type | Repo | Script |
|-----------|------|--------|
| Signal capture | gtm-founder-led-loop | `01_signal_capture.py` |
| AI scoring | gtm-ai-lead-scorer | `score_lead.py` |
| List gate | gtm-list-quality-scorecard | `scorecard.py` |
| Copy assembly | gtm-omnibound-clay-workflow | Clay cols 52-59 |
| Cadences | gtm-email-cadences | YAML variants |
| Clay formulas | gtm-clay-formula-library | IIFE exports |
| Send | n8n clay-push | `clay-push-pipeline.json` |
| Content QA | gtm-neevcloud-content-gate | `gate.py` |
| Health | gtm-deliverability-audit | weekly cron |

## Signal skill routing

When a signal is present, invoke the matching sub-skill from `signal/skill-router.json`:

- job-change -> job-changes
- funding -> funding
- hiring -> hiring
- website-visitor -> website-visitors
- tech-change -> tech-changes
- content-engagement -> content-engagement
- competitor -> competitor-signals
- multi (2+ signals) -> multi-signal

For play selection, see `signal/plays-index.json` (11 GTM plays).

## n8n entrypoints

| Motion | Webhook path | JSON |
|--------|--------------|------|
| signal-activation | `/webhook/gtm-signal-activation` | `n8n/signal-activation-pipeline.json` |
| full pipeline | `/webhook/gtm-pipeline-entry` | `n8n/gtm-full-pipeline.json` |

## Session checklist

1. Read `ENGINE.md` (this file)
2. Run `route.py` for your motion + signal
3. Read the motion markdown in `motions/`
4. Invoke the returned Signal skill if signal-specific copy is needed
5. Run gates before any send
6. Log tier and SLA in CRM

*Last updated: 2026-06-16*