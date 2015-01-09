#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://bingen.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='bingen',
    version='0.1.0',
    description='Create binary data from text input',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Bob Forgey',
    author_email='sesamemucho@gmail.com',
    url='https://github.com/sesamemucho/bingen',
    tests_require=['pytest'],
    packages=[
        'bingen',
    ],
    cmdclass={'test': PyTest},
    package_dir={'bingen': 'bingen'},
    include_package_data=True,
    install_requires=[
    ],
    platforms='any',
    test_suite='sandman.test.test_sandman',
    license='GPLv3',
    zip_safe=False,
    keywords='bingen',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    extras_require={
        'testing': ['pytest'],
    }
)
