SHELL = /bin/sh
environment_bin := ./.venv/bin
.PHONY: lint test

dist:
	${environment_bin}/python3 -m build

dev_dependencies: .venv
	${environment_bin}/pip3 install --upgrade pip
	${environment_bin}/pip3 install -r ./requirements/dev.txt

editable_install: .venv
	${environment_bin}/pip3 install --editable .

lint:
	${environment_bin}/pylint ./{src/thin_film_interference,test}/*py

test:
	${environment_bin}/python3 -m unittest discover ./test/ 'test_*.py'

.venv:
	python3 -m venv ./.venv
