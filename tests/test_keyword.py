from setuptools_pipfile.keyword import use_pipfile
from conftest import Spec, write_toml, requires, source


def test_default(pf, dist):
    write_toml(pf, {
        'packages': {'requests': '*'},
        'dev-packages': {'setuptools': '>=41.0.0'},
    })
    use_pipfile(dist, 'use_pipfile', pf)
    assert dist == {
        'install_requires': ['requests'],
        'tests_require': ['setuptools>=41.0.0']
    }


def test_extras_style_one(pf, dist):
    write_toml(pf, {
        'extra': {
            'socks': {
                'requests': Spec({'extras': ['socks'], 'version': '*'}),
            },
        },
    })
    use_pipfile(dist, 'use_pipfile', {'path': pf, 'extras': True})
    assert dist == {
        'extras_require': {
            'socks': ['requests[socks]'],
        },
    }


def test_extras_style_two(pf, dist):
    write_toml(pf, {
        'extra': [
            {
                'name': 'socks',
                'packages': {
                    'requests': Spec({'extras': ['socks'], 'version': '*'}),
                }
            }
        ]
    })
    use_pipfile(dist, 'use_pipfile', {'path': pf, 'extras': {'style': 2}})
    assert dist == {
        'extras_require': {
            'socks': ['requests[socks]'],
        }
    }


def test_extras_style_three(pf, dist):
    write_toml(pf, {
        'dev-packages': {
            'coverage': Spec({'extras': ['toml'], 'version': '*'}),
        }
    })
    use_pipfile(dist, 'use_pipfile', {'path': pf, 'extras': 3})
    assert dist == {
        'extras_require': {
            'dev': ['coverage[toml]'],
        },
        'tests_require': ['coverage[toml]'],
    }


def test_python_requires(pf, dist):
    write_toml(pf, {})
    use_pipfile(dist, 'use_pipfile', {'path': pf, 'pythons': True})
    assert dist == {
        'python_requires': '=={0}'.format(requires['python_version'])
    }


def test_complex_dependencies(pf, dist):
    write_toml(pf, {
        "source": source + [
            {'name': 'test', 'url': 'https://test.pypi.org/simple', 'verify_ssl': True}
        ],
        "dev-packages": {
            "records": ">0.5.0",
            "requests": Spec({
                "version": "*",
                "extras": [
                    "socks"
                ]
            }),
            "django": Spec({
                "git": "https://github.com/django/django.git",
                "ref": "1.11.4",
                "editable": True
            }),
            "e682b37": Spec({
                "file": "https://github.com/divio/django-cms/archive/release/3.4.x.zip"
            }),
            "e1839a8": Spec({
                "path": ".",
                "editable": True
            }),
            "pywinusb": Spec({
                "version": "*",
                "sys_platform": "== 'win32'",
                "index": "test"
            }),
            "unittest2": Spec({
                'version': ">=1.0,<3.0",
                'markers': "python_version < '2.7.9' or (python_version >= '3.0' and python_version < '3.4')",
                'os_name': "== 'nt'"
            })
        }
    })
    use_pipfile(dist, 'use_pipfile', pf)
    assert dist == {
        'tests_require': [
            'django @ git+https://github.com/django/django.git@1.11.4#egg=django',
            'e682b37 @ https://github.com/divio/django-cms/archive/release/3.4.x.zip',
            "pywinusb ; sys_platform == 'win32'",
            'records>0.5.0',
            'requests[socks]',
            "unittest2>=1.0,<3.0 ; (python_version < '2.7.9' or (python_version >= '3.0' and python_version < '3.4')) and os_name == 'nt'",
        ],
        'dependency_links': ['https://test.pypi.org/simple/pywinusb/']
    }


def test_use_pipfile_unset(dist):
    use_pipfile(dist, 'use_pipfile', None)
    assert dist == {}
