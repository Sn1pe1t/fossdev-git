# Корневой Makefile для микросервисного проекта
# Управление через docker-compose

.PHONY: help build up down logs ps clean restart

# Цвета для вывода (опционально)
GREEN  := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
RESET  := $(shell tput sgr0)

help:
	@echo "$(GREEN)Доступные команды:$(RESET)"
	@echo "  make build   - собрать образы всех сервисов"
	@echo "  make up      - запустить все контейнеры в фоне"
	@echo "  make down    - остановить и удалить контейнеры"
	@echo "  make logs    - показать логи всех сервисов"
	@echo "  make ps      - показать статус контейнеров"
	@echo "  make clean   - остановить контейнеры и удалить образы"
	@echo "  make restart - перезапустить все сервисы"

build:
	@echo "$(YELLOW)Сборка Docker образов...$(RESET)"
	docker-compose build

up:
	@echo "$(YELLOW)Запуск контейнеров...$(RESET)"
	docker-compose up -d
	@echo "$(GREEN)Сервисы запущены. order-service доступен на http://localhost:8002$(RESET)"

down:
	@echo "$(YELLOW)Остановка и удаление контейнеров...$(RESET)"
	docker-compose down

logs:
	docker-compose logs -f

ps:
	docker-compose ps

clean: down
	@echo "$(YELLOW)Удаление образов и неиспользуемых данных...$(RESET)"
	docker-compose down --rmi all --volumes --remove-orphans

restart: down up

# Удобные алиасы
start: up
stop: down
status: ps