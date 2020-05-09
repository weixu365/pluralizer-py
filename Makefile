
test:
	coverage run --omit tests/*.py -m unittest -v tests/test_*.py && coverage html

publish:
	semantic-release --minor publish
	