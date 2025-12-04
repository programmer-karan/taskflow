VENV := .venv
PYTHON := python3
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
REQ := requirements.txt

UVICORN_APP := src.main:app
UVICORN_HOST := localhost
UVICORN_PORT := 8000

.PHONY: help venv install run test docker-up docker-down shell clean

help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies"
	@echo "  make run           Run local server"
	@echo "  make test          Run tests"
	@echo "  make docker-up     Start DB & Redis"
	@echo "  make shell         Open a shell with venv activated"
	@echo "  make clean         Cleanup"

venv:
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "✔ Created venv at $(VENV)"; \
	else \
		echo "✔ Venv already exists at $(VENV)"; \
	fi

install: venv
	@echo "Installing into $(VENV)..."
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install --upgrade -r $(REQ)
	@echo "✔ Dependencies installed"

# Run uvicorn using the venv python so the module is resolved correctly
run: install docker-up
	@echo "Starting Uvicorn on $(UVICORN_HOST):$(UVICORN_PORT)..."
	@$(PY) -m uvicorn $(UVICORN_APP) --host $(UVICORN_HOST) --port $(UVICORN_PORT) --reload

test: install docker-up
	@echo "Running tests..."
	@$(PY) -m pytest -v

docker-up:
	docker compose up -d postgres redis

docker-down:
	docker compose down

# Open an interactive shell with venv activated (activation persists inside that shell)
shell: venv
	@echo "Opening a bash shell with $(VENV) activated..."
	@bash -i -c "source $(VENV)/bin/activate && exec bash"

clean:
	@rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@echo "Cleaned"