"""Provide a clean, simple but flexible way to load JSON and JSON-lines files

To write JSON, use objectify_write with as_json=True

"""
from io import StringIO

from ujson import loads, load

from objectify.log import error
from objectify.encoding import _DEFAULT_ENCODING


def objectify_json(path_buf_stream,
                   encoding=_DEFAULT_ENCODING,
                   from_string=False,
                   ensure_ascii=False,
                   encode_html_chars=False):
    """Return a native Python object from a JSON file path, stream or string"""
    if from_string is True:
        path_buf_stream = StringIO(path_buf_stream)

    read = getattr(path_buf_stream, 'read', None)

    if read is not None:
        return load(read(), ensure_ascii=ensure_ascii, encode_html_chars=encode_html_chars)
    with open(path_buf_stream, encoding=encoding) as infd:
        try:
            return load(infd, ensure_ascii=ensure_ascii, encode_html_chars=encode_html_chars)
        except Exception as err:
            error(repr(err))


def objectify_json_lines(path_buf_stream,
                         from_string=False,
                         fatal_errors=True,
                         encoding=_DEFAULT_ENCODING,
                         ensure_ascii=False,
                         encode_html_chars=False):
    """Generator return an object for each line of JSON in a file, stream or string

    in: path_buf_stream:
      (str) A string file path containing JSON
      (stream) An open readable stream from a file containing JSON
      (stream) A string of JSON content (also requires `from_string=True`)

    This function intentionally operates as a generator, to avoid using huge
    amounts of memory when loading a very large file- afterall, this is the
    primary benefit of the JSON lines format. It is meant to be called many
    times in succession, sometimes up to millions of times, so it is important
    that it is relatively quick/simple.

    There are three ways to invoke this function
    Each of them returns a native Python object

    for obj in objectify_json_lines('file.json'):
        print(obj.items())

    json_fd = open('file.json', 'r', encoding='utf-8')
    for obj in objectify_json_lines(json_fd):
        print(obj.items())

    json_str = '{"A": "B"}\n{"C": "D"}'
    for obj in objectify_json_lines(json_str, from_string=True):
        print(obj.items())
    """
    if from_string is True:
        # If caller specifies path_buf_stream is a string, turn it into
        # a stream to avoid an extra set of logic below
        assert isinstance(path_buf_stream, str)
        path_buf_stream = StringIO(path_buf_stream)

    # If path_buf_stream has a read method, it is effectively stream
    reader = getattr(path_buf_stream, 'read', None)

    with (path_buf_stream if reader else open(path_buf_stream, 'r', encoding=encoding)) as infd:
        for line in infd.readlines():
            line = line.strip()
            # Exception handlers are expensive to set up and even more expensive
            # when they fire. If errors should be fatal, don't bother setting one
            # up at all
            if fatal_errors is True:
                yield loads(line, ensure_ascii=ensure_ascii, encode_html_chars=encode_html_chars)
            else:
                # The more expensive path, preparing to catch an exception and
                # continue gracefully if fatal_errors is False
                try:
                    yield loads(line, ensure_ascii=ensure_ascii, encode_html_chars=encode_html_chars)
                except Exception as err:
                    error('bad JSON-line line: {}'.format(repr(err)))
                    continue
