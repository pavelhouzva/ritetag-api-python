import os
import sys
import setuptools

from setuptools.command.test import test as TestCommand

cwd = os.path.abspath(os.path.dirname(__file__))
version_info = {}

with open(os.path.join(cwd, 'ritetag', '__version__.py'), 'r') as f:
    exec(f.read(), version_info)

with open("README.md", "r") as fh:
    long_description = fh.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    os.system('rm -r dist/*')
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()

setuptools.setup(
    name=version_info['__name__'],
    version=version_info['__version__'],
    author=version_info['__author__'],
    author_email=version_info['__email__'],
    description=version_info['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=version_info['__url__'],
    packages=['ritetag'],
    tests_require=[
        'pytest'
    ],
    requires=[
        'requests'
    ],
    test_suite="tests",
    cmdclass={'test': PyTest},
    scripts=['bin/ritetag-api'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires=">=2.7",
)
