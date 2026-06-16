# GTM Workflows - Rasul Shaikh

Workflows.io-style playbook library: 32 filterable workflows (9 production repos, ColdIQ skills, workflows.io playbooks). Deployed via GitHub Pages.

Live: https://rasulshaikh.github.io/gtm-portfolio

Built with plain HTML/CSS - no frameworks, no build step, instant load.

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
