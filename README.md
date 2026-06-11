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
| CI/CD | GitHub Actions (self-hosted runner) |
| Monitoring | Prometheus + Grafana |

## Features

- Live status card per service (success / failed / running)
- Deployment history table (last 20 deployments)
- REST API for recording deployments
- Kubernetes health/readiness probes
- API key authentication

## Getting Started
To get started with LabPulse, first clone the repository.
Then, add your own secret.yaml file to LabPulse/k8s.
here is with placeholder values:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: labpulse-secret
  namespace: labpulse
type: Opaque
stringData:
  POSTGRES_PASSWORD: placeholder
  API_KEY: placeholder
```
then, add `kubectl apply -f k8s/secret.yaml` to the apply k8s manifest in LabPulse/.github/workflows/deploy.yaml to be:
```yaml
- name: Apply k8s manifests
  run: |
    kubectl apply -f k8s/namespace.yaml
    kubectl apply -f k8s/secret.yaml
    kubectl apply -f k8s/postgres.yaml
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    kubectl apply -f k8s/ingress.yaml
```
