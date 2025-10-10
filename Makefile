
# define the name of the virtual environment directory
VENV := .venv
TEST=
PARAMETERS=

# default target, when make executed without arguments
all: venv

# venv is a shortcut target
venv: $(VENV)/bin/activate
	uv sync

run-old:
	uv run app ${PARAMETERS}

run:
	uv run uvicorn pepper:app ${PARAMETERS}

run-cli:
	uv run uvicorn pepper.main:cli ${PARAMETERS}

dev:
	uv run uvicorn pepper:app --reload ${PARAMETERS}

mig:
	uv run alembic --config ./app/alembic.ini revision --autogenerate -m "initial"

mig-check:
	uv run alembic --config ./app/alembic.ini check

mig-up:
	uv run alembic --config ./app/alembic.ini upgrade head

build:
	uv build ${PARAMETERS}

bundle:
	rm -rf dist build
	uv run pyinstaller perpper-app/src/app/manage.py --onefile --name pepper-app --add-data "app/routes/components.yaml:routes" --collect-all "aiohttp_swagger3"

test: build
	python3 -m pytest ${TEST}

clean:
	uv cache clean
	rm -rf {$(VENV),build,dist,logs/*}; rm -rf .pytest_cache; find . -type f -name '*.pyc' -delete

lint:
	 python3 -m black ./app
	 python3 -m flake8 ./app

dbuild:
	docker-compose build

dup:
	docker-compose up -d --build

dps:
	docker-compose ps

dlogs:
	docker-compose logs -f --tail 15

dclean:
	docker-compose down -v && docker-compose rm

dd:
	docker-compose down -v postgres

ddup:
	docker-compose up -d postgres

