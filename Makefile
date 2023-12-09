.PHONY: help
help:
	@echo "------------------"
	@echo "Available commands:"
	@echo "------------------"
	@echo "build: Build the Docker containers"
	@echo "up: Start the services"
	@echo "down: Stop the services"
	@echo "restart: Restart the services"
	@echo "logs: View output from containers"
	@echo "migrate: Run database migrations"
	@echo "shell: Access the shell of the FastAPI container"

# Build the Docker containers
.PHONY: build
build:
	docker-compose build

# Start the services
.PHONY: up
up:
	docker-compose up -d

# Stop the services
.PHONY: down
down:
	docker-compose down

# Restart the services
.PHONY: restart
restart: down up

# View output from containers
.PHONY: logs
logs:
	docker-compose logs

# Run database migrations
.PHONY: migrate
migrate:
	docker-compose run --rm fastapi-app alembic upgrade head

# Access the shell of the FastAPI container
.PHONY: shell
shell:
	docker-compose exec fastapi-app sh

.PHONY: prune-images
prune:
	docker image prune -f