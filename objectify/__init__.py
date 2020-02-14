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

_DEFAULT_ENCODING = 'ISO-8859-1'
_DEBUG = True


def debug(msg):
    """Consider using error_frame"""
    stderr.write('DEBUG: {}\n'.format(msg))


def error(msg):
    """Write an error message to stderr"""
    stderr.write('ERROR: {}\n'.format(msg))


def info(msg):
    """Write an informational message to stderr"""
    stderr.write('{}\n'.format(msg))


def warn(msg):
    """Write an warning message to stderr"""
    stderr.write('WARN:  {}\n'.format(msg))


def error_frame(msg=''):
    """Print debug info

    The correct way to do this is to use the logging framework which
    exposes all of these things to you, but you can access them using
    the Python inspect module
    """
    if _DEBUG is False:
        return
    caller_frame = inspect.stack()[1]
    frame = caller_frame[0]
    frame_info = inspect.getframeinfo(frame)
    stderr.write('{}{}::{}: {}{}\n'.format(
        RED, frame_info.function, frame_info.lineno, msg, NOCOLOR))


__all__ = ['objectify_json', 'objectify_xml', 'objectify_yaml',
           'objectify_json_lines', 'objectify_read', 'objectify_write']
