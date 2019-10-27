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

    if isinstance(value, Mapping):
        path = value.get('path', path)
        interpolate = value.get('interpolate', interpolate)
        extras = value.get('extras', extras)
        pythons = value.get('pythons', pythons)
    elif isinstance(value, (str, Path)):
        path = value

    pipfile = Pipfile(path, interpolate, pythons, extras)

    for k, v in pipfile.setup_kwargs().items():
        setattr(dist.options, k, v)
