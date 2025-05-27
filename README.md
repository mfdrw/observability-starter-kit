# Observability Starter Kit

A self-contained playground for learning observability tools including Prometheus, Alertmanager, Grafana, and custom metric exporters. Perfect for interns and engineers new to observability.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- `curl` (for testing endpoints)
- `jq` (optional, for pretty JSON output)

### Get Started in 3 Steps

1. **Clone and start the stack**
   ```bash
   git clone <repository-url>
   cd observability-starter-kit
   docker compose up -d
   ```

2. **Wait for services to start** (about 30 seconds)

3. **Access the services**
   - **Demo App**: http://localhost:8000
   - **Prometheus**: http://localhost:9090
   - **Alertmanager**: http://localhost:9093
   - **Grafana**: http://localhost:3000 (admin/admin123)

## 📊 What's Included

### Demo Application (FastAPI)
- **Port**: 8000
- **Endpoints**:
  - `GET /` - Service information
  - `GET /ping` - Health check
  - `GET /error` - Intentionally triggers 500 errors (for testing alerts)
  - `GET /metrics` - Prometheus metrics endpoint

### Prometheus
- **Port**: 9090
- Scrapes demo app and self-monitoring metrics
- Includes pre-configured alert rules
- Data retention: 200 hours

### Alertmanager
- **Port**: 9093
- Routes alerts by severity
- Includes email and Slack webhook placeholders

### Grafana
- **Port**: 3000
- **Login**: admin / admin123
- Pre-provisioned with:
  - Prometheus datasource
  - Demo app dashboard with request rate, error rate, latency, and service status

## 🎯 Learning Exercises

### Exercise 1: Explore the Demo App
```bash
# Test the health endpoint
curl http://localhost:8000/ping

# View available endpoints
curl http://localhost:8000/

# Check raw metrics
curl http://localhost:8000/metrics
```

### Exercise 2: Trigger and Observe Alerts
```bash
# Generate some errors to trigger alerts
for i in {1..10}; do curl http://localhost:8000/error; done

# Check Prometheus alerts (wait 1-2 minutes)
open http://localhost:9090/alerts

# Check Alertmanager
open http://localhost:9093
```

### Exercise 3: Explore Grafana Dashboard
1. Open http://localhost:3000 (admin/admin123)
2. Navigate to the "Demo App Dashboard"
3. Generate traffic and watch metrics update:
   ```bash
   # Generate normal traffic
   for i in {1..50}; do curl http://localhost:8000/ping; sleep 1; done
   
   # Generate error traffic
   for i in {1..10}; do curl http://localhost:8000/error; sleep 2; done
   ```

### Exercise 4: Customize Alerts
1. Edit `prometheus/alert_rules.yml`
2. Restart Prometheus: `docker compose restart prometheus`
3. Test your new alert rules

### Exercise 5: Add Custom Metrics
1. Modify `demo_app/app/metrics.py` to add new metrics
2. Rebuild and restart: `docker compose up -d --build demo_app`
3. View new metrics in Prometheus and add to Grafana dashboard

## 🛠 Development

### Project Structure
```
observability-starter-kit/
├── compose.yaml              # Docker Compose configuration
├── demo_app/                 # FastAPI demo application
│   ├── app/
│   │   ├── main.py          # FastAPI app with endpoints
│   │   └── metrics.py       # Prometheus metrics and middleware
│   ├── Dockerfile           # Container definition
│   ├── pyproject.toml       # Python dependencies (uv)
│   └── uv.lock             # Locked dependencies
├── prometheus/
│   ├── prometheus.yml       # Prometheus configuration
│   └── alert_rules.yml      # Alert rule definitions
├── alertmanager/
│   └── alertmanager.yml     # Alertmanager configuration
└── grafana/
    ├── provisioning/        # Auto-provisioning configs
    └── dashboards_src/      # Source dashboard definitions
```

### Useful Commands

```bash
# Start the stack
docker compose up -d

# View logs
docker compose logs -f [service_name]

# Stop the stack
docker compose down

# Rebuild a specific service
docker compose up -d --build demo_app

# Check service health
docker compose ps
```

### Modifying the Demo App

The demo app uses `uv` for dependency management:

```bash
cd demo_app

# Add a new dependency
uv add <package_name>

# Run locally for development
uv run uvicorn app.main:app --reload
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file to customize settings:

```bash
# Grafana
GF_SECURITY_ADMIN_PASSWORD=your_secure_password

# Demo App
DEMO_APP_PORT=8000
```

### Customizing Alerts

Edit `alertmanager/alertmanager.yml` to configure real notification channels:

```yaml
receivers:
  - name: 'slack-alerts'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#alerts'
```

### Adding Dashboards

1. Create/modify dashboards in Grafana UI
2. Export dashboard JSON
3. Save to `grafana/dashboards_src/`
4. Copy to `grafana/provisioning/dashboards/`

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check logs for errors
docker compose logs

# Ensure ports aren't in use
netstat -tulpn | grep -E ':(3000|8000|9090|9093)'

# Clean restart
docker compose down && docker compose up -d
```

### Metrics Not Appearing
```bash
# Check if demo app is healthy
curl http://localhost:8000/ping

# Verify Prometheus can scrape targets
curl http://localhost:9090/api/v1/targets
```

### Grafana Dashboard Issues
1. Verify Prometheus datasource: http://localhost:3000/datasources
2. Check dashboard provisioning logs: `docker compose logs grafana`
3. Manually import dashboard from `grafana/dashboards_src/`

## 📚 Next Steps

- **Add More Services**: Extend with databases, message queues, etc.
- **Custom Exporters**: Write exporters for your own applications
- **Advanced Alerting**: Set up PagerDuty, OpsGenie integration
- **Log Aggregation**: Add Loki and Promtail for centralized logging
- **Distributed Tracing**: Integrate Jaeger or Tempo
- **Production Deployment**: Use Kubernetes with Helm charts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `docker compose up -d`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Observing!** 🔍📈
