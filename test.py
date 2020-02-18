#!/usr/bin/env python3
"""Hastily written test driver

This library returns generators whenever possible, to avoid
filling up memory when loading huge line-based files. This
can't be avoided for some formats (XML, YaML, JSON) but for others
it is simple (JSON Lines, CSV, Lines, ...)

The output will always be either an array or a dict in JSON format
For line-based items, the generators may contain nearly any native
object type

"""
from collections import OrderedDict
from copy import copy
from sys import argv, stderr

from objectify.xml import objectify_xml
from objectify.yaml import objectify_yaml
from objectify.json import objectify_json, objectify_json_lines
from objectify.csv import objectify_csv
from objectify.lines import objectify_lines
from objectify.io import objectify_write


def main():
    """Test driver"""
    infile = argv[1]

    loadmap = {
        '.json': (objectify_json, {}, (dict, OrderedDict)),
        '.yaml': (objectify_yaml, {}, (dict, OrderedDict)),
        '.yml': (objectify_yaml, {'template': True}, (dict, OrderedDict)),
        '.xml': (objectify_xml, {}, (dict, OrderedDict)),
    }
    obj = None
    for extension, options in loadmap.items():
        handler = options[0]
        kwargs = options[1]
        types = options[2]
        if infile.endswith(extension):
            # Each handler takes a string as input, not a filename
            # Each handler returns a native Python3 datatype, either
            # a dict or OrderedDict. Both types can be cleanly and
            # safely serialized to JSON, or just used in memory as a
            # standard dict
            obj = handler(infile, **kwargs)
            break
    else:
        line_based_extensions = {
            '.lst': (objectify_lines, {}, (str, int, float)),
            '.jsonl': (objectify_json_lines, {}, (dict, OrderedDict)),
            '.csv': (objectify_csv, {}, (dict, OrderedDict))
        }
        for extension, options in line_based_extensions.items():
            rows = []
            if infile.endswith(extension):
                handler = options[0]
                kwargs = options[1]
                types = options[2]
                for obj in handler(infile, **kwargs):
                    if not isinstance(obj, types):
                        raise RuntimeError('unexpected!')
                    rows.append(obj)
                obj = copy(rows)
                break
    if obj is None:
        stderr.write('Unable to parse input file!')
        exit(1)

    if not isinstance(obj, (dict, list)):
        print('Not expected: {} / {}'.format(obj, types))
        exit(1)

    outfile = infile.replace(extension, '-converted.json')
    objectify_write(outfile, obj, as_json=True)
    print('Conversion complete, please see {} ...'.format(outfile))


if __name__ == "__main__":
    main()
