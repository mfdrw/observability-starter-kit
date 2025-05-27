# Observability Starter Kit – Project Plan

> **Purpose**: Provide interns with a self-contained playground consisting of a FastAPI demo application, Prometheus, Alertmanager and Grafana – all runnable with a single `docker compose up` command.  
> This document breaks the work down into clear, bite-sized tasks so another engineer can pick it up without additional context.

---

## 1. High-Level Objectives

1. Containerise a small FastAPI application that exposes custom Prometheus metrics.
2. Deploy Prometheus to scrape the demo app (and itself) and forward alerts to Alertmanager.
3. Deploy Alertmanager with a basic routing/receiver configuration.
4. Deploy Grafana pre-seeded with:
   * Prometheus datasource
   * A starter dashboard visualising demo-app metrics
5. Provide out-of-the-box alert rules (e.g. HTTP 500 error rate) that fire and appear in Alertmanager & Grafana.
6. Ship concise documentation so interns can:
   * Spin the stack up/down quickly
   * Trigger sample alerts & explore dashboards

---

## 2. Deliverables

* `compose.yaml` (Docker Compose v2 syntax)
* `demo_app/` directory with FastAPI source, Dockerfile, and Python dependency files (`pyproject.toml`, `uv.lock`) managed by `uv`
* `prometheus/prometheus.yml` and `prometheus/alert_rules.yml`
* `alertmanager/alertmanager.yml`
* `grafana/provisioning/**` with datasource & dashboard provisioning files
* Sample dashboard JSON (`grafana/dashboards_src/demo_dashboard.json`)
* `.env.example` holding default credentials
* **README.md** with quick-start & learning exercises
* (Optional) CI workflow that performs a smoke test

---

## 3. Milestones & Task Breakdown

Below is a checklist grouped by milestone.  
Each task specifies a suggested owner, effort estimate and blocking dependencies.

### 3.1  Project Bootstrap

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| B-1 | Initialise git repo, commit this `project.md`, create `main` branch | 0.5 |  | — |
| B-2 | Add `.gitignore` (Python, Docker, VS Code) | 0.2 |  | B-1 |
| B-3 | Create directory scaffold as outlined in README | 0.5 |  | B-1 |

### 3.2  Demo Application (`demo_app`)

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| A-1 | Initialise `uv` project: create `pyproject.toml` (+ `uv lock`) with dependencies `fastapi`, `uvicorn[standard]`, `prometheus_client` | 0.2 |  | B-3 |
| A-2 | Implement `app/main.py` with `GET /ping` & `GET /error` routes | 1.0 |  | A-1 |
| A-3 | Implement `app/metrics.py` with custom counters/histograms + middleware | 1.0 |  | A-2 |
| A-4 | Build `Dockerfile` (python-slim base, install `uv` & sync deps, expose 8000) | 0.5 |  | A-3 |
| A-5 | Local test: `docker build` + `curl /ping` | 0.3 |  | A-4 |

### 3.3  Prometheus Configuration

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| P-1 | Author `prometheus/prometheus.yml` with scrape configs | 0.8 |  | B-3 |
| P-2 | Create `prometheus/alert_rules.yml` with high-error-rate alert | 0.5 |  | P-1 |
| P-3 | Validate config via `prom/prometheus --config.file` local run | 0.3 |  | P-2 |

### 3.4  Alertmanager Configuration

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| AM-1 | Write minimal `alertmanager/alertmanager.yml` with default route | 0.5 |  | B-3 |
| AM-2 | (Optional) Add email/Slack receiver placeholders | 0.3 |  | AM-1 |

### 3.5  Grafana Provisioning

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| G-1 | Create datasource file `grafana/provisioning/datasources/prometheus_ds.yml` | 0.3 |  | B-3, P-1 |
| G-2 | Build initial dashboard in running Grafana, export JSON | 1.5 |  | G-1 |
| G-3 | Check dashboard into `grafana/dashboards_src/` & reference via provisioning | 0.4 |  | G-2 |

### 3.6  Docker Compose Integration

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| C-1 | Draft `compose.yaml` with four services + network | 1.0 |  | A-4, P-1, AM-1, G-1 |
| C-2 | Implement bind-mounts for all config files | 0.4 |  | C-1 |
| C-3 | Spin up stack, verify:
  • Prometheus targets healthy
  • Grafana datasource connected
  • Alert fires on `/error` traffic | 1.0 |  | C-2 |

### 3.7  Documentation & Developer UX

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| D-1 | Write `README.md` with install, quick-start & exercises | 1.0 |  | C-3 |
| D-2 | Create `.env.example` (Grafana admin password, etc.) | 0.2 |  | D-1 |
| D-3 | Add Makefile helpers (`make up`, `make down`, `make logs`) | 0.5 |  | C-3 |

### 3.8  Quality Assurance & CI (Optional)

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| QA-1 | Write smoke test script hitting `/ping` & Prometheus API | 0.8 |  | C-3 |
| QA-2 | Add GitHub Actions workflow to build & test stack | 1.0 |  | QA-1 |

### 3.9  Project Close-Out

| ID | Task | Est. hrs | Owner | Depends on |
|----|------|----------|-------|------------|
| H-1 | Final code review & tidy up | 0.5 |  | All |
| H-2 | Tag v1.0 release, push Docker images (optional) | 0.3 |  | H-1 |
| H-3 | Handover meeting / knowledge transfer | 0.5 |  | H-2 |

---

## 4. Estimated Timeline (person-days)

| Milestone | Total hrs | ≈ Days (8 h) |
|-----------|-----------|--------------|
| Bootstrap | 1.2 | 0.2 |
| Demo App | 3.0 | 0.4 |
| Prometheus | 1.6 | 0.2 |
| Alertmanager | 0.8 | 0.1 |
| Grafana | 2.2 | 0.3 |
| Compose & Verification | 2.4 | 0.3 |
| Docs & UX | 1.7 | 0.2 |
| QA & CI | 1.8 | 0.2 |
| Buffer & Close-Out | 1.3 | 0.2 |
| **Total** | **16.0 h** | **~2 days** |

---

## 5. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Docker image version drift | Stack fails months later | Pin image tags & document upgrade path |
| Grafana dashboard export becomes stale | Broken provisioning | Document "how to update dashboard" procedure |
| Alert routing secrets checked in | Security breach | Use `.env` / `secrets` instead of hard-coding receivers |

---

## 6. Next Steps for Future Enhancements (Backlog)

* Add Loki + Promtail for log aggregation.
* Add Tempo or Jaeger for distributed tracing.
* Create Terraform / Helm charts for Kubernetes deployment.
* Publish tutorial labs for interns (e.g. "write your own exporter").

---

*Document generated 2025-05-27.* 