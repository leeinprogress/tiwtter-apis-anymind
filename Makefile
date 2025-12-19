.PHONY: help install run test test-unit test-int lint format type-check check clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the application"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-unit    - Run unit tests only"
	@echo "  make test-int     - Run integration tests only"
	@echo "  make lint         - Run linter (ruff)"
	@echo "  make format       - Format code with ruff"
	@echo "  make type-check   - Run type checking (mypy)"
	@echo "  make check        - Run all quality checks"
	@echo "  make clean        - Clean cache and build files"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest --cov=app --cov-report=html --cov-report=term-missing

test-unit:
	pytest tests/unit/ -v

test-int:
	pytest tests/integration/ -v

lint:
	ruff check app tests

format:
	ruff format app tests
	ruff check --fix app tests

type-check:
	mypy app

check: lint type-check test
	@echo "All checks passed!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage
	@echo "Cleanup complete!"
