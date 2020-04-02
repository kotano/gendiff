make install:
	poetry install

demo:
	make install_from_pip
	gendiff ../../ftest/before.json ../../ftest/after.json

publish_test:
	poetry config repositories.kotano-gendiff https://test.pypi.org/legacy/
	poetry publish -r kotano-gendiff

lint:
	poetry run flake8 gendiff

install_from_pip:
	pip install -i https://test.pypi.org/simple/ kotano-gendiff --upgrade

uninstall:
	pip uninstall kotano-gendiff
	rm ~/test/bin/gendiff
