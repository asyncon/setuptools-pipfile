import os
import toml
from collections.abc import Mapping, Iterable
from distutils.errors import DistutilsSetupError, DistutilsFileError

setup_fields = (
    'install_requires',
    'tests_require',
    'dependency_links',
    'extras_require',
    'python_requires',
)

url_keys = {
    'path',
    'file',
    'git',
    'svn',
    'hg',
    'bzr',
    'uri',
}

marker_keys = {
    'implementation_name',
    'implementation_version',
    'os_name',
    'platform_machine',
    'platform_python_implementation',
    'platform_release',
    'platform_system',
    'platform_version',
    'python_full_version',
    'python_version',
    'sys_platform',
}

other_keys = {
    'editable',
    'extras',
    'index',
    'markers',
    'ref',
    'version',
}


def clone_config(cfg, interpolate=False):
    if isinstance(cfg, Mapping):
        return {k: clone_config(v) for k, v in cfg.items()}
    elif isinstance(cfg, str):
        return os.path.expandvars(cfg) if interpolate else cfg
    elif isinstance(cfg, Iterable):
        return [clone_config(i) for i in cfg]
    else:
        return cfg


class Dependency(dict):
    def __init__(self, name, data):
        data = {'version': data} if isinstance(data, str) else data
        super().__init__(data)
        self['name'] = name

    @property
    def name(self):
        return self['name']

    @property
    def url(self):
        keys = list(url_keys & self.keys())
        if not keys:
            return ''
        if len(keys) > 1:
            raise DistutilsSetupError(
                'Pipfile Dependency[{0}] conflict: {1!r}'.format(
                    self.name, keys))
        if 'version' in self:
            raise DistutilsSetupError(
                'Pipfile Dependency[{0}] conflict: {1!r}'.format(
                    self.name, ['version'] + keys))
        url = keys[0]
        if url in ('git', 'svn', 'hg', 'bzr'):
            url = '{0}+{1}'.format(url, self[url])
        else:
            url = self[url]
        if 'ref' in self:
            url = '{0}@{1[ref]}#egg={1.name}'.format(url, self)
        return ' @ {0}'.format(url)

    @property
    def extras(self):
        if 'extras' in self:
            return '[{0}]'.format(','.join(self['extras']))
        return ''

    @property
    def specifier(self):
        if 'version' in self:
            if self['version'] != '*':
                return self['version']
        return ''

    @property
    def marker(self):
        markers = self.get('markers', '')
        keys = ['{} {}'.format(k, self[k]) for k in marker_keys & self.keys()]
        if not keys and not markers:
            markers = ''
        elif keys and markers:
            markers = ' and '.join([' ; ({0})'.format(markers)] + keys)
        elif not markers:
            markers = ' ; ' + ' and '.join(keys)
        return markers

    def __str__(self):
        return '{0.name}{0.extras}{0.specifier}{0.url}{0.marker}'.format(self)


class Pipfile(dict):

    def __init__(self, path, interpolate=False, pythons=False, extras=False):
        self.interpolate = interpolate
        self.extras = {'table': 'extra', 'key': 'name', 'subtable': 'packages'}

        if extras is True:
            pass
        elif isinstance(extras, str):
            self.extras['table'] = extras
        elif isinstance(extras, Mapping):
            self.extras.update(extras)
        else:
            self.extras['table'] = None

        if pythons is True:
            self.pythons = '{0[requires][python_version]}'
        else:
            self.pythons = pythons

        if isinstance(path, Mapping):
            data = path
            self.path = 'Pipfile'
        else:
            self.path = path
            if not os.path.exists(path):
                raise DistutilsFileError(
                    'Pipfile missing {0}'.format(os.path.abspath(path)))

            with open(self.path, 'r') as fp:
                data = toml.load(fp)

        super().__init__(clone_config(data, interpolate))

    def not_dot(self, spec):
        return isinstance(spec, str) or spec.get('path') != '.'

    def get_deps(self, table):
        return [Dependency(k, v) for k, v in table.items() if self.not_dot(v)]

    @property
    def deps(self):
        return self.get_deps(self.get('packages', {}))

    @property
    def dev_deps(self):
        return self.get_deps(self.get('dev-packages', {}))

    @property
    def extra_deps(self):
        if self.extras.get('style', 1) != 2:
            return {
                k: self.get_deps(v)
                for k, v in self.get(self.extras['table'], {}).items()
            }
        return {
            e[self.extras['key']]: self.get_deps(e[self.extras['subtable']])
            for e in self.get(self.extras['table'], [])
        }

    @property
    def all_deps(self):
        return self.deps + self.dev_deps + [
            d for deps in self.extra_deps.values() for d in deps
        ]

    @property
    def install_requires(self):
        return [str(p) for p in self.deps]

    @property
    def tests_require(self):
        return [str(d) for d in self.dev_deps]

    @property
    def dependency_links(self):
        indexes = {d['index'] for d in self.all_deps if 'index' in d}
        return sorted(s['url'] for s in self['source'] if s['name'] in indexes)

    @property
    def extras_require(self):
        if not self.extras['table']:
            return None
        return {k: [str(d) for d in v] for k, v in self.extra_deps.items()}

    @property
    def python_requires(self):
        if not isinstance(self.pythons, str):
            return None
        return self.pythons.format(self)

    def setup_kwargs(self):
        return {
            k: v for k, v in (
                (key, getattr(self, key)) for key in setup_fields
            ) if v
        }
