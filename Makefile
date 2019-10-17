check:
	flake8 .

test:
	pytest -s -v -p no:cacheprovider tests/