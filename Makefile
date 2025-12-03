# Makefile
VENV := .venv
PYTHON := python3
# Fix: Corrected variable name from PYTOHN
UVICORN_APP := src.main:app
# Note: Ensure your main.py is inside a 'src' folder as discussed
UVICORN_HOST := 0.0.0.0
UVICORN_PORT := 8000

.PHONY: help venv install run test docker-up docker-down clean

help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies"
	@echo "  make run           Run local server"
	@echo "  make test          Run tests"
	@echo "  make docker-up     Start DB & Redis"
	@echo "  make clean         Cleanup"

venv:
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "✔ Created venv"; \
	fi

install: venv
	@. $(VENV)/bin/activate && pip install -r requirements.txt
	@echo "✔ Dependencies installed"

# Fix: Added 'docker-up' dependency so DB starts automatically before app
run: install docker-up
	@echo "Starting Uvicorn..."
	@. $(VENV)/bin/activate && uvicorn $(UVICORN_APP) --host $(UVICORN_HOST) --port $(UVICORN_PORT) --reload

# New Command: Run tests
test: install docker-up
	@echo "Running tests..."
	@. $(VENV)/bin/activate && pytest -v

docker-up:
	docker compose up -d postgres redis

docker-down:
	docker compose down

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +