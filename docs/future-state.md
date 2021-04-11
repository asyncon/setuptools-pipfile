# Future State

While there is no current plan to develop this further, the future is always changing.
If pipenv and the Pipfile implements a different way to do something this will change with it.
That being said any breaking changes will be accompanied by a major version increment.

To ensure future compatibility either:

- make sure dependency on this package has an upper bounds on the major version
- or explicitly set all configuration options.

For example to enable extras style 1 and hard set all the current defaults

=== "pyproject.toml"

    ```toml
    [tool.setuptools-pipfile]
    path = "Pipfile"
    interpolate = false
    pythons = false
    extras.style = 1
    extras.table = "extra"
    ```

=== "setup.py"

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
