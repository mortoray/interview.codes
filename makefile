make: check test

check:
	mypy *.py test/*.py
.PHONY: check

test:
	python -m pytest test/
.PHONY: test

freeze:
	pip freeze --local > requirements.txt

