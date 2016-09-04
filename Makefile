
.PHONY: default test serve docs

FLASK_APP ?= 'flasktestapp._app'

FLASK_CONFIG_ENV:=FLASK_APP=$(FLASK_APP) FLASK_SETTINGS='flasktestapp.settings:DevConfig'

default: test

test:
	python setup.py test

run:
	$(FLASK_CONFIG_ENV) flask run

serve: run

servedev:
	$(FLASK_CONFIG_ENV) flask run

shell:
	$(FLASK_CONFIG_ENV) flask shell

flask-db-init:
	$(FLASK_CONFIG_ENV) flask db init

flask-db-upgrade:
	$(FLASK_CONFIG_ENV) flask db upgrade

setupdev:
	$(MAKE) flask-db-init
	$(MAKE) flask-db-upgrade

develop:
	$(MAKE) install-requirements

install-requirements:
	pip install -r requirements/dev.txt
	pip install -e .

docs:
	$(MAKE) -C docs/ html
