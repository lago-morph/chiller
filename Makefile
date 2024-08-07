define DOCS
Convenience helpers for Watch and Chill development

To get running at http://localhost:8222
make packages
make images
make docker-net
make start-all
(wait a few seconds then) make init-postgres

Python packaging: packages api-package sdk-package frontend-package
Docker images:    images api-image frontend-image load-image (+same with -ttl)
Testing:          all-tests unit-tests integration-tests browser-test load-test
Unit and int.:    api-unit frontend-unit api-integration frontend-integration
Docker:           docker-net start-all stop-all
Docker cont.:     start/stop - postgres/api/frontend (e.g., start-api)
DB test:          get-movies get-movies-num get-users get-users-num
DB:               init-postgres

Note - create .venvs to run unit, integration, and browser tests - see Wiki
endef

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
TTL_FRONTEND_NAME := $(shell uuidgen)
TTL_API_NAME := $(shell uuidgen)
TTL_LOAD_NAME := $(shell uuidgen)

.ONESHELL:

# dummy target does nothing when make without arguments
export DOCS
show-usage: 
	@echo "$$DOCS"

packages: api-package sdk-package frontend-package
images: api-image frontend-image load-image
images-ttl: api-image-ttl frontend-image-ttl load-image-ttl

all-tests: unit-tests integration-tests browser-test
unit-tests: api-unit frontend-unit
integration-tests: api-integration frontend-integration

browser-test:
	. ../run/chiller_browser/.venv/bin/activate
	CHILLER_HOST=$(LOCALHOST) CHILLER_PORT=$(CHILLER_FRONTEND_PORT) pytest frontend/browser_tests
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

frontend-image-ttl:
	docker build -f frontend/Dockerfile -t ttl.sh/$(TTL_FRONTEND_NAME) .
	docker push ttl.sh/$(TTL_FRONTEND_NAME)
	echo
	echo "frontend image name: $(TTL_FRONTEND_NAME)"
	echo "- name: ghcr.io/lago-morph/chiller_frontend\n  newName: ttl.sh/$(TTL_FRONTEND_NAME)\n  newTag: latest" > /tmp/ttl_frontend_values.yaml
	echo "helm override values file in /tmp/ttl_frontend_values.yaml"

frontend-image:
	docker build -f frontend/Dockerfile -t chiller_frontend .

api-image-ttl:
	docker build -f api/Dockerfile -t ttl.sh/$(TTL_API_NAME) .
	docker push ttl.sh/$(TTL_API_NAME)
	echo
	echo "api image name: $(TTL_API_NAME)"
	echo "- name: ghcr.io/lago-morph/chiller_api\n  newName: ttl.sh/$(TTL_API_NAME)\n  newTag: latest" > /tmp/ttl_api_values.yaml
	echo "helm override values file in /tmp/ttl_api_values.yaml"

api-image: 
	docker build -f api/Dockerfile -t chiller_api .

load-image-ttl:
	docker build -f load/Dockerfile -t ttl.sh/$(TTL_LOAD_NAME) .
	docker push ttl.sh/$(TTL_LOAD_NAME)
	echo
	echo "load image name: $(TTL_LOAD_NAME)"
	echo "- name: ghcr.io/lago-morph/chiller_load\n  newName: ttl.sh/$(TTL_LOAD_NAME)\n  newTag: latest" > /tmp/ttl_load_values.yaml
	echo "helm override values file in /tmp/ttl_load_values.yaml"

load-image: 
	docker build -f load/Dockerfile -t chiller_load .

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

get-movies:
	PGPASSWORD=$(PGPASSWORD) psql -U $(PGUSER) -d $(PGDATABASE) -h $(PGHOST) -c 'select * from movielist;'

get-movies-num:
	PGPASSWORD=$(PGPASSWORD) psql -U $(PGUSER) -d $(PGDATABASE) -h $(PGHOST) -c 'select count(*) from movielist;'

get-users:
	PGPASSWORD=$(PGPASSWORD) psql -U $(PGUSER) -d $(PGDATABASE) -h $(PGHOST) -c 'select * from users;'

get-users-num:
	PGPASSWORD=$(PGPASSWORD) psql -U $(PGUSER) -d $(PGDATABASE) -h $(PGHOST) -c 'select count(*) from users;'

init-postgres:
	PGPASSWORD=$(PGPASSWORD) psql -U $(PGUSER) -d $(PGDATABASE) -h $(PGHOST) -f api/chiller_api/db/schema.sql

start-api:
	docker run --rm --name chiller-api -e CHILLER_DB_PASSWORD=$(PGPASSWORD) -e CHILLER_DB_HOST=chiller-postgres -d -p $(CHILLER_API_PORT):80 --network $(DOCKER_NET) chiller_api

stop-api:
	docker stop chiller-api

load-test:
	docker run --rm --name chiller-load -e CHILLER_HOST=chiller-frontend -e CHILLER_PORT=80 --network $(DOCKER_NET) -d chiller_load

start-frontend:
	docker run --rm --name chiller-frontend -e CHILLER_HOST=chiller-api --network $(DOCKER_NET) -p $(CHILLER_FRONTEND_PORT):80 -d chiller_frontend

stop-frontend:
	docker stop chiller-frontend
