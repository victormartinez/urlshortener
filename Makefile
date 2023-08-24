PROJECT_NAME = urlshorten
TEST_FOLDER = tests
APPLICATION = urlshorten.main:app

.PHONY:default
default: help

.PHONY: help
help:
	@echo "All Commands:"
	@echo "	Code Style:"
	@echo "		check - Check format style."
	@echo "		format - Format code style."
	@echo "		typecheck - Check types in code"
	@echo "	Env:"
	@echo "		clean - Remove temp files."
	@echo "		down - Stop containers."
	@echo "		run - Run application in development mode."
	@echo "		coverage - Run tests and gather coverage data."
	@echo "		up - Start containers."
	@echo "	Test:"
	@echo "		unit-test - Run unit tests."
	@echo "		integration-test - Run integration tests."
	@echo "		load-test - Run load test."
	@echo "		load-test-build - Build containers images for load test."
	@echo "		load-test-up - Run application containers for load test."


.PHONY: format
format:
	@echo ""
	@echo "FORMATTING CODE:"
	@echo ""
	black -l 88 -t py310 --skip-string-normalization --preview $(PROJECT_NAME) $(TEST_FOLDER)
	unify --in-place --recursive --quote '"' $(PROJECT_NAME) $(TEST_FOLDER)
	isort --profile black .

	@echo ""
	@echo "CHECKING CODE STILL NEEDS FORMATTING:"
	@echo ""
	black -l 88 -t py310 --skip-string-normalization --preview --check $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "CHECKING TYPING"
	@echo ""
	@make typecheck

	@echo ""
	@echo "CHECKING CODE STYLE"
	@echo ""
	flake8 $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "ENSURE DOUBLE QUOTES"
	@echo ""
	unify --check-only --recursive --quote '"' $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "SORT IMPORTS"
	@echo ""
	isort --profile black -c .

	@echo ""
	@echo "CHECKING SECURITY ISSUES"
	@echo ""
	bandit -r $(PROJECT_NAME)

.PHONY: clean
clean:
	- @find . -name "*.pyc" -exec rm -rf {} \;
	- @find . -name "__pycache__" -delete
	- @find . -name "*.pytest_cache" -exec rm -rf {} \;
	- @find . -name "*.mypy_cache" -exec rm -rf {} \;

.PHONY: typecheck
typecheck:
	mypy --python-version 3.10 --ignore-missing-imports --disallow-untyped-defs --disallow-untyped-calls $(PROJECT_NAME)/

.PHONY: run
run:
	uvicorn $(APPLICATION)

.PHONY: up
up:
	docker-compose up

.PHONY: down
down:
	docker-compose down --remove-orphans

.PHONY: db_upgrade_test
db_upgrade_test:
	DB_PORT=5435 DB_USER=postgres DB_PASS=urlshorten_test DB_HOST=127.0.0.1 DB_PORT=5435 DB_NAME=urlshorten_test alembic upgrade head

.PHONY: unit-test
unit-test:
	pytest tests/unit/ -vv

.PHONY: db_upgrade
db_upgrade:
	alembic upgrade head

.PHONY: db_generate_revision
db_generate_revision:
	alembic revision --autogenerate

.PHONY: integration-test
integration-test:
	- @make db_test_drop
	docker run -d --name urlshorten_test_db -e "POSTGRES_DB=urlshorten_test" -e "POSTGRES_PASSWORD=urlshorten_test" -P -p 127.0.0.1:5435:5432 postgres:14-alpine
	sleep 6
	@make db_upgrade_test
	pytest tests/integration/ -vv
	docker container stop urlshorten_test_db
	docker container rm urlshorten_test_db

.PHONY: coverage
coverage:
	coverage run -m pytest tests/unit/ -vv
	coverage report -m

.PHONY: db_test_drop
db_test_drop:
	docker container ls -a | grep urlshorten_test_db | awk '{print $$1}' | xargs docker container stop | xargs docker container rm

.PHONY: db_drop
db_drop:
	docker container ls -a | grep urlshorten_db | awk '{print $$1}' | xargs docker container stop | xargs docker container rm

.PHONY: load-test
load-test:
	k6 run tests/load/script.js

.PHONY: load-test-build
load-test-build:
	docker-compose --file docker-compose-load.yaml build --no-cache

.PHONY: load-test-up
load-test-up:
	docker-compose --file docker-compose-load.yaml up --scale urlshorten_app_load=5
