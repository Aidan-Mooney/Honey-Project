SHELL := /bin/bash

define execute_in_env
	export PYTHONPATH=. && source venv/bin/activate && $1
endef

create-environment:
	@echo ">>> Setting up Venv"
	python -m venv venv

install-requirements: create-environment
	@echo ">>> Installing requirements."
	$(call execute_in_env, pip install -r ./requirements.txt)

install-dev-tools: create-environment
	@echo ">>> Installing Dev Tools"
	$(call execute_in_env, pip install bandit ruff pytest pytest-testdox pytest-cov)

security-checks: create-environment
	@echo ">>> Running security checks"
	$(call execute_in_env, bandit -lll */*.py *c/*.py)

check-pep8-compliance: create-environment
	@echo ">>> Running ruff"
	$(call execute_in_env, ruff check src)
	$(call execute_in_env, ruff check test)

run-pytest: create-environment
	@echo ">>> Running pytest"
	$(call execute_in_env, pytest --testdox -vvvrP --cov=src --cov-fail-under=90 test/*)