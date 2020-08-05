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

To understand why this isn't enabled by default see [Advanced Usage](#advanced-usage).

## Basic Usage

Add `setuptools-pipfile` to setup_requires and `use_pipfile=True` in your setup.py.

This assumes that the Pipfile is in the same file directory as setup.py.

If the Pipfile is located elsewhere you can set `use_pipfile` to a path relative to setup.py.

## Advanced Usage

These are features that aren't currently provided by [pipenv](https://pypi.org/project/pipenv/) but hope they will be in the future.

To enable advanced mode simply provide a dict of options to `use_pipfile`.

### Pipfile Path

To change the path in advanced mode simply set the path key 

```python
setup(use_pipfile={'path': 'src/Pipfile'})
```

### Environment Variable Interpolation

If this pipenv feature is required for some reason it can reenabled by setting the interpolate key.

```python
setup(use_pipfile={'interpolate': True})
```

Note that if interpolation is enabled all index urls will have their basic auth
credentials stripped to prevent them from being populated into package metadata.

### Disabling Custom Index Dependency Links

To disable the population of custom index dependency links simply set the indexes key.

```python
setup(use_pipfile={'indexes': False})
```

To set hard set these as a direct urls in `install_requires` and `tests_require` against the [pep440][pep440] advice.

[pep440]: https://www.python.org/dev/peps/pep-0440/#direct-references

```python
setup(use_pipfile={'indexes': True})
```

### Populate Python Requires

Pipfile currently locks to a specific minor version. This is copied to Pipfile.lock. 
A better behaviour would be to allow defining a range of permissible versions. 
Then upon running `pipenv install` a concreate version is locked into Pipfile.lock.

To enable this in the future set the pythons key to `True`.

To change the key to lookup set the pythons key to an alternate format string.

```python
setup(use_pipfile={'pythons': '{0[requires][python_versions]}'})
```

### Populate Extras

This is currently not supported by Pipfile but if it does it will likely be supported in one of three ways.

#### Style One

The first and more likely style looks like so:

```toml
[extra.socks]
PySocks = {version = ">=1.5.6, !1.5.7"}
win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
```

To use the default setup for style one:

```python
setup(use_pipfile={'extras': True})
# or
setup(use_pipfile={'extras': 1})
# or
setup(use_pipfile=1)
```

To change the prefix for the table to something like `[option.socks]` use:

```python
setup(use_pipfile={'extras': {'table': 'option'}})
```

#### Style Two

The second style is based on [poetry](https://poetry.eustace.io/) syntax.

```toml
[[extra]]
name = "socks"

[extra.packages]
PySocks = {version = ">=1.5.6, !1.5.7"}
win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
```

To use the default setup for style two:

```python
setup(use_pipfile={'extras': {'style': 2}})
# or
setup(use_pipfile={'extras': 2})
# or
setup(use_pipfile=2)
```

Like style one use the `table` field to change the table prefix.

```python
setup(use_pipfile={'extras': {'style': 2, 'table': 'option'}})
```

Use the `subtable` field to change the suffix used to describe the packages.

```python
setup(use_pipfile={'extras': {'style': 2, 'subtable': 'requires'}})
```

To change the packaging suffix to something like `[extras.require]` use:

```python
setup(use_pipfile={'extras': {'style': 2, 'table': 'extras', 'subtable': 'require'}})
```

Finally to change the key used to identify the extra group use:

```python
setup(use_pipfile={'extras': {'style': 2, 'key': 'title'}})
```

This would result in:


```toml
[[extra]]
title = "socks"
```

#### Style Three

The third style is based on the Pipfile dev-packages implementation.

```toml
[socks-packages]
PySocks = {version = ">=1.5.6, !1.5.7"}
win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
```

To use style three:

```python
setup(use_pipfile={'extras': {'style': 3}})
# or
setup(use_pipfile={'extras': 3})
# or
setup(use_pipfile=3)
```

This last varient is the quickest way to make the dev packages installable.
This could be useful for testing frameworks such as tox.
Simply specify your dependencies to be `.[dev]`.

## Future State

While there is no current plan to develop this further, the future is always changing.
If pipenv and the Pipfile implements a different way to do something this will change with it.
That being said any breaking changes will be accompanied by a major version increment.

To ensure future compatibility either:

- make sure dependency on this package has an upper bounds on the major version
- or explicitly set all configuration options.

For example to enable extras style 1 and hard set all the current defaults

```python
setup(
    use_pipfile={
        'path': 'Pipfile',
        'interpolate': False,
        'pythons': False,
        'extras': {
            'style': 1,
            'table': 'extra'
        }
    }
)
```
