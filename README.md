# ⬡ LabPulse

A lightweight deployment tracker for self-hosted Kubernetes clusters.
Every push to your repo is automatically recorded — giving you a live history
of what was deployed, when, and whether it succeeded.

**[labpulse.alalfy.dev](https://labpulse.alalfy.dev)**

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / Flask |
| Database | PostgreSQL 17 |
| Frontend | Jinja2 + CSS (Gruvbox theme) |
| Container | Docker |
| Orchestration | k3s |
| Ingress | Traefik |
| CI/CD | GitHub Actions (self-hosted runner |
| Monitoring | Prometheus + Grafana |

## Features

- Live status card per service (success / failed / running)
- Deployment history table (last 20 deployments)
- REST API for recording deployments
- Kubernetes health/readiness probes
- API key authentication
```
