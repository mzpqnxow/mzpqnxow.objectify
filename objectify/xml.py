#!/usr/bin/env python3
"""Convert XML to a native Python dict object as accurately as possible

Based on https://github.com/hay/xml_to_json

This is an imperfect science, but the chosen implementation should work
for your purposes. It was tested on a limited corpus of XML files

It is trivial to use XML parsing libraries to create a workable in-memory
XML object, using the xml library. It is a bit more work to create a workable
in-memory Python3 native-object (dict)

Useful for:
  - Working with XML data usng Python native types, directly
  - Converting an XML stream into a JSON stream

Beware of memory pressure on extremely large XML files!
"""
from sys import argv
from collections import OrderedDict
import xml.etree.cElementTree as ET

from objectify.io import (
    objectify_read,
    objectify_write)


def _elem_to_internal(element,
                      strip_ns=True,
                      strip_whitespace=True,
                      skip_tails=('#', ),
                      skip_text=('\n', )):
    """Convert an Element into a native Python dictionary"""
    def _strip_tag(tag):
        """Strip a tag out of brackets"""
        strip_ns_tag = tag
        split_array = tag.split('}')
        if len(split_array) > 1:
            strip_ns_tag = split_array[1]
            tag = strip_ns_tag
        return tag

    cur_dict = OrderedDict()
    elem_tag = element.tag
    if strip_ns is True:
        elem_tag = _strip_tag(element.tag)
    for key, value in list(element.attrib.items()):
        cur_dict['@' + key] = value

    # Merge sub-elements
    for sub_element in element:
        cur_val = _elem_to_internal(
            sub_element, strip_ns=strip_ns, strip_whitespace=strip_whitespace)

        tag = sub_element.tag
        if strip_ns is True:
            tag = _strip_tag(sub_element.tag)

        value = cur_val[tag]

        try:
            # add to existing list for this tag
            cur_dict[tag].append(value)
        except AttributeError:
            # turn existing entry into a list
            cur_dict[tag] = [cur_dict[tag], value]
        except KeyError:
            # add a new non-list entry
            cur_dict[tag] = value
    text = element.text
    tail = element.tail
    if strip_whitespace is True:
        # Remove whitespace from both ends
        if text:
            text = text.strip()
        if tail:
            tail = tail.strip()

    if tail and not tail not in skip_tails:
        # Use tail unless it is in blacklisted skip list
        cur_dict['#tail'] = tail

    if cur_dict:
        # Use #text element if other attributes exist and text
        # is not a blacklisted value
        if text and text not in skip_text:
            cur_dict["#text"] = text
    else:
        # Text is the value if no attributes
        cur_dict = text or None
    return {elem_tag: cur_dict}


def objectify_xml(path_buf_stream, strip_ns=False, strip_whitespace=True):
    """Convert an XML string into a Python dict suitable for JSON"""
    def _elem2json(elem, strip_ns=True, strip_whitespace=True):
        """Convert an ElementTree or Element into a JSON string"""
        if hasattr(elem, 'getroot'):
            elem = elem.getroot()
        return _elem_to_internal(elem,
                                 strip_ns=strip_ns,
                                 strip_whitespace=strip_whitespace)

    xmlstring = objectify_read(path_buf_stream)

    elem = ET.fromstring(xmlstring)
    return _elem2json(
        elem, strip_ns=strip_ns, strip_whitespace=strip_whitespace)


def main():
    """Test driver"""
    strip_line_endings = False
    infile = argv[1]
    outfile = '{}.json'.format(argv[1])
    buf = objectify_read(infile)

    if strip_line_endings is True:
        buf = buf.replace('\n', '').replace('\r', '')

    obj = objectify_xml(buf)
    objectify_write(outfile, obj, as_json=True)
    print('Conversion complete, please see {} ...'.format(outfile))


if __name__ == "__main__":
    main()
