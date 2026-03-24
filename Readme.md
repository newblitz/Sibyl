# 🚨 Supply Chain Disruption Intelligence

> Real-time supplier risk monitoring — detects geopolitical events, weather anomalies, and port disruptions before they hit your business.

![Status](https://img.shields.io/badge/status-in%20progress-orange)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Celery](https://img.shields.io/badge/Celery-5.3-37814A?logo=celery)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)

---

## 🧠 The Problem

Modern businesses depend on complex supplier networks they can't see. A port closure in Rotterdam, a typhoon in Taiwan, a geopolitical escalation in the Red Sea — these events take weeks to surface as delivery delays. By then, it's too late.

**Supply Chain Disruption Intelligence** monitors news, weather, shipping traffic, and social signals in real-time, maps events to your specific suppliers using NLP entity extraction, scores disruption severity, and pushes alerts to your dashboard before the impact reaches you.

---

## ✨ Features

- **Multi-source real-time pipeline** — ingests NewsAPI, Open-Meteo weather, MarineTraffic port data, and Twitter/X signals via Celery beat scheduling
- **LLM-powered entity extraction** — uses spaCy NER + Claude API to map raw news events to specific supplier nodes in your supply graph
- **Graph-based risk architecture** — PostgreSQL recursive CTEs model supplier → port → geography relationships with multi-hop traversal
- **Disruption severity scoring** — XGBoost model trained on historical supply chain events, outputs 0–100 risk score with confidence band
- **Real-time alert dashboard** — WebSocket push via Django Channels delivers ranked alerts within 1–5 seconds of event ingestion
- **Historical backtesting** — validate model accuracy against past disruptions (Suez Canal 2021, COVID port closures, Red Sea 2024)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Data Sources                          │
│  NewsAPI  │  Open-Meteo  │  MarineTraffic  │  Twitter/X  │
└─────────────────────────┬───────────────────────────────┘
                          │ Celery Beat (scheduled polling)
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Ingestion Pipeline                      │
│  Fetch → Deduplicate (Redis) → Normalize → Store        │
│                   RawEvent table                        │
└─────────────────────────┬───────────────────────────────┘
                          │ Celery task: process_raw_events
                          ▼
┌─────────────────────────────────────────────────────────┐
│              NLP Entity Extraction                       │
│  spaCy NER → extract orgs, locations, ports             │
│  Claude API → map entities to supplier nodes            │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│           PostgreSQL Risk Graph                          │
│  Supplier ──ships_through──► Port                       │
│  Port     ──located_in────► Geography                   │
│  Recursive CTE traversal: event → affected suppliers    │
└─────────────────────────┬───────────────────────────────┘
                          │ XGBoost severity scorer
                          ▼
┌─────────────────────────────────────────────────────────┐
│           Django Channels WebSocket Push                 │
│  Alert fired → broadcast to subscribed dashboard users  │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              React Dashboard                             │
│  Live alert feed │ Risk map │ Supplier graph view        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework |
| Async tasks | Celery 5.3 + Redis 7 |
| Real-time | Django Channels 4 + Daphne (WebSockets) |
| Database | PostgreSQL 15 (graph via recursive CTEs) |
| NLP | spaCy, Claude API (entity extraction) |
| ML | XGBoost, scikit-learn (severity scoring) |
| Frontend | React 18 + Vite, Zustand, Recharts |
| Data sources | NewsAPI, Open-Meteo, MarineTraffic, Twitter/X API |
| DevOps | Docker, Docker Compose |

---

## 📁 Project Structure

```
supply-chain-intelligence/
├── apps/
│   ├── pipeline/              # Multi-source ingestion
│   │   ├── sources/
│   │   │   ├── news.py        # NewsAPI fetcher
│   │   │   ├── weather.py     # Open-Meteo fetcher
│   │   │   ├── shipping.py    # MarineTraffic fetcher
│   │   │   └── twitter.py     # Twitter/X fetcher
│   │   ├── models.py          # RawEvent, DataSourceLog
│   │   ├── tasks.py           # Celery beat tasks
│   │   └── dedup.py           # Redis deduplication
│   ├── graph/                 # Supplier risk graph
│   │   ├── models.py          # Supplier, Port, Geography, SupplyEdge
│   │   └── traversal.py       # Recursive CTE queries
│   ├── scoring/               # Disruption severity
│   │   ├── model.py           # XGBoost scorer
│   │   └── backtesting.py     # Historical validation
│   └── alerts/                # Alert engine + WS push
│       ├── consumers.py       # Django Channels consumer
│       └── tasks.py           # Alert generation tasks
├── frontend/                  # React 18 + Vite
│   └── src/
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   └── SupplierGraph.jsx
│       └── hooks/
│           └── useAlerts.js   # WebSocket hook
├── config/
│   ├── settings/
│   ├── celery.py
│   └── asgi.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- NewsAPI key → [newsapi.org](https://newsapi.org)
- Open-Meteo (free, no key needed)
- MarineTraffic API key → [marinetraffic.com](https://marinetraffic.com)
- Twitter/X Bearer Token → [developer.twitter.com](https://developer.twitter.com)
- Anthropic API key → [console.anthropic.com](https://console.anthropic.com)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/supply-chain-intelligence.git
cd supply-chain-intelligence

# 2. Copy environment variables
cp .env.example .env

# 3. Fill in your API keys in .env
nano .env

# 4. Build and start all services
docker-compose up --build

# 5. Run migrations
docker-compose exec backend python manage.py migrate

# 6. Seed sample supplier data
docker-compose exec backend python manage.py seed_suppliers

# 7. Start the pipeline manually (or let Celery beat handle it)
docker-compose exec backend python manage.py trigger_pipeline
```

### Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/supplychain

# Redis
REDIS_URL=redis://redis:6379/0

# API Keys
NEWS_API_KEY=your-newsapi-key
MARINETRAFFIC_API_KEY=your-marinetraffic-key
TWITTER_BEARER_TOKEN=your-twitter-bearer-token
ANTHROPIC_API_KEY=your-anthropic-key

# Open-Meteo (no key required)
```

---

## 🔄 Pipeline Flow

The pipeline runs on a Celery beat schedule. Each source has its own polling interval:

| Source | Interval | What it fetches |
|---|---|---|
| NewsAPI | Every 15 min | Headlines filtered by supply chain keywords |
| Open-Meteo | Every 1 hour | Extreme weather alerts at supplier locations |
| MarineTraffic | Every 30 min | Port congestion, vessel delays, route changes |
| Twitter/X | Every 10 min | Real-time signals from logistics accounts |

Events are deduplicated via Redis (SHA-256 hash of source URL + headline) before hitting the database — prevents duplicate alerts from the same event appearing across sources.

---

## 📊 Risk Scoring

Each event is scored 0–100 for disruption severity by an XGBoost model trained on historical supply chain disruptions:

| Score | Severity | Example |
|---|---|---|
| 0–25 | Low | Minor weather delay, small port slowdown |
| 26–50 | Moderate | Regional strike, localized flooding |
| 51–75 | High | Major port closure, geopolitical escalation |
| 76–100 | Critical | Suez-level blockage, pandemic-scale disruption |

**Features used:** event type, affected geography, commodity category, season, historical disruption frequency at that location, concurrent events in same region.

---

## 🗂️ API Endpoints

```
GET  /api/events/              # Paginated raw events feed
GET  /api/events/?source=news  # Filter by source
GET  /api/alerts/              # Generated alerts, ordered by severity
GET  /api/suppliers/           # Your supplier nodes
POST /api/suppliers/           # Add a supplier
GET  /api/suppliers/{id}/risk/ # Current risk score + active alerts
GET  /api/graph/traverse/?supplier_id=1  # Graph traversal from supplier
WS   /ws/alerts/               # WebSocket — live alert push
```

---

## 🧪 Running Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run pipeline tests only
docker-compose exec backend pytest apps/pipeline/tests/ -v

# Run with coverage
docker-compose exec backend pytest --cov=apps --cov-report=html
```

---

## 🗺️ Roadmap

- [x] Multi-source ingestion pipeline (NewsAPI, Open-Meteo, MarineTraffic, Twitter/X)
- [x] Redis deduplication layer
- [x] PostgreSQL supplier graph with recursive CTE traversal
- [x] spaCy NER + Claude API entity extraction
- [ ] XGBoost severity scoring model (in progress)
- [ ] WebSocket real-time alert dashboard (in progress)
- [ ] Historical backtesting on 2020–2024 disruption data
- [ ] React dashboard with supplier graph visualisation
- [ ] PDF disruption report export
- [ ] Multi-tenant support (each company sees only their supplier graph)

---

## 🤝 Contributing

This project is under active development. Issues and PRs welcome.

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Run tests before pushing
pytest

# Submit a PR with a clear description of what changed and why
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.


> ⭐ Star this repo if you found it useful!