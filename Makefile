# Переменные
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Цвета для вывода (опционально, для красоты)
GREEN  := $(shell tput setaf 2)
RED    := $(shell tput setaf 1)
YELLOW := $(shell tput setaf 3)
RESET  := $(shell tput sgr0)

.PHONY: venv install run typecheck lint format check-requirements check clean

# Создание виртуального окружения
venv:
	@echo "$(YELLOW)Creating virtual environment...$(RESET)"
	python3 -m venv $(VENV)

# Установка зависимостей
install: venv
	@echo "$(YELLOW)Installing dependencies from requirements.txt...$(RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Запуск приложения (гарантированно из окружения проекта)
run: venv
	@echo "$(YELLOW)Running app.py...$(RESET)"
	$(PYTHON) src/app.py

# Проверка типов через mypy
typecheck: venv
	@echo "$(YELLOW)Running mypy type check...$(RESET)"
	$(PYTHON) -m mypy src/

# Проверка стилей через flake8 (без изменений)
lint: venv
	@echo "$(YELLOW)Running flake8 linter...$(RESET)"
	$(PYTHON) -m flake8 src/

# Автоматическое форматирование через black
format: venv
	@echo "$(YELLOW)Formatting code with black...$(RESET)"
	$(PYTHON) -m black src/

# Проверка соответствия импортов и requirements.txt
check-requirements: venv
	@echo "$(YELLOW)Checking imports against requirements.txt...$(RESET)"
	$(PYTHON) -m pip_check_reqs --ignore-extra src/

# Композитный target: все проверки качества
check: typecheck lint check-requirements
	@echo "$(GREEN)All checks passed successfully!$(RESET)"

# Очистка временных файлов и окружения
clean:
	@echo "$(YELLOW)Cleaning up...$(RESET)"
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache