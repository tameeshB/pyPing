from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from pypingcli import __version__

from setuptools import Command, find_packages, setup

class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)

setup(
    
    name = 'pypingcli',
    version = __version__,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    url='https://github.com/tameeshB/pyPingCLI',
    author='Tameesh Biswas',
    author_email='g@tameesh.in',
    classifiers = [
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'pyping=pypingcli.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)