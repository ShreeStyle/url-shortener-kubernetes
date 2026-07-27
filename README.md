# URL Shortener on Kubernetes

A production-inspired DevOps project demonstrating containerization, orchestration, monitoring, and CI/CD using Flask and PostgreSQL.

---

## Tech Stack

- Python (Flask)
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- Kubernetes
- Prometheus
- Grafana
- Jenkins
- GitHub Actions (optional)

---

## Architecture

```
                 User
                   │
                   ▼
              Browser
                   │
                   ▼
          Kubernetes Service
                   │
        ┌──────────┴──────────┐
        │                     │
    Flask Pod 1          Flask Pod 2
        │                     │
        └──────────┬──────────┘
                   │
          PostgreSQL Service
                   │
             PostgreSQL Pod
```

---

## Features

- URL Shortening
- URL Redirection
- Click Tracking
- PostgreSQL Database
- Dockerized Application
- Kubernetes Deployment
- Health Checks
- Prometheus Metrics
- Kubernetes Secrets
- Load Balancing
- Rolling Updates

---

## Project Structure

```text
app/
database/
kubernetes/
monitoring/
jenkins/
screenshots/
```

---

## Docker

Build

```bash
docker build -t url-shortener .
```

Run

```bash
docker compose up -d
```

---

## Kubernetes

Create Namespace

```bash
kubectl apply -f kubernetes/namespace.yaml
```

Deploy Database

```bash
kubectl apply -f kubernetes/postgres-secret.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml
```

Deploy Application

```bash
kubectl apply -f kubernetes/app-deployment.yaml
kubectl apply -f kubernetes/app-service.yaml
```

Check Pods

```bash
kubectl get pods -n url-shortener
```

---

## Monitoring

Prometheus scrapes metrics from

```
/metrics
```

Available metrics include

- shortened_urls_total
- redirect_requests_total

---

## Screenshots

### Application

(Add Screenshot)

### Kubernetes Pods

(Add Screenshot)

### PostgreSQL

(Add Screenshot)

### Prometheus

(Add Screenshot)

### Grafana

(Add Screenshot)

---

## Learning Outcomes

- Docker Image Creation
- Docker Compose
- Kubernetes Deployments
- Kubernetes Services
- Kubernetes Secrets
- Readiness Probes
- Liveness Probes
- Prometheus Monitoring
- CI/CD Pipeline using Jenkins

---

## Future Improvements

- Ingress Controller
- Persistent Volume
- ConfigMap
- Flask-Migrate
- Horizontal Pod Autoscaler
- Helm Charts