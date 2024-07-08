MAKEFLAGS += --jobs

PGUSER := postgres
PGPASSWORD := postgres
PGDATABASE := chiller
LOCALHOST := 127.0.0.1
PGHOST := $(LOCALHOST)
CHILLER_API_PORT := 8080
CHILLER_FRONTEND_PORT := 8222
DOCKER_NET := chiller-net
PGIMAGE := postgres:16.3-alpine

.ONESHELL:

# Note that there are no dependencies here because I'm lazy
target-required: 

packages: api-package sdk-package frontend-package
images: api-image frontend-image

all-tests: unit-tests integration-tests browser-test
unit-tests: api-unit frontend-unit
integration-tests: api-integration frontend-integration

browser-test:
	. ../run/chiller_browser/.venv/bin/activate
	pytest frontend/browser_tests
	deactivate

api-integration:
	. ../run/chiller_sdk/.venv/bin/activate
	CHILLER_HOST=$(LOCALHOST):$(CHILLER_API_PORT) \
		pytest sdk/integration_test
	deactivate

frontend-integration:
	. ../run/chiller_frontend/.venv/bin/activate
	CHILLER_HOST=$(LOCALHOST):$(CHILLER_API_PORT) \
		pytest frontend/integration_tests
	deactivate

api-unit:
	. ../run/chiller_api/.venv/bin/activate
	CHILLER_DB_PASSWORD=$(PGPASSWORD) \
		CHILLER_DB_HOST=$(PGHOST) \
		pytest api/chiller_api/test
	deactivate

frontend-unit:
	. ../run/chiller_frontend/.venv/bin/activate
	pytest frontend/tests
	deactivate

frontend-image:
	docker build -f frontend/Dockerfile -t chiller_frontend .

api-image: 
	docker build -f api/Dockerfile -t chiller_api .

api-package: 
	python3 -m build api

frontend-package: 
	python3 -m build frontend

sdk-package: 
	python3 -m build sdk

docker-net:
	docker network create $(DOCKER_NET)

start-all: start-postgres start-api start-frontend
stop-all: stop-postgres stop-api stop-frontend

start-postgres:
	docker run --rm --name chiller-postgres -e POSTGRES_PASSWORD=$(PGPASSWORD) -e POSTGRES_DB=$(PGDATABASE) -d -p 5432:5432 --network $(DOCKER_NET) $(PGIMAGE)

stop-postgres:
	docker stop chiller-postgres

init-postgres:
	PGPASSWORD=$(PGPASSWORD) psql -U $(PGUSER) -d $(PGDATABASE) -h $(PGHOST) -f api/chiller_api/db/schema.sql

start-api:
	docker run --rm --name chiller-api -e CHILLER_DB_PASSWORD=$(PGPASSWORD) -e CHILLER_DB_HOST=chiller-postgres -d -p $(CHILLER_API_PORT):80 --network $(DOCKER_NET) chiller_api

stop-api:
	docker stop chiller-api

start-frontend:
	docker run --rm --name chiller-frontend -e CHILLER_HOST=chiller-api --network $(DOCKER_NET) -p $(CHILLER_FRONTEND_PORT):80 -d chiller_frontend

stop-frontend:
	docker stop chiller-frontend
