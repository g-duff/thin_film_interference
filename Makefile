SHELL = /bin/sh
environment_bin := ./.venv/bin

dist:
	${environment_bin}/python3 -m build

dev_dependencies: .venv
	${environment_bin}/pip3 install --upgrade pip
	${environment_bin}/pip3 install -r ./requirements/dev.txt

lint_check:
	${environment_bin}/pylint ./{src,tests}/*py

test:
	${environment_bin}/python3 -m unittest discover ./tests/ 'test_*.py'

.venv:
	python3 -m venv ./.venv
