# Paths
REPO_PATH = $(shell pwd)
VENV = $(REPO_PATH)/venv
PYCACHE = $(REPO_PATH)/__pycache__

# Configuration
API_ID = {YOUR_API_ID}
API_HASH = {YOUR_API_HASH}
PHONE = {YOUR_PHONE}
DB_PASS = {YOUR_DB_PASS}
DB_PATH = $(REPO_PATH)/db
GROUP_ID = {YOUR_GROUP_ID}
BOTS_GROUP_ID = {YOUR_BOTS_GROUP_ID}

all: deploy

bootstrap:
	@echo "Generating db folder"
	mkdir $(DB_PATH)
	@echo "Bootstraping python venv"
	python -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -r requirements.txt
	@echo "Source it using: . $(VENV)/bin/activate"

clean:
	@echo "Removing folders"
	rm -rf $(DB_PATH) $(VENV) $(PYCACHE)

deploy:
	python bot.py $(API_ID) $(API_HASH) $(PHONE) $(DB_PASS) $(DB_PATH) $(GROUP_ID) $(BOTS_GROUP_ID)

.PHONY: all bootstrap clean deploy
