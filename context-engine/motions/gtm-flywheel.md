# Motion: GTM Flywheel 2026

**Source:** [workflows.io GTM Flywheel Playbook](https://www.workflows.io/workflows/gtm-flywheel-playbook)  
**Production anchor:** `gtm-founder-led-loop`  
**ColdIQ:** `linkedin-content`, `cold-email`, `multi-signal`

## When to use

You need a full-funnel system: content drives traffic, traffic generates signals, signals convert through outbound, and wins feed back into content.

## 6 layers (implemented)

| Layer | workflows.io | Rasul implementation | Output |
|-------|--------------|----------------------|--------|
| 1 Traffic | Founder posts, ads, SEO | gtm-founder-led-loop/04_content_miner.py | Next post topic |
| 2 Capture | Engagers, visitors, sign-ups | gtm-founder-led-loop/01_signal_capture.py | Hot/Warm/Nurture CSV |
| 3 Nurture | Email sequences, newsletter | gtm-email-cadences/ (23 YAML) | 3-step sequences |
| 4 Conversion | Demo, trial, meeting | gtm-cold-email-personalizer | Personalized E1 |
| 5 Qualification | Score + tier | gtm-ai-lead-scorer | 0-100 score |
| 6 Retention | Deliverability, expansion | gtm-deliverability-audit | Weekly Slack report |

## Content gate (layer 1)

Before publishing 80 posts/week (NeevCloud pattern):

```bash
python3 gtm-neevcloud-content-gate/gate.py --input draft.md
```

Verdicts: PASS / FLAG / FAIL. Only PASS goes to CMS.

## Flywheel loop

```
Post (Traffic) -> Engagers captured (Capture) -> Warm outbound (Nurture)
  -> Reply/meeting (Conversion) -> Score tier (Qualification)
  -> Call transcript mined (Retention/Traffic) -> Next post
```

## Gates in flywheel

1. **Content gate** before publish (gtm-neevcloud-content-gate)
2. **List gate** before send (gtm-list-quality-scorecard, B+)
3. **Copy gate** col 60 PASS (gtm-omnibound-clay-workflow)
4. **Deliverability** weekly (gtm-deliverability-audit)

## Run

```bash
python3 context-engine/engine/route.py --motion gtm-flywheel --signal content-engagement
```