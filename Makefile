.PHONY: build run prune all stop

build:
	@echo "Building Docker Image..."
	docker build -t toucans-hub .

run:
	@echo "Running Docker Container..."
	docker run -d --name toucans-hub -p 8000:8000 toucans-hub


stop:
	@echo "Stopping Docker Container..."
	docker stop toucans-hub

prune:
	@echo "Pruning old Docker images..."
	docker image prune -f
	# Uncomment the following line to also remove all unused images, not just dangling ones
	# docker system prune -a -f

all: prune stop build run
