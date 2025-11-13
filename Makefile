APP_CONTAINER = main-app
APP_FILE = docker_compose/app.yaml
DB_CONTAINER = postgres
DC = docker compose
ENV_FILE = .env
EXEC = docker exec -it
LOGS = docker logs
STORAGES_FILE = docker_compose/storages.yaml
MANAGE_PY = python manage.py


.PHONY: storages 
storages: 
	${DC} -f ${STORAGES_FILE} --env-file ${ENV_FILE} up -d

.PHONY: storages-down
storages-down: 
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres 
postgres:
	${EXEC} ${DB_CONTAINER} psql -U postgres

.PHONY: storages-logs
storages-logs: 
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} --env-file ${ENV_FILE} up  --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} collectstatic

.PHONY: precommit
precommit:
	pre-commit run --all-files

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest