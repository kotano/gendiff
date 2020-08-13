install:
	poetry install

demo: download

publish:
	poetry build
	poetry config repositories.kotano-gendiff https://test.pypi.org/legacy/
	@poetry publish -r kotano-gendiff --username ${TEST_PYPI_USERNAME} --password ${TEST_PYPI_PASSWORD}

test:
	poetry run pytest -vv --strict --cov --cov-report xml
	@curl https://kotano.github.io/pikachu_test.tp

lint:
	poetry run flake8 gendiff

check: lint
	pytest -vv --strict

download:
	@echo 'Downloading package from "test.pypi.org"'
	pip install -i https://test.pypi.org/simple/ kotano-gendiff --upgrade

uninstall:
	pip uninstall kotano-gendiff
