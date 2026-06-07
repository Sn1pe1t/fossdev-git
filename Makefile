PYTHON = .venv/bin/python
PIP = .venv/bin/pip
MYPY = .venv/bin/mypy
BLACK = .venv/bin/black
ISORT = .venv/bin/isort

SOURCES = src/

venv:
	python -m venv .venv

install: venv
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) src/app.py

typecheck: install
	$(MYPY) $(SOURCES)

format: install
	$(ISORT) $(SOURCES)
	$(BLACK) $(SOURCES)

lint: install
	$(ISORT) --check-only $(SOURCES)
	$(BLACK) --check $(SOURCES)

check-requirements: install
	$(PYTHON) scripts/check_imports.py

check: typecheck check-requirements lint

clean:
	rm -rf .venv .mypy_cache __pycache__

.PHONY: venv install run typecheck format lint check-requirements check clean