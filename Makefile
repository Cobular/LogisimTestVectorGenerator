.PHONY: test

test: *.py
	python -m unittest discover . -p *.py