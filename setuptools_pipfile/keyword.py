from collections.abc import Mapping
from pathlib import Path
from .pipfile import Pipfile


def use_pipfile(dist, attr, value):
    if not value:
        return

    path = 'Pipfile'
    interpolate = True
    extras = False
    pythons = False
    indexes = None

    if isinstance(value, Mapping):
        path = value.get('path', path)
        interpolate = value.get('interpolate', interpolate)
        extras = value.get('extras', extras)
        pythons = value.get('pythons', pythons)
        indexes = value.get('indexes', indexes)
    elif isinstance(value, (str, Path)):
        path = value
    elif isinstance(value, int):
        extras = value
    elif hasattr(value, '__fspath__'):
        path = value

    pipfile = Pipfile(path, interpolate, pythons, extras, indexes)

    for k, v in pipfile.setup_kwargs().items():
        setattr(dist, k, v)
