import sys
import toml
import pytest
from setuptools.dist import check_requirements, check_specifier, check_extras

requires = {'python_version': '{0.major}.{0.minor}'.format(sys.version_info)}
source = [{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}]


@pytest.fixture
def pf(tmp_path):
    return tmp_path / 'Pipfile'


@pytest.fixture
def pp(tmp_path):
    return tmp_path / 'pyproject.toml'


class Spec(dict, toml.decoder.InlineTableDict):
    pass


def write_toml(p, data, dump=False):
    if dump:
        print(data)
    spec = {
        'source': source,
        'packages': {},
        'dev-packages': {},
        'requires': requires
    }
    spec.update(data)
    p.write_text(toml.dumps(spec, toml.TomlPreserveInlineDictEncoder()))
    if dump:
        print(p.read_text())


def write_pyproject(p, data, dump=False):
    if dump:
        print(data)
    spec = {
        'build-system': {
            'requires': ["setuptools", "wheel"],
            'build-backend': "setuptools.build_meta",
        },
        'tool': {'setuptools-pipfile': data},
    }
    p.write_text(toml.dumps(spec, toml.TomlPreserveInlineDictEncoder()))
    if dump:
        print(p.read_text())


class Dist(dict):
    def __setattr__(self, key, value):
        if value:
            if key == 'python_requires':
                check_specifier(self, key, value)
            elif key in ('install_requires', 'tests_require'):
                check_requirements(self, key, value)
            elif key == 'extras_require':
                check_extras(self, key, value)
        self[key] = value


@pytest.fixture
def dist():
    d = Dist()
    return d
