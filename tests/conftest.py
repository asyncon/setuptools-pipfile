import sys
import toml
import pytest

requires = {'python_version': '{0.major}.{0.minor}'.format(sys.version_info)}
source = [{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}]


@pytest.fixture
def pf(tmp_path):
    return tmp_path / 'Pipfile'


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


class Options:
    def __init__(self, d):
        self.__dict__['_d'] = d
    def __setattr__(self, key, value):
        self._d[key] = value


class Dist(dict):
    def __init__(self):
        super().__init__()
        self.options = Options(self)


@pytest.fixture
def dist():
    d = Dist()
    return d
