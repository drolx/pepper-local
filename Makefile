
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
	uv run uvicorn pepper.server:app ${PARAMETERS}

run-cli:
	uv sync
	uv run pepper-cli ${PARAMETERS}

dev:
	uv run uvicorn pepper.server:app --reload ${PARAMETERS}

mig:
	uv run --project=pepper-sync aerich init-db

mig-up:
	uv run --project=pepper-sync aerich migrate

build:
	uv build ${PARAMETERS}

bundle:
	rm -rf dist build
	uv run pyinstaller perpper-app/src/app/manage.py --onefile --name pepper-app --add-data "app/routes/components.yaml:routes" --collect-all "aiohttp_swagger3"

test:
	uv run --project=pepper-sync pytest ${PARAMETERS}

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

