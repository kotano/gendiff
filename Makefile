install:
	poetry install

demo:
	make install_from_pip

publish_test: check
	poetry config repositories.kotano-gendiff https://test.pypi.org/legacy/
	poetry publish -r kotano-gendiff

test:
	poetry run pytest -vv --strict --cov --cov-report xml

lint:
	poetry run flake8 gendiff

check: lint test

install_from_pip:
	pip install -i https://test.pypi.org/simple/ kotano-gendiff --upgrade

uninstall:
	pip uninstall kotano-gendiff
	rm ~/test/bin/gendiff
