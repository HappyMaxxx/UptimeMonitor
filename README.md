# UptimeMonitor 🟢

An automated service for monitoring website availability via **HTTP** and **Ping** checks.

## Features

- 🔍 Automated periodic checks via **Celery Beat**
- 🌐 HTTP and Ping monitoring support
- 🔐 JWT authentication for secure API access
- 📊 Check history stored in PostgreSQL
- ⚡ Redis as Celery task broker
- 🗃️ Database migrations with Alembic
- 🐳 Full Docker Compose deployment

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Validation | Pydantic |
| Database | PostgreSQL |
| Migrations | Alembic |
| Task Queue | Celery + Celery Beat |
| Broker | Redis |
| HTTP Client | httpx |
| Auth | JWT |
| Deployment | Docker, Docker Compose |

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone https://github.com/HappyMaxxx/UptimeMonitor.git
cd UptimeMonitor
```

2. Create `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Fill in the environment variables in `.env`.

4. Start the services:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## API Docs

Once running, interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
UptimeMonitor/
├── app/
│   ├── api/          # Route handlers
│   ├── core/         # Config, security, dependencies
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic & monitoring tasks
│   └── main.py
├── alembic/          # Database migrations
├── tests/            # Pytest tests
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
```

## Running Tests

```bash
docker-compose exec web pytest
```

## Author

**Maksym Patyk** — [github.com/HappyMaxxx](https://github.com/HappyMaxxx)
