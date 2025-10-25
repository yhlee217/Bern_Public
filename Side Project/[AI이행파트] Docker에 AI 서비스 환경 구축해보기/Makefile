.PHONY: help build up down restart logs shell test lint format clean all dev prod

# Default target
help:
	@echo "Available commands:"
	@echo "  build     Build Docker images"
	@echo "  up        Start services in detached mode"
	@echo "  down      Stop and remove services"
	@echo "  restart   Restart services"
	@echo "  logs      Show service logs"
	@echo "  shell     Open shell in running container"
	@echo "  test      Run tests"
	@echo "  lint      Run code linting"
	@echo "  format    Format code"
	@echo "  clean     Clean up containers, images, and volumes"
	@echo "  all       Build, test, and start services"
	@echo "  dev       Start in development mode"
	@echo "  prod      Start in production mode"

# Docker operations
build:
	@echo "Building Docker images..."
	docker-compose -f docker/docker-compose.yml build

up:
	@echo "Starting services..."
	docker-compose -f docker/docker-compose.yml up -d

down:
	@echo "Stopping services..."
	docker-compose -f docker/docker-compose.yml down

restart: down up

logs:
	@echo "Showing logs..."
	docker-compose -f docker/docker-compose.yml logs -f

shell:
	@echo "Opening shell in container..."
	docker-compose -f docker/docker-compose.yml exec sentiment-api /bin/bash

# Development operations
dev:
	@echo "Starting in development mode..."
	cp .env.example .env 2>/dev/null || true
	docker-compose -f docker/docker-compose.yml up --build

prod:
	@echo "Starting in production mode..."
	docker-compose -f docker/docker-compose.yml up -d --build

# Testing and Quality
test:
	@echo "Running tests..."
	docker-compose -f docker/docker-compose.yml exec sentiment-api python -m pytest tests/ -v

test-local:
	@echo "Running tests locally..."
	python -m pytest tests/ -v

lint:
	@echo "Running linting..."
	docker-compose -f docker/docker-compose.yml exec sentiment-api flake8 src/ tests/
	docker-compose -f docker/docker-compose.yml exec sentiment-api black --check src/ tests/
	docker-compose -f docker/docker-compose.yml exec sentiment-api isort --check-only src/ tests/

lint-local:
	@echo "Running linting locally..."
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	@echo "Formatting code..."
	docker-compose -f docker/docker-compose.yml exec sentiment-api black src/ tests/
	docker-compose -f docker/docker-compose.yml exec sentiment-api isort src/ tests/

format-local:
	@echo "Formatting code locally..."
	black src/ tests/
	isort src/ tests/

# Health check
health:
	@echo "Checking service health..."
	curl -f http://localhost:8000/health || exit 1

# API test
api-test:
	@echo "Testing API..."
	curl -X POST "http://localhost:8000/predict" \
		-H "Content-Type: application/json" \
		-d '{"text": "I love this product!"}'

# Cleanup operations
clean:
	@echo "Cleaning up..."
	docker-compose -f docker/docker-compose.yml down -v --remove-orphans
	docker system prune -f
	docker volume prune -f

clean-all: clean
	@echo "Removing all related images..."
	docker images | grep sentiment | awk '{print $$3}' | xargs -r docker rmi -f

# Combined operations
all: build test up health

# Installation (for local development)
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest-cov pre-commit

# Documentation
docs:
	@echo "Opening API documentation..."
	@echo "Swagger UI: http://localhost:8000/docs"
	@echo "ReDoc: http://localhost:8000/redoc"

# Environment setup
env:
	@echo "Setting up environment..."
	cp .env.example .env
	@echo "Please edit .env file with your configuration"

# Monitoring
monitor:
	@echo "Monitoring services..."
	watch -n 2 'docker-compose -f docker/docker-compose.yml ps && echo "" && docker stats --no-stream'