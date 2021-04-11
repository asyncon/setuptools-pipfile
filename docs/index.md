# Overview

Setuptools-pipfile provides a way to dynamically link a setuptools dependency
configuration to the Pipfile managed by [Pipenv](https://pipenv.pypa.io/).

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

To understand why this isn't enabled by default see [Advanced Usage](config-advanced).
