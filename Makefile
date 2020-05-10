
guard-%:
	@ if [ "${${*}}" = "" ]; then \
			echo "Environment variable $* not set"; \
			exit 1; \
	fi

style:
	# stop the build if there are Python syntax errors or undefined names
	flake8 pluralizer tests --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings.
	flake8 pluralizer tests --count --statistics

test:
	coverage run --omit tests/*.py -m unittest -v tests/test_*.py && coverage html && coverage xml && coverage report --fail-under=100

publish:
	npm install
	npx semantic-release

# The following two tasks are executed from semantic-release process
package: guard-PYPI_VERSION 
	rm -rf dist
	python setup.py sdist bdist_wheel

publish-pypi: package guard-PYPI_TOKEN
	twine upload -u '__token__' -p '$(PYPI_TOKEN)' --skip-existing dist/*
