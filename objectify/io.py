"""Simple i/o wrappers for consistency"""
from json import (dump as json_dump, load as json_load)
from sys import (stderr, exc_info as exception_info)

_DEFAULT_ENCODING = 'ISO-8859-1'


def objectify_open(filename,
                   mode='r',
                   encoding=_DEFAULT_ENCODING,
                   readbuf=None,
                   readlines=None,
                   json_object=None,
                   strip_eol=False):
    """Wrapper for open with basic exception handling and flags to return file content

    Uses ISO-8859-1 as the default encoding, which is safe for international text
    Returns a stream when mode is read or write
    Returns bytes if get_content is True
    Returns a list of bytes if get_lines is True and get_content

    """
    assert mode[0] in 'rw'
    if len(
            list(
                filter(lambda test: test is not None,
                       (readbuf, readlines, json_object)))) > 1:
        stderr.write(
            'Internal error, buf, lines and obj are mutually exclusive!\n')
        return None
    try:
        if mode[0] == 'r' and (readbuf, readlines) == (False, False):
            return open(filename, mode, encoding=encoding)
        with open(filename, mode, encoding=encoding) as stream:
            if mode[0] == 'r':
                if readbuf:
                    return stream.read()
                elif readlines:
                    if strip_eol is True:
                        return stream.read().splitlines()
                    return stream.readlines()
                elif json_object:
                    return json_load(stream)

            if readbuf:
                return stream.write(readbuf)
            if readlines:
                return stream.writelines(readlines)
            if json_object:
                return json_dump(json_object, stream, indent=2)
    except OSError as err:
        stderr.write('Problem {0}ing "{1}"\n'.format(
            'read' if mode[0] == 'r' else 'writ', filename))
        stderr.write('OSError({0}): {1}\n'.format(err.errno, err.strerror))
        exception_info()[0]
    except ValueError as err:
        stderr.write('Problem {0}ing "{1}"\n'.format(
            'read' if mode[0] == 'r' else 'writ', filename))
        stderr.write(
            'ValueError when loading "{}", probable invalid encoding="{}"'.format(
                filename, encoding))
        exception_info()[0]
    raise RuntimeError('Out of logic, sorry')
