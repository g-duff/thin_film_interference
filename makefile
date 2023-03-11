SHELL = /bin/sh

environment := ./.venv
environment_bin := ${environment}/bin

.PHONY: clean format lint test

# Default Goal
editable_install: .venv
	${environment_bin}/pip3 install --editable .

clean:
	rm -rf ${environment}

dev_dependencies: .venv
	${environment_bin}/pip3 install --upgrade pip
	${environment_bin}/pip3 install -r ./requirements/dev.txt

dist:
	${environment_bin}/python3 -m build

format:
	${environment_bin}/autopep8 --in-place ./thin_film_interference/*py ./test/*py

lint:
	${environment_bin}/pylint ./thin_film_interference/*py ./test/*py

test:
	${environment_bin}/python3 -m unittest discover ./test/ 'test_*.py'

.venv:
	python3 -m venv ${environment}
