"""Nothing to see here"""
import inspect
import logging
from logging import NullHandler
from sys import stderr

from objectify.json import (
    objectify_json,
    objectify_json_lines)
from objectify.xml import objectify_xml
from objectify.yaml import objectify_yaml
from objectify.io import (
    objectify_read,
    objectify_write)

RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
NOCOLOR = '\033[1;0m'
BLUE = '\033[1;34m'

logging.getLogger(__name__).addHandler(NullHandler())

__all__ = ['objectify_json', 'objectify_xml', 'objectify_yaml',
           'objectify_json_lines', 'objectify_read', 'objectify_write']
