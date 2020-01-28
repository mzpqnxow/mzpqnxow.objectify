"""Nothing to see here"""
import logging
from logging import NullHandler

from objectify.json import objectify_json
from objectify.xml import objectify_xml
from objectify.yaml import objectify_yaml

logging.getLogger(__name__).addHandler(NullHandler())

_DEFAULT_ENCODING = 'ISO-8859-1'

__all__ = ['objectify_json', 'objectify_xml', 'objectify_yaml']
