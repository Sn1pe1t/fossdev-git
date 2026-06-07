VENV = .venv
PYTHON = $(VENV)/Scripts/python

.PHONY: venv install run typecheck lint format check-requirements check clean

venv:
	python -m venv $(VENV)

install: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

run: venv
	$(PYTHON) src/app.py

typecheck: venv
	$(PYTHON) -m mypy src/

lint: venv
	$(PYTHON) -m flake8 src/

format: venv
	$(PYTHON) -m black src/

check-requirements: venv
	$(PYTHON) -m pip_check_reqs --ignore-extra src/

check: typecheck lint check-requirements

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true