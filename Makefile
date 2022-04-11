.ONESHELL:
SHELL := /bin/sh

.EXPORT_ALL_VARIABLES:
SERVICE_NAME ?= spacex-api
BUILD_DATE ?= $(shell date +"%Y-%m-%d %T")
CURRENT_UID=$(shell id -u):$(shell id -g)

### go coverage test ###
cover_dir=.cover
cover_profile=${cover_dir}/profile.out
cover_html=${cover_dir}/coverage.html

default:
	@echo "##             		  SPACEX-API	                 ##"
	@echo "##                                                    ##"
	@echo "## build: Creates the container                       ##"
	@echo "## devshell: Open a shell prompt.                     ##"

# =========================== SET VARS BY MODE ==============================

# wildcard
%:
	@:

# =========================== BUILD ==============================
# Build service image(s)
build: 
	CURRENT_UID=$(CURRENT_UID) docker-compose build $(SERVICE_NAME)

# =========================== EXEC ==============================
# Runs a docker container's shell to access the service.
# Inside the container execute `python manage.py` to start the application.
devshell: parse 
	$(info [INFO] Starting a shell in spacex-api container...)
	@docker-compose -f docker-compose.yml run --entrypoint bash --rm -e "TERM=xterm-256color" --service-ports $(SERVICE_NAME);

# =========================== INIT ==============================
# Command to insert starlink_historical_data.json into the DB
# the script will parse the JSON into time-serie
initdb:
	@python initdb.py



test_cover: test
	go tool cover -func=${cover_profile}

export-vars:
	@echo "[INFO] Export .env variables"
	export $(grep -v '^#' .env | xargs)

