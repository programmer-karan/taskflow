# TaskFlow

> Distributed Task Processing Engine

TaskFlow is a high-performance, distributed task execution system built with FastAPI, Celery, Redis, and PostgreSQL. It is designed to handle asynchronous workloads reliably under heavy concurrent conditions, featuring a robust architecture for background workers, caching, and observability.

---

## 🚀 Features

- **Asynchronous Task Processing**: Distributed worker system using Celery and Redis
- **Concurrency & Speed**: Async-first API design with Redis-based response caching and rate limiting
- **Object Storage**: Seamless integration with MinIO for decoupled file handling
- **Observability**: Built-in Prometheus metrics and structured logging for production monitoring
- **Cloud Native**: Fully containerized with Docker and ready for Kubernetes deployment
- **CI/CD Ready**: Integrated pipeline that validates builds using isolated Postgres and Redis containers

---

## 🛠️ Tech Stack

TaskFlow leverages several industry-standard open-source projects:

| Technology | Description |
|------------|-------------|
| **FastAPI** | Modern, high-performance web framework for Python |
| **Celery** | Distributed Task Queue to handle background jobs |
| **Redis** | Message broker, caching layer, and rate-limiting store |
| **PostgreSQL** | Reliable primary relational datastore |
| **Alembic** | Lightweight database migration tool for usage with SQLAlchemy |
| **Docker & Kubernetes** | Container orchestration and deployment |
| **Prometheus** | Metrics and monitoring |
| **MinIO** | High-performance object storage |

---

## 🏗️ Engineering Decisions

| Technology | Role | Why? |
|------------|------|------|
| **Redis** | Broker/Cache | Unified layer for brokering, caching, and atomic rate limiting |
| **Celery** | Worker Engine | Decouples long-running tasks and supports horizontal scaling |
| **Async FastAPI** | API Layer | High concurrency for I/O-bound workloads |
| **Alembic** | Migrations | Versioned schema control for consistent DB states |

---

## 📦 Installation

### Prerequisites

- Docker
- Python 3.10+

### Local Setup

1. Clone the repository and spin up the infrastructure:

```bash
git clone https://github.com/programmer-karan/taskflow.git
cd taskflow/backend
docker-compose up --build
```

2. Apply database migrations:

Once the containers are running, apply the database schema:

```bash
alembic upgrade head
```

3. Run the API (Development):

```bash
uvicorn src.main:app --reload
```

---

## 🧪 Testing

The test suite validates integration behavior by spinning up temporary service containers.

```bash
pytest
```

---

## ☸️ Kubernetes Deployment

TaskFlow is manifest-ready for Minikube or cloud providers.

```bash
minikube start
kubectl apply -f k8s/
minikube tunnel
```

---

## 📁 Project Structure

```
backend/
 ├── src/                # Modular domain logic (auth, tasks, files)
 ├── alembic/            # DB Migrations
 ├── Dockerfile          # Container definition
 ├── docker-compose.yml  # Local orchestration
 ├── prometheus.yml      # Metrics config
 └── pytest.ini          # Testing config
```

---

## 💡 How It Works

1. **Type a request** to the Async API
2. **Watch Celery workers** handle the heavy lifting
3. **✨ Scalability ✨**

---

## 👨‍💻 Author

**Karan Kumar**  
Backend Engineer – Distributed Systems, Async Processing, System Design

[![GitHub](https://img.shields.io/badge/GitHub-programmer--karan-181717?style=flat&logo=github)](https://github.com/programmer-karan)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/programmer-karan)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/programmer-karan">Karan Kumar</a></sub>
</div>
