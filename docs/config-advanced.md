# Advanced Usage

These are features that aren't currently provided by [pipenv](https://pypi.org/project/pipenv/) but hope they will be in the future.

To enable advanced mode simply provide a dict of options.

## Pipfile Path

To change the path in advanced mode simply set the path key.

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    path = "src/Pipfile"
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'path': 'src/Pipfile'})
    ```

## Environment Variable Interpolation

If this pipenv feature is required for some reason it can reenabled by setting the interpolate key.

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    interpolate = true
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'interpolate': True})
    ```

Note that if interpolation is enabled all index urls will have their basic auth
credentials stripped to prevent them from being populated into package metadata.

## Disabling Custom Index Dependency Links

To disable the population of custom index dependency links simply set the indexes key.

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    indexes = false
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'indexes': False})
    ```

To hard set these as a direct urls in `install_requires` and `tests_require`
against the [pep440][pep440] advice set to `True`.

[pep440]: https://www.python.org/dev/peps/pep-0440/#direct-references

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    indexes = true
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'indexes': True})
    ```

## Populate Python Requires

Pipfile currently locks to a specific minor version. This is copied to Pipfile.lock. 
A better behaviour would be to allow defining a range of permissible versions. 
Then upon running `pipenv install` a concreate version is locked into Pipfile.lock.

To enable this in the future set the pythons key to `True`.

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    pythons = true
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'pythons': True})
    ```

### Alternative Formatting

To change the key to lookup set the pythons key to an alternate format string.

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    pythons = "{0[requires][python_versions]}"
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'pythons': '{0[requires][python_versions]}'})
    ```

## Populate Extras

This is currently not supported by Pipfile but if it does it will likely be supported in one of three ways.

### Style One

The first and more likely style looks like so:

```toml
[extra.socks]
PySocks = {version = ">=1.5.6, !1.5.7"}
win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
```

To use the default setup for style one:

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extras = true
    # or
    [tool.setuptools-pipfile]
    extras = 1
    # or
    [tool]
    setuptools-pipfile = 1
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': True})
    # or
    setup(use_pipfile={'extras': 1})
    # or
    setup(use_pipfile=1)
    ```

#### Rename Table

To change the prefix for the table to something like `[option.socks]` use:

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extras.table = "option"
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': {'table': 'option'}})
    ```

=== "Pipfile"

    ```toml
    [[option]]
    name = "socks"

    [option.packages]
    PySocks = {version = ">=1.5.6, !1.5.7"}
    win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
    ```

### Style Two

The second style is based on [poetry](https://poetry.eustace.io/) syntax.

```toml
[[extra]]
name = "socks"

[extra.packages]
PySocks = {version = ">=1.5.6, !1.5.7"}
win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
```

To use the default setup for style two:

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extras = 2
    # or
    [tool]
    setuptools-pipfile = 2
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': {'style': 2}})
    # or
    setup(use_pipfile={'extras': 2})
    # or
    setup(use_pipfile=2)
    ```

#### Rename Table

Like style one use the `table` field to change the table prefix.

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extras.style = 2
    extras.table = option
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': {'style': 2, 'table': 'option'}})
    ```

=== "Pipfile"

    ```toml
    [[option]]
    name = "socks"

    [option.packages]
    PySocks = {version = ">=1.5.6, !1.5.7"}
    win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
    ```

#### Rename Subtable

Use the `subtable` field to change the suffix used to describe the packages.

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extra.style = 2
    extra.subtable = "requires"
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': {'style': 2, 'subtable': 'requires'}})
    ```

=== "Pipfile"

    ```toml
    [[extra]]
    name = "socks"

    [extra.requires]
    PySocks = {version = ">=1.5.6, !1.5.7"}
    win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
    ```

#### Change naming key

Finally to change the key used to identify the extra group use:

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extras.style = 2
    extras.key = "title"
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': {'style': 2, 'key': 'title'}})
    ```

=== "Pipfile"

    ```toml
    [[extra]]
    title = "socks"
    ```

#### Complete example

To change the packaging suffix to something like `[extras.require]` with a naming key of `group` use:

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extras.style = 2
    extras.key = "group"
    extras.table = "extras"
    extras.subtable = "require"
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': {'style': 2, 'table': 'extras', 'subtable': 'require'}})
    ```

=== "Pipfile"

    ```toml
    [[extras]]
    group = "socks"

    [extras.require]
    PySocks = {version = ">=1.5.6, !1.5.7"}
    win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
    ```

### Style Three

The third style is based on the Pipfile dev-packages implementation.

```toml
[socks-packages]
PySocks = {version = ">=1.5.6, !1.5.7"}
win_inet_pton = {sys_platform = "win32", python_version = "2.7"}
```

To use style three:

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    extras.style = 3
    # or
    [tool]
    setuptools-pipfile = 3
    ```

=== "setup.py"

    ```python
    setup(use_pipfile={'extras': {'style': 3}})
    # or
    setup(use_pipfile={'extras': 3})
    # or
    setup(use_pipfile=3)
    ```

This last varient is the quickest way to make the dev packages installable.
This could be useful for testing frameworks such as tox.
Simply specify your dependencies to be `.[dev]` or package install extras to `dev`.


