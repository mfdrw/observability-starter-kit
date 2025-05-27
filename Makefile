.PHONY: help up down logs restart build clean status test

# Default target
help: ## Show this help message
	@echo "Observability Starter Kit - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

up: ## Start the observability stack
	docker compose up -d
	@echo "🚀 Stack started! Access services at:"
	@echo "  Demo App:     http://localhost:8000"
	@echo "  Prometheus:   http://localhost:9090"
	@echo "  Alertmanager: http://localhost:9093"
	@echo "  Grafana:      http://localhost:3000 (admin/admin123)"

down: ## Stop the observability stack
	docker compose down

logs: ## Show logs for all services
	docker compose logs -f

logs-demo: ## Show logs for demo app only
	docker compose logs -f demo_app

logs-prometheus: ## Show logs for Prometheus only
	docker compose logs -f prometheus

logs-grafana: ## Show logs for Grafana only
	docker compose logs -f grafana

logs-alertmanager: ## Show logs for Alertmanager only
	docker compose logs -f alertmanager

restart: ## Restart the entire stack
	docker compose restart

restart-demo: ## Restart demo app only
	docker compose restart demo_app

restart-prometheus: ## Restart Prometheus only
	docker compose restart prometheus

build: ## Rebuild and start the stack
	docker compose up -d --build

build-demo: ## Rebuild demo app only
	docker compose up -d --build demo_app

clean: ## Stop stack and remove volumes
	docker compose down -v
	docker system prune -f

status: ## Show status of all services
	docker compose ps

test: ## Run basic health checks
	@echo "🔍 Testing services..."
	@echo -n "Demo App: "
	@curl -s http://localhost:8000/ping > /dev/null && echo "✅ OK" || echo "❌ FAIL"
	@echo -n "Prometheus: "
	@curl -s http://localhost:9090/-/healthy > /dev/null && echo "✅ OK" || echo "❌ FAIL"
	@echo -n "Alertmanager: "
	@curl -s http://localhost:9093/-/healthy > /dev/null && echo "✅ OK" || echo "❌ FAIL"
	@echo -n "Grafana: "
	@curl -s http://localhost:3000/api/health > /dev/null && echo "✅ OK" || echo "❌ FAIL"

test-alerts: ## Trigger test alerts by hitting error endpoint
	@echo "🚨 Triggering test alerts..."
	@for i in $$(seq 1 10); do curl -s http://localhost:8000/error > /dev/null; done
	@echo "✅ Sent 10 error requests. Check Prometheus alerts in 1-2 minutes."

metrics: ## Show current metrics from demo app
	curl -s http://localhost:8000/metrics | grep -E "^(http_requests_total|http_errors_total|http_request_duration)"

targets: ## Show Prometheus targets status
	curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health, lastScrape: .lastScrape}'

dev-demo: ## Run demo app locally for development
	cd demo_app && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

install-dev: ## Install development dependencies
	cd demo_app && uv sync

lint-demo: ## Lint the demo app code
	cd demo_app && uv run ruff check app/

format-demo: ## Format the demo app code
	cd demo_app && uv run ruff format app/ 