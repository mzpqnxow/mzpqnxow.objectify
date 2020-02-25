#!/usr/bin/env python3
# -*- mode:python; tab-width: 4; coding: utf-8 -*-
from __future__ import print_function
import versioneer
from os.path import (
    abspath,
    dirname)
from setuptools import (
    setup,
    find_packages)

CURDIR = abspath(dirname(__file__))
NAMESPACE = ['mzpqnxow']
PACKAGE = 'objectify'
DESCRIPTION = 'A package containing common reusable functions and classes'
URL = 'https://github.com/mzpqnxow/objectify'
EMAIL = 'copyright@mzpqnxow.com'
AUTHOR = 'mzpqnxow'
LICENSE = 'BSD 3-Clause'
REQUIRED = ['jinja2', 'ujson']

NAME = '.'.join(NAMESPACE + [PACKAGE])
ABOUT = {}

# Use https://pypi.org/classifiers/ for reference
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Natural Language :: English',
    'Topic :: Software Development :: Libraries']

setup(
    version=versioneer.get_version(),
    classifiers=CLASSIFIERS,
    cmdclass=versioneer.get_cmdclass(),
    name=NAME,
    packages=find_packages(),
    install_requires=REQUIRED,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL)
