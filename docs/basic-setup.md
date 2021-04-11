# Setup

Setuptools-pipfile is not your regular package.
It is used by your package build system.

## Setup Configuration

!!! example "Build System Configuration"

    There are three ways to configure your build system to use setuptools-pipfile.

    === "pyproject.toml"

        ```toml
        [build-system]
        requires = ["setuptools", "wheel", "setuptools-pipfile"]
        build-backend = "setuptools.build_meta"
        ```

    === "setup.cfg"

        ```cfg
        [options]
        setup_requires =
            setuptools-pipfile
        ```

    === "setup.py"

        ```python
        import setuptools
        setuptools.setup(setup_requires='setuptools-pipfile')
        ```

The use of a `pyproject.toml` file is the preferred method as it is future of python packaging.

For more information refer to [PEP517](https://www.python.org/dev/peps/pep-0517/).

## Enable Basic Usage

Setuptools-pipfile must be enabled for it to take effect.

!!! example "Enable default behaviour"

    === "pyproject.toml"

        This is enough to enable default functionality.

        ```toml
        [tool.setuptools-pipfile]
        ``` 

    === "setup.py"

        Add `use_pipfile=True` in your setup.py.

        ```python
        import setuptools
        setuptools.setup(use_pipfile=True)
        ```

This assumes that the Pipfile is in the same file directory as setup.py.

If the Pipfile is located elsewhere you can instead set a relative path.

!!! example "Relocate Pipfile"

    === "pyproject.toml"

        ```toml
        [tool]
        setuptools-pipfile = "src/Pipfile"
        ``` 

    === "setup.py"

        ```python
        import setuptools
        setuptools.setup(use_pipfile='src/Pipfile')
        ```

Anything beyond this is considered [Advanced Usage](../config-advanced/).
