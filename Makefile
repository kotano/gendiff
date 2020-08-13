install:
	poetry install

demo:
	make install_from_pip

publish_test:
	poetry build
	poetry config repositories.kotano-gendiff https://test.pypi.org/legacy/
	@poetry publish -r kotano-gendiff --username ${TEST_PYPI_USERNAME} --password ${TEST_PYPI_PASSWORD}

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
