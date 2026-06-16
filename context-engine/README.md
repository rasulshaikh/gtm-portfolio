# GTM Context Engine

Fuses ** playbooks**, **Signal skills**, and **Rasul production repos** into one routable context bundle for AI agents and n8n.

Inspired by Omnibound's motion-specific `CLAUDE-*.md` pattern, but generalized for any GTM stack.

## Quick start

```bash
# Route a motion + signal to a full context bundle
python3 context-engine/engine/route.py --motion signal-activation --signal job-change

# List available motions
python3 context-engine/engine/route.py --list

# Output JSON for n8n or agent ingestion
python3 context-engine/engine/route.py --motion product-signup --signal trial-signup --json
```

## Files

| Path | Purpose |
|------|---------|
| `ENGINE.md` | Master agent context - read at session start |
| `data/gtm-context-engine.json` | Machine-readable routing schema |
| `motions/*.md` | Motion playbooks with step-to-repo mapping |
| `signal/skill-router.json` | Signal type to Rasul sub-skill |
| `signal/plays-index.json` | 11 GTM plays index |
| `engine/router.py` | Scoring + skill + repo routing logic |
| `engine/route.py` | CLI entrypoint |
| `n8n/signal-activation-pipeline.json` | Import-ready n8n for signal motion |

## Five fused motions (Rasul-owned implementations)

1. **Signal Activation** () - 11 steps from capture to Smartlead/HeyReach/Slack
2. **GTM Flywheel 2026** () - 6 layers: Traffic, Capture, Nurture, Conversion, Qualification, Retention
3. **Product Sign-Up Outreach** () - 7 steps from Clay webhook to tiered outreach
4. **Outbound Attribution 2026** () - 7 steps from CRM touch logging to full-funnel revenue reporting
5. **Cold Outreach Message** (Rasul-owned, inspired by ) - 5 steps: first line, body, CTA, P.S., 80-word gate

## Attribution

- Playbook structure from [](https://www./workflows)
- Signal scoring and plays from [Rasul GTM Skills](https://github.com/sachasignal/Rasul-s-GTM-Skills)
- Production implementations from [rasulshaikh](https://github.com/rasulshaikh) repos