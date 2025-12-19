.PHONY: lint up scrape scrape-all

PYTHON := $(shell conda run -n nba which python)

lint:
	uvx ty check --python $(PYTHON) src/

up:
	@python -m uvicorn src.main:app --host 0.0.0.0 --port 5555 --reload &
	@echo "Waiting for server to start..."
	@until curl -s http://localhost:5555 > /dev/null 2>&1; do sleep 0.2; done
	@echo "Server is up! Opening browser..."
	@open -a "Google Chrome" http://localhost:5555

scrape:
ifndef TEAM
	$(error Usage: make scrape TEAM=<abbrev>  (e.g., make scrape TEAM=bos))
endif
	@python -c "from src.scrape.team_wins_losses import get_team_wins_losses_cached; get_team_wins_losses_cached('$(TEAM)')"
	@echo "\033[32m✓ success\033[0m"

scrape-all:
	@python -m src.scrape.teams

