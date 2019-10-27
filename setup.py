import setuptools

from setuptools_pipfile.pipfile import Pipfile

setuptools.setup(
    use_scm_version=True,
    **Pipfile('Pipfile').setup_kwargs()
)
