SHELL := /bin/bash
SRC_DIR := ./src
TEST_DIR := ./test
PY :=
MYPY :=
MYPY_OPTS := --strict
PYTEST_OPTS :=

# use poetry's virtualenv tooling if POETRY=Y
ifeq ($(POETRY), Y)
	PY := poetry run python
	MYPY := poetry run mypy
else
	PY := PYTHONPATH=$$PYTHONPATH:${SRC_DIR} $(shell which python)
	MYPY := $(shell which mypy)
endif

.PHONY: test/mypy
test/mypy:
	${MYPY} ${MYPY_OPTS} ${SRC_DIR}

.PHONY: test/pytest
test/pytest:
	${PY} -m pytest ${PYTEST_OPTS} ${TEST_DIR}

.PHONY: test
test: test/mypy test/pytest
