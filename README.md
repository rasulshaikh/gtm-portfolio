# GTM Workflows - Rasul Shaikh

Workflows.io-style playbook library plus **GTM Context Engine**: 3 fused motions (Signal Activation, GTM Flywheel, Product Sign-Up) routing workflows.io steps to ColdIQ skills and 9 production repos.

Live: https://rasulshaikh.github.io/gtm-portfolio

Built with plain HTML/CSS - no frameworks, no build step, instant load.

## GTM Context Engine

Fuses [workflows.io](https://www.workflows.io/workflows) playbooks with [ColdIQ GTM Skills](https://github.com/sachacoldiq/ColdIQ-s-GTM-Skills) and Rasul production repos.

```bash
python3 context-engine/engine/route.py --motion signal-activation --signal job-change
python3 context-engine/engine/route.py --motion product-signup --signals trial-signup,funding --json
```

| File | Purpose |
|------|---------|
| `context-engine/ENGINE.md` | Master agent context (read at session start) |
| `context-engine/data/gtm-context-engine.json` | Routing schema |
| `context-engine/motions/*.md` | Step-to-repo mapping per motion |
| `context-engine/n8n/signal-activation-pipeline.json` | Import-ready n8n |

Live UI: scroll to **Context Engine** on the portfolio site.

## Architecture

Full end-to-end system design: [docs/architecture.md](docs/architecture.md) (with mermaid diagrams) · [docs/architecture.pdf](docs/architecture.pdf)

## Exports

| File | Description |
|------|-------------|
| `docs/architecture.md` | Full E2E architecture with mermaid diagrams |
| `docs/architecture.pdf` | 4-page architecture PDF |
| `docs/gtm-pipeline-overview.pdf` | Condensed pipeline overview |
| `profile/gtm-profile.pdf` | 2-page GTM profile for sharing |
| `profile/gtm-profile.json` | Full profile schema (stack, repos, copy map) |
| `profile/workflow.json` | 6-phase pipeline + copy locations |
| `n8n/gtm-full-pipeline.json` | Master n8n orchestrator |

Regenerate PDFs: `python3 tools/generate_architecture_pdf.py && python3 tools/generate_play_pdfs.py`
