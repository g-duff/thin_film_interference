SHELL = /bin/sh

dev_dependencies: .venv
	./.venv/bin/pip3 install --upgrade pip
	./.venv/bin/pip3 install -r ./requirements/dev.txt

.venv:
	python3 -m venv ./.venv
