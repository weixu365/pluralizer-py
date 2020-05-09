
guard-%:
	@ if [ "${${*}}" = "" ]; then \
			echo "Environment variable $* not set"; \
			exit 1; \
	fi

test:
	coverage run --omit tests/*.py -m unittest -v tests/test_*.py && coverage html

publish:
	npx semantic-release --branches init

package: guard-PYPI_VERSION 
	rm -rf dist
	python setup.py sdist bdist_wheel

pypi: guard-PYPI_TOKEN
	twine upload -u '__token__' -p '$(PYPI_TOKEN)' --skip-existing dist/*
