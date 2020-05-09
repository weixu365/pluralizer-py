
guard-%:
	@ if [ "${${*}}" = "" ]; then \
			echo "Environment variable $* not set"; \
			exit 1; \
	fi

test:
	coverage run --omit tests/*.py -m unittest -v tests/test_*.py && coverage html

publish:
	npm install
	npx semantic-release

# The following two tasks are executed from semantic-release process
package: guard-PYPI_VERSION 
	rm -rf dist
	python setup.py sdist bdist_wheel

publish-pypi: package guard-PYPI_TOKEN
	twine upload -u '__token__' -p '$(PYPI_TOKEN)' --skip-existing dist/*
