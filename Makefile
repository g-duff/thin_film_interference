SHELL = /bin/sh
environment_bin := ./.venv/bin

dist:
	${environment_bin}/python3 -m build

dev_dependencies: .venv
	${environment_bin}/pip3 install --upgrade pip
	${environment_bin}/pip3 install -r ./requirements/dev.txt

editable_install: .venv
	${environment_bin}/pip3 install --editable .

lint_check:
	${environment_bin}/pylint ./{src/thin_film_interference,tests}/*py

test:
	${environment_bin}/python3 -m unittest discover ./tests/ 'test_*.py'

.venv:
	python3 -m venv ./.venv
