#!/usr/bin/env python3
"""Convert XML to a Python dict object

Based on https://github.com/hay/xml_to_json

This is an imperfect science, so testing is imperative. It should
work well enough for most purposes

It is trivial to use XML parsing libraries to create a workable
in-memory XML structure. This purpose of this library is to
create a workable in-memory Python3 native-type structure that
can be easily serialized to plain JSON (or YaML, etc)
"""
from sys import argv
from collections import OrderedDict
import xml.etree.cElementTree as ET

from objectify.io import objectify_open

_DEVELOPMENT_MODE = False  # Use to test untested functionality


def _elem_to_internal(elem,
                      strip_ns=True,
                      strip=True,
                      skip_tails=('#', ),
                      skip_text=('\n', )):
    """Convert an Element into an internal dictionary (not JSON!)."""
    def _strip_tag(tag):
        """Strip a tag out of brackets"""
        strip_ns_tag = tag
        split_array = tag.split('}')
        if len(split_array) > 1:
            strip_ns_tag = split_array[1]
            tag = strip_ns_tag
        return tag
    d = OrderedDict()
    elem_tag = elem.tag
    if strip_ns is True:
        elem_tag = _strip_tag(elem.tag)
    for key, value in list(elem.attrib.items()):
        d['@' + key] = value

    # loop over subelements to merge them
    for subelem in elem:
        v = _elem_to_internal(subelem, strip_ns=strip_ns, strip=strip)

        tag = subelem.tag
        if strip_ns is True:
            tag = _strip_tag(subelem.tag)

        value = v[tag]

        try:
            # add to existing list for this tag
            d[tag].append(value)
        except AttributeError:
            # turn existing entry into a list
            d[tag] = [d[tag], value]
        except KeyError:
            # add a new non-list entry
            d[tag] = value
    text = elem.text
    tail = elem.tail
    if strip is True:
        # ignore leading and trailing whitespace
        if text:
            text = text.strip()
        if tail:
            tail = tail.strip()

    if tail and not tail not in skip_tails:
        # Use tail unless it is in blacklisted skip list
        d['#tail'] = tail

    if d:
        # Use #text element if other attributes exist and text
        # is not a blacklisted value
        if text and text not in skip_text:
            d["#text"] = text
    else:
        # Text is the value if no attributes
        d = text or None
    return {elem_tag: d}


def objectify_xml(xmlstring, strip_ns=True, strip=True):
    """Convert an XML string into a Python dict suitable for JSON"""
    def _elem2json(elem, strip_ns=True, strip=True):
        """Convert an ElementTree or Element into a JSON string"""
        if hasattr(elem, 'getroot'):
            elem = elem.getroot()
        return _elem_to_internal(elem, strip_ns=strip_ns, strip=strip)

    assert isinstance(xmlstring, str)
    elem = ET.fromstring(xmlstring)
    return _elem2json(
        elem, strip_ns=strip_ns, strip=strip)


def main():
    """Test driver"""
    strip = False
    strip_ns = False
    strip_text = False
    strip_nl = False
    infile = argv[1]
    outfile = '{}.json'.format(argv[1])
    if True in (strip_text, strip_ns):
        strip = 1
    buf = objectify_open(infile, readbuf=True)
    if strip_nl is True:
        buf = buf.replace('\n', '').replace('\r', '')
    out = objectify_xml(buf, strip_ns, strip)
    objectify_open(outfile, 'w', json_object=out)
    print('Conversion complete, please see {} ...'.format(outfile))


if __name__ == "__main__":
    main()
