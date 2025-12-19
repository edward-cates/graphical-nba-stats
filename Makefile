.PHONY: lint

PYTHON := $(shell conda run -n nba which python)

lint:
	uvx ty check --python $(PYTHON) src/

