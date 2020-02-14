"""Simple 'raw' read/write functions with basic exception handling"""

from objectify import _DEFAULT_ENCODING, error, error_frame
from ujson import dump


def objectify_read(path_or_stream,
                   encoding=_DEFAULT_ENCODING):
    """Wrapper to return str or bytes from a file or stream

    path_or_stream: can be a readable stream-like object or a file path

    """
    reader = getattr(path_or_stream, 'read', None)
    try:
        with (path_or_stream if reader else open(path_or_stream, 'r', encoding=encoding)) as infd:
            return infd.read()
    except OSError as err:
        error_frame('Problem reading from file')
        error('OSError({0}): {1}'.format(err.errno, err.strerror))
    except Exception as err:
        error_frame(repr(err))
        exit(1)


def objectify_write(path_or_stream,
                    buf,
                    as_json=False,
                    encoding=_DEFAULT_ENCODING):
    """Wrapper to write str or bytes to a file or stream

    path_or_stream: can be a writable stream-like object or a file path

    """
    writer = getattr(path_or_stream, 'write', None)
    try:
        with (path_or_stream if writer else open(path_or_stream, 'w', encoding=encoding)) as infd:
            if as_json is True:
                try:
                    return dump(buf, infd)
                except Exception as err:
                    error_frame('Unable to write JSON to file, invalid JSON?')
                    exit(1)
            return infd.write(buf)
    except OSError as err:
        error_frame('Problem writing to file')
        error('OSError({0}): {1}'.format(err.errno, err.strerror))
    except Exception as err:
        error_frame(repr(err))
        exit(1)
