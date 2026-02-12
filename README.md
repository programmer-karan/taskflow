🚀 TaskFlow – Distributed Task Processing Engine

TaskFlow is a distributed task execution system built with FastAPI, Celery, Redis, and PostgreSQL, designed to handle asynchronous workloads reliably under concurrent conditions.

This project demonstrates production-oriented backend engineering including background workers, caching, rate limiting, CI pipelines, observability, container orchestration, and Kubernetes deployment.


🏗 System Architecture

Client
  ↓
FastAPI API Layer (Async)
  ↓
PostgreSQL (Primary DB)
  ↓
Redis
  ├── Celery Broker
  ├── Caching Layer
  └── Rate Limiting Store
  ↓
Celery Worker Nodes
  ↓
MinIO (Object Storage)
  ↓
Prometheus (Metrics)

Key Characteristics
	•	Async-first API design
	•	Message-driven background execution
	•	Dockerized multi-service architecture
	•	CI-tested with isolated Postgres + Redis
	•	Kubernetes-compatible deployment

⚙ Core Capabilities

1️⃣ Asynchronous Task Processing
	•	Celery-based distributed worker system
	•	Redis broker for task queuing
	•	Fault-tolerant background execution
	•	Designed for horizontal worker scaling

2️⃣ Concurrency & Performance
	•	Async FastAPI endpoints
	•	Redis-based response caching
	•	Rate limiting using atomic Redis operations
	•	Pagination layer for large datasets

3️⃣ Persistence & Migrations
	•	PostgreSQL as primary datastore
	•	Alembic for versioned schema migrations
	•	Clean modular domain separation

4️⃣ File Handling
	•	MinIO object storage integration
	•	Decoupled file service logic

5️⃣ Observability & Reliability
	•	Prometheus metrics endpoint
	•	Structured logging
	•	CI pipeline validating build + tests

6️⃣ Deployment & Infra
	•	Docker Compose local orchestration
	•	Kubernetes deployment (Minikube)
	•	CI pipeline with service containers (Postgres + Redis)

🧠 Engineering Decisions

Why Redis?
	•	Unified layer for:
	•	Message brokering (Celery)
	•	Caching
	•	Rate limiting
	•	Atomic operations enable safe throttling
	•	Low-latency in-memory store

Why Celery?
	•	Decouples long-running tasks from API layer
	•	Retry & failure handling support
	•	Enables horizontal scaling of worker nodes

Why Async FastAPI?
	•	High concurrency under I/O-bound workloads
	•	Efficient request handling
	•	Modern Python async ecosystem

Why Containerization?
	•	Deterministic environments
	•	Simplified local setup
	•	Deployment portability

📂 Project Structure
backend/
  src/
    auth/
    tasks/
    files/
    notifications/
    shared/
    main.py
  alembic/
  Dockerfile
  docker-compose.yml
  prometheus.yml
  requirements.txt
  pytest.ini

🚀 Running Locally

git clone https://github.com/programmer-karan/taskflow.git
cd taskflow/backend
docker-compose up --build

Run migrations:
alembic upgrade head

Run API:
uvicorn src.main:app --reload

🧪 Testing
pytest

CI pipeline:
	•	Spins up Postgres container
	•	Spins up Redis container
	•	Executes async test suite
	•	Validates integration behavior

☸ Kubernetes Deployment
minikube start
kubectl apply -f k8s/
minikube tunnel


📈 What This Project Demonstrates
	•	Distributed system fundamentals
	•	Async processing patterns
	•	Worker-based architecture
	•	Infrastructure awareness (CI, Docker, K8s)
	•	Performance considerations (caching, rate limiting)
	•	Clean modular backend design

⸻

👨‍💻 Author

Karan Kumar
Backend Engineer – Distributed Systems, Async Processing, System Design
GitHub: https://github.com/programmer-karan
LinkedIn: (your link)
