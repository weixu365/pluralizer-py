
test:
	python -m unittest -v tests/test_*.py

publish:
	pip install python-semantic-release
	semantic-release publish
	