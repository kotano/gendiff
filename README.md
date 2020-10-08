# Gendiff

Gendiff is a tool that can compare two files.

[![Maintainability](https://api.codeclimate.com/v1/badges/087a56ccfee9a94dfdd7/maintainability)](https://codeclimate.com/github/kotano/python-project-lvl2/maintainability)
[![Build Status](https://travis-ci.org/kotano/python-project-lvl2.svg?branch=master)](https://travis-ci.org/kotano/python-project-lvl2)
[![Test Coverage](https://api.codeclimate.com/v1/badges/087a56ccfee9a94dfdd7/test_coverage)](https://codeclimate.com/github/kotano/python-project-lvl2/test_coverage)
[![Github Actions Status](https://github.com/kotano/python-project-lvl2/workflows/Upload%20to%20PyPi/badge.svg)](https://github.com/kotano/python-project-lvl2/actions)

## Installation

```sh
pip install -i https://test.pypi.org/simple/ kotano-gendiff
```

## Usage

---

### Basic usage

```sh
gendiff path/to/file1  path/to/file2
```

[![asciicast](https://asciinema.org/a/AVgGlJJXhj1JoClK6KmxcxUF9.svg)](https://asciinema.org/a/AVgGlJJXhj1JoClK6KmxcxUF9)

### Yaml support

[![asciicast](https://asciinema.org/a/lWCwN8RkgighGdMM4ceYKUwnU.svg)](https://asciinema.org/a/lWCwN8RkgighGdMM4ceYKUwnU)

### Plain format

[![asciicast](https://asciinema.org/a/vS3iC2fOXj9PmFjBcGu202lTn.svg)](https://asciinema.org/a/vS3iC2fOXj9PmFjBcGu202lTn)

### Json format

[![asciicast](https://asciinema.org/a/y2bGBKVY9VbewMB40556Nub0D.svg)](https://asciinema.org/a/y2bGBKVY9VbewMB40556Nub0D)

## Contributing

### Adding new view

Views folder is made to add new views to Gendiff.

To add new view you should create new module in views folder.
It's name will be collected by `cli` automatically.

Inside that module you have to add function called 'modulename + _view', i.e. `plain_view` for plain module.

After you finished creating your view, add corresponding code to views.\_\_init__.render function.
