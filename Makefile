.PHONY: venv format format-check lint compile docs-refs check

VENV ?= .venv
VENV_BIN := $(VENV)/bin
PYTHON ?= python3

RUFF := $(if $(wildcard $(VENV_BIN)/ruff),$(VENV_BIN)/ruff,ruff)
PYTHON := $(if $(wildcard $(VENV_BIN)/python),$(VENV_BIN)/python,python3)

venv:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install ruff

format:
	$(RUFF) format .

format-check:
	$(RUFF) format --check .

lint:
	$(RUFF) check .


compile:
	$(PYTHON) -m compileall -q scripts

docs-refs:
	$(PYTHON) scripts/check_docs_references.py

check: format-check lint compile docs-refs
