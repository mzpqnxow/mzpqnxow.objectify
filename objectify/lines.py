"""Nonsense"""
from io import StringIO

from objectify.encoding import _DEFAULT_ENCODING


def objectify_lines(path_or_stream,
                    encoding=_DEFAULT_ENCODING,
                    from_string=False, comment=None, unique=False):
    """Return a native Python object from a JSON file path, stream or string

    This function is specifically to minimize memory usage, suitable for processing
    VERY large files without causing memory pressure by implementing as a generator
    providing a single line at a time back to the caller. If this caller wants a
    list all at once they can just wrap `list()` around the all, or just a list
    or set comprehension, but this defeats the purpose of the function

    in: path_or_stream:
      (str) A string file path containing JSON
      (stream) An open readable stream from a file containing JSON
      (stream) A string of JSON content (also requires `from_string=True`)

    Note that only two comment usages are supported:
      - Comment at beginning of line, skip entire line
      - Single comment, ignore all content after comment character

    Comments *must* be a single character, e.g. '#', NOT '<!', etc
    By default, there is no comment defined unless `comment` is set by the caller

    Examples:

      for obj in objectify_lines('file.json', encoding='utf-8'):
        print(line)

      lines_fd = open('lines.lst', 'r', encoding='utf-8')
      for line in objectify_lines(json_fd):
        print(line)

      lines_str = 'a\nb\nc'
        for line in objectify_lines(lines_str, from_string=True):
          print(line)

    If the caller just wants a simple list of lines all in memory at once without
    any concern for memory pressure simply call with a list() or use a set or list
    comprehension:

    Build one large list all at once:
      list(objectify_lines('file.lst', encoding='utf-8'))

    Alternately, use a list comprehension for transforming lines along the way:
      [line.upper() for line in objectify_lines('file.lst', encoding='utf-8')]

    To perform an unique, use a set comprehension:
      {line.lower() for line in objectify_lines('file.lst', encoding='utf-8')}
    """
    if from_string is True:
        # If caller specifies path_or_stream is a string, turn it into
        # a stream to avoid an extra set of logic below
        assert isinstance(path_or_stream, str)
        path_or_stream = StringIO(path_or_stream)

    # If path_or_stream has a read method, it is effectively stream
    reader = getattr(path_or_stream, 'read', None)

    with (path_or_stream if reader else open(path_or_stream, 'r', encoding=encoding)) as infd:
        if unique is False:
            for line in infd.readlines():
                line = line.strip()
                if comment:
                    if line[0] == comment:
                        continue
                    comment_loc = line.rfind(comment)
                    line = line[0:comment_loc].strip()
                yield line
