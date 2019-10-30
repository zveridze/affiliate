check:
	flake8 .
	py.test -p no:cacheprovider tests/ --cov=app --cov-report=xml