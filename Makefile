
guard-%:
	@ if [ "${${*}}" = "" ]; then \
			echo "Environment variable $* not set"; \
			exit 1; \
	fi

install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

venv:
	uv venv -p python3.10

install-deps:
	uv sync -p python3.10

lint:
	. .venv/bin/activate \
		&& .venv/bin/ec \
		&& .venv/bin/ruff check . \
		&& .venv/bin/ruff format --check . \
		&& .venv/bin/pyright

format:
	. .venv/bin/activate \
		&& .venv/bin/ruff check --fix . \
		&& .venv/bin/ruff format .

test:
	.venv/bin/coverage run --omit tests/*.py -m unittest -v tests/test_*.py \
	&& .venv/bin/coverage html \
	&& .venv/bin/coverage xml \
	&& .venv/bin/coverage report --fail-under=100

publish:
	npm install
	npx semantic-release

# The following two tasks are executed from semantic-release process
package: guard-PYPI_VERSION 
	rm -rf dist
	uv version --no-sync $$PYPI_VERSION
	uv build

publish-pypi: package guard-PYPI_TOKEN
	UV_PUBLISH_TOKEN=$$PYPI_TOKEN uv publish
