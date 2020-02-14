#!/usr/bin/env python3
# -*- mode:python; tab-width: 4; coding: utf-8 -*-
from __future__ import print_function
from os.path import (
    abspath,
    dirname)
from setuptools import (
    setup,
    find_packages)

CURDIR = abspath(dirname(__file__))
NAMESPACE = []
PACKAGE = 'objectify'
PROJECT_NAME = 'py{}'.format(PACKAGE)
DESCRIPTION = 'A package containing common reusable functions and classes'
URL = 'https://github.com/mzpqnxow/objectify'
EMAIL = 'copyright@mzpqnxow'
AUTHOR = 'mzpqnxow'
LICENSE = 'BSD 3-Clause'
REQUIRED = ['jinja2', 'ujson']

NAME = '.'.join(NAMESPACE + [PROJECT_NAME])
ABOUT = {}
VERSION_LIST = ['0', '0', '1']
VERSION = '.'.join(VERSION_LIST)

setup(
    version=VERSION,
    name=NAME,
    packages=find_packages(),
    install_requires=REQUIRED,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL)
