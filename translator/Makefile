all: install
	make run

install:
	pipenv install --dev

shell:
	pipenv shell

pshell:
	pipenv run ipython

run:
	pipenv run python eazyraspi.py

test:
	pipenv run pytest

clean_run:
	rm -f *.pdf
	rm -f *.dot
	rm -f *.erp.py

clean: Pipfile.lock
	pipenv --rm
	rm -f Pipfile.lock

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
