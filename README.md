# ForgeCI

ForgeCI is a work-in-progress continuous integration platform built to explore the systems behind modern CI/CD infrastructure.

The project currently receives authenticated GitHub webhook events, identifies the exact repository, branch, and commit associated with a push, and connects to PostgreSQL for persistent build-state storage. The long-term goal is to evolve this into a distributed CI system with queued jobs, concurrent workers, isolated Docker execution, failure recovery, and GitHub status reporting.

## Current Status

ForgeCI is under active development.

Currently implemented:

- FastAPI backend with health-check endpoint
- GitHub webhook ingestion
- Real GitHub push event handling
- GitHub webhook signature verification using HMAC-SHA256
- GitHub event-type filtering
- Repository, branch, and commit SHA extraction
- Automated API and webhook security tests with pytest
- PostgreSQL database setup
- SQLAlchemy + psycopg database connectivity
- Environment-based secret and database configuration
- Local webhook development through an HTTPS tunnel

Current automated test coverage includes:

- Health endpoint
- Valid GitHub webhook signatures
- Missing webhook signatures
- Invalid webhook signatures
- Non-push GitHub event handling

## Architecture

Current request flow:

```text
Developer
   |
   | git push
   v
GitHub
   |
   | signed webhook
   v
ForgeCI FastAPI API
   |
   |-- verify X-Hub-Signature-256
   |-- identify GitHub event type
   |-- extract repository
   |-- extract commit SHA
   |-- extract branch
   |
   v
PostgreSQL
```

Planned architecture:

```text
GitHub Push
    |
    v
ForgeCI API
    |
    v
PostgreSQL Build Record
    |
    v
Redis Job Queue
    |
    +------------+------------+
    |            |            |
    v            v            v
 Worker 1     Worker 2     Worker N
    |            |            |
    +------------+------------+
                 |
                 v
          Docker Containers
                 |
                 v
          Run Repository Tests
                 |
                 v
       Store Build/Test Results
                 |
                 v
          GitHub Checks API
```

## Tech Stack

**Backend**
- Python 3.12
- FastAPI
- Uvicorn

**Database**
- PostgreSQL
- SQLAlchemy
- psycopg

**Testing**
- pytest
- FastAPI TestClient

**Integrations**
- GitHub Webhooks
- HMAC-SHA256 webhook authentication
- ngrok for local webhook development

**Planned**
- Redis
- Docker / Docker Compose
- Distributed workers
- GitHub Checks API
- AWS deployment
- Failure recovery and worker heartbeats

## GitHub Webhook Flow

When code is pushed to a configured repository:

1. GitHub generates a `push` event.
2. GitHub sends the event to `/webhooks/github`.
3. ForgeCI reads the raw request body and `X-Hub-Signature-256` header.
4. ForgeCI independently computes the expected HMAC-SHA256 signature using the configured webhook secret.
5. Invalid or unsigned requests are rejected.
6. ForgeCI checks the `X-GitHub-Event` event type.
7. Push events are parsed for:
   - repository name
   - commit SHA
   - Git reference / branch
8. The event is acknowledged with an HTTP response.

This allows ForgeCI to identify the exact version of a repository that should eventually be scheduled for testing.

## Project Structure

```text
ForgeCI/
├── src/
│   └── forgeci/
│       ├── __init__.py
│       ├── database.py
│       └── api/
│           ├── __init__.py
│           └── main.py
│
├── tests/
│   ├── test_health.py
│   └── test_webhook.py
│
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```

## Local Development

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ForgeCI
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi "uvicorn[standard]" pytest httpx sqlalchemy "psycopg[binary]"
```

### 4. Configure environment variables

ForgeCI expects secrets and connection information through environment variables rather than hard-coded credentials.

```bash
export GITHUB_WEBHOOK_SECRET="your-webhook-secret"
export DATABASE_URL="postgresql+psycopg://forgeci:YOUR_PASSWORD@localhost:5432/forgeci"
```

Never commit real secrets or database passwords to the repository.

### 5. Start PostgreSQL

```bash
sudo service postgresql start
```

### 6. Run the API

```bash
PYTHONPATH=src uvicorn forgeci.api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET /health
```

## Testing

Run the ForgeCI test suite with:

```bash
pytest
```

The tests currently verify both normal API behavior and webhook authentication failure cases.

## Security

ForgeCI does not trust incoming webhook payloads by default.

GitHub webhook requests are authenticated using the shared webhook secret and the `X-Hub-Signature-256` header. ForgeCI computes its own HMAC-SHA256 signature from the exact request body and compares it using Python's constant-time `hmac.compare_digest()`.

Requests with missing or incorrect signatures are rejected before their payload is processed.

Secrets are provided through environment variables and are not stored in source code.

## Roadmap

The next development milestones are:

- [x] FastAPI application setup
- [x] Health endpoint
- [x] Automated API testing
- [x] GitHub webhook endpoint
- [x] Webhook signature verification
- [x] GitHub event filtering
- [x] Real GitHub push integration
- [x] PostgreSQL connectivity
- [ ] Build database model and persistence
- [ ] Create build records from push events
- [ ] Redis-backed job queue
- [ ] CI worker process
- [ ] Repository cloning and commit checkout
- [ ] Isolated Docker test execution
- [ ] Concurrent workers
- [ ] Job leases, heartbeats, and failure recovery
- [ ] GitHub Checks API integration
- [ ] Performance and concurrency benchmarking
- [ ] Deployment and observability

## Project Goals

ForgeCI is being built as a systems-focused project to develop practical experience with:

- backend API design
- relational databases
- distributed systems
- concurrency
- job scheduling
- message queues
- container isolation
- fault tolerance
- CI/CD infrastructure
- GitHub APIs and webhooks
- performance benchmarking

The project intentionally prioritizes infrastructure and reliability over UI complexity.

## License

