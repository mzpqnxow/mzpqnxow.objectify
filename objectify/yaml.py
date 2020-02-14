"""Perform an ordered load of a YaML file to be used as a Python3 dict

Useful for loading YaML files in general; especially useful for preserving
the order of YaML files for use-cases involving configuration languages
where order may be important

There is also support for Jinja2 templating. The caller may specific a
custom dict() via extra_vars or they can alow the YaML file to template
itself- basically a multiple-pass recursive templating. Easier to describe
with a contrived example:

---
user: admin
root: /usr
home: /home
bin_path: "{{ root }}/bin"
lib_path: "{{ root }}/lib"
user_home: "{{ home }}/{{ user }}"
ssh_root: "{{ user_home }}/.ssh"
ssh_key: "{{ ssh_root }}/id_rsa"
...

For things like configuration files, the order is preserved when loaded
There are basic checks for duplicate keys
"""
from collections import OrderedDict
from re import compile as regex_compile
from sys import stderr
from io import StringIO

from yaml import (safe_load as load_yaml_plain, YAMLError as YAMLException)

from objectify.log import error_frame, error, debug
from objectify.encoding import _DEFAULT_ENCODING
from objectify.template import recursive_template
from objectify.io import objectify_read


def objectify_yaml(path_buf_stream,
                   from_string=False,
                   template=True,
                   extra_vars=None,
                   passes=2,
                   user_path_expand=False,
                   encoding=_DEFAULT_ENCODING):
    """Load a YaML file, stream or string into a Python3 object, optionally templating

    This function can be used to perform an ordered load of a YaML file
    Optionally, it can be used easily with templating
    Templating can be applied recursively / self-templating, for example:

    ---
    root_path: /root
    ssh_path: "{{ root_path }}/.ssh"
    secret_key: "{{ secret_key }}"
    ...

    The above can be templated in two ways:
      1. The variables in the YaML file itself can be applied as source
         data for the templating operation. This allows `ssh_path` to
         be expanded to `/root/.ssh`
      2. The variables can also be templated using a user specified data
         source. For example, if the user passes the following:

         objectify_yaml(..., extra_vars={"secret_key": "s3kr3t"})

         ... the `secret_key` value will be templated to contain "s3kr3t"

    To activate templating, pass `template=True`. This will automatically
    perform self-templating

    To activate templating with an external data source, specify `template=True`
    as well as extra_vars={"some": "dict"}

    To expand values such as "~username" set `expand_user=True`

    You can perform multiple self-templating passes using the `passes=n` parameter
    where n is the amount of passes to make. Usually there is no need for more
    than one

    TODO: Allow deeply nested templating. This requires breaking up the full key
          path/namespace into a list of keys to follow. This also may require
          awareness of datatypes (e.g. lists) so requires a bit more code to do
          correctly. For now there is no use-case, so it is not implelemented

    """
    if from_string is False:
        path_buf_stream = objectify_read(path_buf_stream, encoding=encoding)

    first_pass_data = _load_yaml_ordered(path_buf_stream)
    if template is False:
        debug('skipping ordered YaML templateing, template=False')
        return first_pass_data
    # Parse the YaML into a dictionary and then apply
    # that to the original YaML as if it was a template
    # itself. Allows nested/self-referential templating
    # in YaML files
    if extra_vars is None:
        extra_vars = first_pass_data

    if isinstance(extra_vars, dict):
        first_pass_data = recursive_template(first_pass_data, extra_vars, user_path_expand=user_path_expand)
    else:
        error_frame('unable to load extra_vars, must be dict()')
        exit(1)
    next_pass_data = first_pass_data
    for _ in range(passes):
        next_pass_data = recursive_template(next_pass_data, next_pass_data, user_path_expand=user_path_expand)
    return next_pass_data


def _load_yaml_ordered(yamlstring):
    """Load a YaML file as an OrderedDict, which is important if you plan to
    do nested templating on it using a templating engine like Jinja2

    Calling objectify_yaml() is functionally equivalent to calling this
    function directly, unless template=True is set. In other words, use
    objectify_yaml, do *not* user _load_yaml_ordered directly as it may
    change!

    Returns:
      None on error
      OrderedDict({}) on empty file or general (non-YaML) exception
      OrderedDict({contents}) on properly formatted YaML file
    """
    def _sanity_check(yamlstring):
        """Sanity check to identify duplicate top-level keys

        If there are duplicate top-level keys, they will simply overwrite
        one-another as they are loaded into a Python dict() so it is a
        good idea to keep this logic, though it isn't very pretty
        """
        lines = yamlstring.splitlines()
        top_level_keys = []
        duped_keys = []

        yaml_key_compiled = regex_compile(r'^([A-Za-z0-9_]+) *:')

        for line in lines:
            matched = yaml_key_compiled.search(line)
            if matched:
                if matched.group(1) in top_level_keys:
                    duped_keys.append(matched.group(1))
                else:
                    top_level_keys.append(matched.group(1))
        if duped_keys:
            stderr.write('YaML file %s contains duplicate top-level keys\n',
                         duped_keys)
            exit(1)
        return yamlstring, top_level_keys

    yamlstring, top_level_keys = _sanity_check(yamlstring)
    yamlfd = StringIO(yamlstring)

    # 2nd pass to set up the OrderedDict
    try:
        dict_tmp = load_yaml_plain(yamlfd)
        return OrderedDict([(key, dict_tmp[key]) for key in top_level_keys])
    except YAMLException as err:
        error('Parse error, invalid YaML')
        error_frame(repr(err))
        return None
    except Exception as err:
        error('Unknown exception when parsing YaML')
        error_frame(repr(err))
        return None
