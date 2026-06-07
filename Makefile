# Root Makefile for microservices project
# Docker Compose management

.PHONY: help build up down logs ps clean restart

# Optional colors
GREEN  := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
RESET  := $(shell tput sgr0)

help:
	@echo "$(GREEN)Available commands:$(RESET)"
	@echo "  make build   - build Docker images for all services"
	@echo "  make up      - start all containers in background"
	@echo "  make down    - stop and remove containers"
	@echo "  make logs    - show live logs of all services"
	@echo "  make ps      - show container status"
	@echo "  make clean   - stop containers and remove images + volumes"
	@echo "  make restart - restart all services"

build:
	@echo "$(YELLOW)Building Docker images...$(RESET)"
	docker-compose build

up:
	@echo "$(YELLOW)Starting containers...$(RESET)"
	docker-compose up -d
	@echo "$(GREEN)Services started. order-service available at http://localhost:8002$(RESET)"

down:
	@echo "$(YELLOW)Stopping and removing containers...$(RESET)"
	docker-compose down

logs:
	docker-compose logs -f

ps:
	docker-compose ps

clean: down
	@echo "$(YELLOW)Removing images, volumes and orphaned data...$(RESET)"
	docker-compose down --rmi all --volumes --remove-orphans

restart: down up

# Aliases
start: up
stop: down
status: ps