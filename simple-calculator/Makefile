VENV = .venv
PYTHON = $(VENV)/Scripts/python   # для Windows; на Linux: $(VENV)/bin/python
PIP = $(VENV)/Scripts/pip

.PHONY: venv install test lint typecheck format build upload clean

venv:
	python -m venv $(VENV)

install: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .

test:
	$(PYTHON) -m pytest tests/

lint:
	$(PYTHON) -m flake8 src/ tests/

typecheck:
	$(PYTHON) -m mypy src/

format:
	$(PYTHON) -m black src/ tests/

build:
	$(PYTHON) -m build

upload-test: build
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm -rf $(VENV) dist/ build/ *.egg-info .mypy_cache .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true