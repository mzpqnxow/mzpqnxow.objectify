"""Simple 'raw' read/write functions with basic exception handling"""

from objectify.encoding import _DEFAULT_ENCODING
from objectify.log import error, error_frame
from ujson import dump


def objectify_read(path_buf_stream,
                   encoding=_DEFAULT_ENCODING):
    """Wrapper to return str or bytes from a file or stream

    path_buf_stream: can be a readable stream-like object or a file path

    """
    reader = getattr(path_buf_stream, 'read', None)
    try:
        with (path_buf_stream if reader else open(path_buf_stream, 'r', encoding=encoding)) as infd:
            buf = infd.read()
            return buf
    except OSError as err:
        error_frame('Problem reading from file')
        error('OSError({0}): {1}'.format(err.errno, err.strerror))
    except Exception as err:
        error_frame(repr(err))
        exit(1)


def objectify_write(path_buf_stream,
                    buf,
                    as_json=False,
                    encoding=_DEFAULT_ENCODING):
    """Wrapper to write str or bytes to a file or stream

    path_buf_stream: can be a writable stream-like object or a file path

    """
    writer = getattr(path_buf_stream, 'write', None)
    try:
        with (path_buf_stream if writer else open(path_buf_stream, 'w', encoding=encoding)) as infd:
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
