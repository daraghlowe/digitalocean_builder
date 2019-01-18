.PHONY: default all clean clean-artifacts build shell seeddata test jenkins-test smoke-staging smoke-production update-deps \
	celery-status psql makemigrations merge-migrations up down pull-linters generate-openapi unittest

IMAGE_TAG ?= :latest

default: all

MARKDOWN_LINTER := wpengine/mdl
YAML_LINTER := wpengine/yamllint

help: ## Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
}' $(MAKEFILE_LIST) | sort

all: clean-artifacts lint build generate-openapi test

clean: down ## Delete local data and ensure containers are stopped
	rm -rf ./.compose-data

clean-artifacts: ## Delete all generated files in the artifacts dir
	mkdir -p ./digitalocean-builder/artifacts/
	rm -rf ./digitalocean-builder/artifacts/*

local.env:
	@touch local.env

digitalocean-builder/requirements.txt: digitalocean-builder/requirements.in digitalocean-builder/requirements.indexes
	docker-compose run --rm app bash -c 'pip-compile --output-file requirements.txt requirements.in'

upgrade-deps:  ## Generate a new requirements.txt with the latest deps
	docker-compose run --rm app bash -c 'pip-compile --upgrade --output-file requirements.txt'

build: local.env digitalocean-builder/requirements.txt ## Build all the docker images
	docker-compose build

test: local.env build lint unittest ## Run project tests

unittest: local.env build ## Just run unit tests (skip lints)
	docker-compose run --rm dev bash -c "./digitalocean-builder/bin/test.sh"

smoke-test-staging: local.env ## Smoke test the staging instance of the service
	docker-compose run --rm -u root -e GIT_COMMIT -e SMOKE_DOMAIN=digitalocean-builder-staging.wpesvc.net dev bash -c "./digitalocean-builder/bin/smoke.sh"

smoke-test-production: local.env ## Smoke test the production instance of the service
	docker-compose run --rm -u root -e GIT_COMMIT -e SMOKE_DOMAIN=digitalocean-builder.wpesvc.net dev bash -c "./digitalocean-builder/bin/smoke.sh"

run: ## Start a local instance of the service
	docker-compose up

up: ## Start a local instance of the service run as a daemon
	docker-compose up -d

down: ## Ensure the docker-compose pieces are all stopped
	docker-compose down

shell: local.env  ## Start a shell on a local instance of the service
	docker-compose run --rm dev bash

django-shell: local.env ## Launch a django shell on a local instance of the service
	docker-compose run --rm app python manage.py shell

makemigrations: local.env ## Generate migration files
	docker-compose run --rm dev ./digitalocean-builder/manage.py makemigrations

merge-migrations: local.env ## Merge migration files
	docker-compose run --rm dev ./digitalocean-builder/manage.py makemigrations --merge

celery-status: ## Show the status of the celery tasks
	docker-compose run --rm worker celery -A config.celery inspect active

psql: ## launch a psql shell on a local instance of the service
	docker-compose exec db psql digitalocean-builder -U postgres

lint: lint-terraform lint-markdown lint-python lint-yaml ## Run all linters

# Pull down our mdl, and yamllint images for use in linting.
pull-linters:
	@echo "\nEnsuring up to date linters"
	docker pull ${MARKDOWN_LINTER}
	docker pull ${YAML_LINTER}

lint-markdown: pull-linters ## Lint the markdown files for the service
	@echo "\nLinting markdown files"
	docker run --rm -v `pwd`:/workspace ${MARKDOWN_LINTER} /workspace
	@echo "Markdown linting passed!"

lint-yaml: pull-linters ## Lint the yaml files for the service
	@echo "\nLinting yaml files"
	docker run --rm -v `pwd`:/workspace -v `pwd`/.yamllintrc:/yamllint/.yamllintrc ${YAML_LINTER} /workspace
	@echo "Yaml linting passed!"

lint-python: pull-linters build ## Lint the python files for the service
	@echo "\nLinting python files"
	docker-compose run --rm dev flake8 digitalocean-builder
	@echo "Python linting passed!"

lint-terraform: ## Lint the terraform stacks for the project
	@echo "\nLinting terraform files"
	docker run --rm -v `pwd`:/workspace -w /workspace --entrypoint /workspace/deploy/terraform/terraform-validate.sh hashicorp/terraform:0.9.11
	@echo "Terraform linting passed!"

generate-openapi: local.env ## Generate Open API files for Cloud Endpoints
	docker-compose run --rm dev python ./digitalocean-builder/specification/generate_openapi.py