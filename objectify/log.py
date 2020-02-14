from sys import stderr
import inspect


def debug(msg):
    """Consider using error_frame"""
    stderr.write('DEBUG: {}\n'.format(msg))


def error(msg):
    """Write an error message to stderr"""
    stderr.write('ERROR: {}\n'.format(msg))


def info(msg):
    """Write an informational message to stderr"""
    stderr.write('{}\n'.format(msg))


def warn(msg):
    """Write an warning message to stderr"""
    stderr.write('WARN:  {}\n'.format(msg))


def error_frame(msg=''):
    """Print debug info

    The correct way to do this is to use the logging framework which
    exposes all of these things to you, but you can access them using
    the Python inspect module
    """
    caller_frame = inspect.stack()[1]
    frame = caller_frame[0]
    frame_info = inspect.getframeinfo(frame)
    stderr.write('{}::{}: {}\n'.format(frame_info.function, frame_info.lineno, msg))
