# setuptools-pipfile

Dependency management via Pipfile

[![Travis (.org)](https://img.shields.io/travis/asyncon/setuptools-pipfile)](https://travis-ci.org/projects/asyncon/setuptools-pipfile)
[![MIT](https://img.shields.io/pypi/l/setuptools-pipfile.svg)](https://github.com/asyncon/setuptools-pipfile/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/setuptools-pipfile.svg)](https://pypi.org/project/setuptools-pipfile/)
[![Python](https://img.shields.io/pypi/pyversions/setuptools-pipfile.svg)](https://pypi.org/project/setuptools-pipfile/)
[![Downloads](https://pepy.tech/badge/setuptools-pipfile)](https://pepy.tech/project/setuptools-pipfile)

## Overview

In basic mode setuptools-pipfile does the following:

- Populates `install_requires` from the packages table.
- Populates `tests_require` from the dev-packages table.
- Populates `dependency_links` from the source tables if needed by dependencies.

Advanced configuration can be used to control:

- The path to the Pipfile.
- Variable interpolation.
- Removing indexes from `dependency_links`.
- Activate and control populating `extras_require`.
- Control populating `python_requires`.

All documentation is located [here](https://asyncon.github.io/setuptools-pipfile/).
