#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
flasktestapp: setup script

Copyright 2016, Wes Turner
License: BSD 3-Clause
"""
import sys
import flasktestapp
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


setup(
    name='flasktestapp',
    version=flasktestapp.__version__,
    description="A Flask app for learning Flask",
    long_description=open("README.rst").read(),
    author='Wes Turner',
    author_email='wes@wrd.nu',
    url="https://github.com/westurner/flasktestapp",
    license='BSD 3-Clause',
    classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
    ],
    zip_safe=False,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    install_requires=[
      "Flask"
        ,
      "MarkupSafe",
      "Werkzeug",
      "Jinja2",
      "itsdangerous",
      "click",

      "SQLAlchemy",
      # "psycopg2",
      "alembic",
      "Flask-SQLAlchemy",
      "flask-migrate",

      "Flask-Login",
      "Flask-Bcrypt",

      "Flask-WTF",
      "WTForms",

      "Flask-Babel", "Flask-Admin",
      "Flask-Script",

      "Flask-Caching",
      "Flask-Assets",
      "jsmin",
      "cssmin",

      "factory-boy",
      "fake-factory", # -> "faker"

      # NOTE!
      "flask-debugtoolbar"
    ],
    # pip install -r requirements/dev.txt
    # tests_require=["pytest", "webtest", "factory-boy", "fake-factory"],
    cmdclass={'test': PyTest},
    entry_points={
        "console_scripts": ["flasktestapp-manage = flasktestapp.manage:main"],
        "paste.app_factory": ["main = flasktestapp.app:app_factory"],
        "flask.commands": [
            "clean = flasktestapp.commands:clean",
            "factories = flasktestapp.commands:factories",
            "lint = flasktestapp.commands:lint",
            "test = flasktestapp.commands:test",
            "urls = flasktestapp.commands:urls",
        ]
    },
)
