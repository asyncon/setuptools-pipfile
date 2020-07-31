from setuptools_pipfile.pipfile import Pipfile, DistutilsFileError, DistutilsSetupError
from conftest import Spec, write_toml, requires, source, pytest
import os


def test_default(pf):
    write_toml(pf, {
        'packages': {'requests': '*',},
        'dev-packages': {'pytest': '*',},
    })
    assert Pipfile(pf, extras={'style': 1,}).setup_kwargs() == {
        'install_requires': ['requests'],
        'tests_require': ['pytest']
    }


def test_extras_style_one():
    assert Pipfile({
        'source': source,
        'packages': {},
        'dev-packages': {},
        'option': {
            'socks': {
                'requests': Spec({'extras': ['socks'], 'version': '*'}),
            },
        },
    }, extras='option').setup_kwargs() == {
        'extras_require': {
            'socks': ['requests[socks]'],
        },
    }


def test_extras_style_two(pf):
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
    assert Pipfile(pf, extras={'style': 2,}).setup_kwargs() == {
        'extras_require': {
            'socks': ['requests[socks]'],
        }
    }


def test_extras_style_three(pf):
    write_toml(pf, {
        'dev-packages': {
            'coverage': Spec({'extras': ['toml'], 'version': '*'}),
        }
    })
    assert Pipfile(pf, extras=3).setup_kwargs() == {
        'extras_require': {
            'dev': ['coverage[toml]'],
        },
        'tests_require': ['coverage[toml]'],
    }


def test_python_requires(pf):
    write_toml(pf, {})
    assert Pipfile(pf, pythons=True).setup_kwargs() == {
        'python_requires': '=={0}'.format(requires['python_version'])
    }


def test_missing_pipfile(pf):
    with pytest.raises(DistutilsFileError):
        Pipfile(pf)


def test_multiple_urls(pf):
    write_toml(pf, {
        'packages': {
            "e682b37": Spec({
                "file": "https://github.com/divio/django-cms/archive/release/3.4.x.zip",
                "git": "https://github.com/django/django.git",
                "ref": "1.11.4",
                "editable": True
            }),
        }
    })
    with pytest.raises(DistutilsSetupError):
        Pipfile(pf).setup_kwargs()


def test_url_with_version(pf):
    write_toml(pf, {
        'packages': {
            "e682b37": Spec({
                "git": "https://github.com/django/django.git",
                "version": "1.11.4",
                "editable": True
            }),
        }
    })
    with pytest.raises(DistutilsSetupError):
        Pipfile(pf).setup_kwargs()


def test_source_url_interpolation(pf):
    write_toml(pf, {
        'source': [{
            'name': 'pypi',
            'url': '${MY_CUSTOM_PIP_URL}/simple',
            'verify_ssl': True,
        }]
    })
    os.environ['MY_CUSTOM_PIP_URL'] = 'https://pypi.example.com'
    assert Pipfile(pf, interpolate=True).sources['pypi'] == 'https://pypi.example.com/simple'
