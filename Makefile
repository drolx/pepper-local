
# define the name of the virtual environment directory
VENV := .venv
TEST=
PARAMETERS=

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate:

# venv is a shortcut target
venv: $(VENV)/bin/activate
	python3 -m venv $(VENV)
	python3 -m pipenv shell

install:
	python3 -m pip install --upgrade pipenv pip setuptools black pyinstaller
	python3 -m pip install --editable .
	

setup:
	python3 -m pip install . ${PARAMETERS}

run:
	python3 -m app ${PARAMETERS}

mig:
	python3 -m alembic --config ./app/alembic.ini revision --autogenerate -m "initial"

mig-check:
	python3 -m alembic --config ./app/alembic.ini check

mig-up:
	python3 -m alembic --config ./app/alembic.ini upgrade head

build:
	python3 -m pip install build
	python3 -m build ${PARAMETERS}

bundle:
	rm -rf dist build
	pyinstaller app/manage.py --onefile --name pepper-local --add-data "app/routes/components.yaml:routes" --collect-all "aiohttp_swagger3"

test: build
	python3 -m pytest ${TEST}

clean:
	python3 -m pipenv --rm
	rm -rf {$(VENV),build,dist,logs/*}; rm -rf .pytest_cache; find . -type f -name '*.pyc' -delete

lint:
	 python3 -m black ./app

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

