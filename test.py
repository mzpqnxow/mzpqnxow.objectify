#!/usr/bin/env python3
from collections import OrderedDict
from sys import argv, stderr

from ujson import dumps

from objectify.xml import objectify_xml
from objectify.yaml import objectify_yaml
from objectify.json import objectify_json
from objectify.io import objectify_read, objectify_write


def main():
    """Test driver"""
    infile = argv[1]

    loadmap = {
        '.json': (objectify_json, {}),
        '.yaml': (objectify_yaml, {}),
        '.yml': (objectify_yaml, {'template': True}),
        '.xml': (objectify_xml, {})
    }

    obj = None
    for extension, handler_args in loadmap.items():
        if infile.endswith(extension):
            handler = handler_args[0]
            kwargs = handler_args[1]
            outfile = infile.replace(extension, '.json')
            # Each handler takes a string as input, not a filename
            # Each handler returns a native Python3 datatype, either
            # a dict or OrderedDict. Both types can be cleanly and
            # safely serialized to JSON, or just used in memory as a
            # standard dict
            obj = handler(infile, **kwargs)
            break
    else:
        stderr.write('Unknown extension!\n')
        exit(1)
    if obj is None:
        stderr.write('Unable to parse input file!')
        exit(1)
    if not isinstance(obj, (dict, OrderedDict)):
        stderr.write('Something went fail ...\n')
        exit(1)

    # Write JSON
    print(dumps(obj, indent=2))
    objectify_write(outfile, obj, as_json=True)
    print('Conversion complete, please see {} ...'.format(outfile))


if __name__ == "__main__":
    main()
