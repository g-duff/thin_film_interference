SHELL = /bin/sh

build:
	./.venv/bin/python3 -m build

dev_dependencies: .venv
	./.venv/bin/pip3 install --upgrade pip
	./.venv/bin/pip3 install -r ./requirements/dev.txt

lint_check:
	./.venv/bin/pylint ./{src,tests}/*py

.venv:
	python3 -m venv ./.venv
