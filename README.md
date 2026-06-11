# ⬡ LabPulse

Deployment tracker for self-hosted Kubernetes.  
Records every push — service, version, commit, status.

**[labpulse.alalfy.dev](https://labpulse.alalfy.dev)**

Stack: Flask, PostgreSQL 17, Docker, k3s, Traefik, GitHub Actions.

## API

```http
POST /api/deployments
X-API-Key: <your-api-key>
Content-Type: application/json

{
  "service_name": "labpulse",
  "status": "success",
  "version": "1.0.3",
  "commit_sha": "a1b2c3d",
  "message": "Add health endpoint"
}
```
