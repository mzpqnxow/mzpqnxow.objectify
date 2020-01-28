"""Perform an ordered load of a YaML file to be used as a Python3 dict

TODO: 

Optional support for Jinja2 templating, including multiple-pass
recursive templating, example:

---
user: admin
root: /usr
home: /home
bin_path: "{{ root }}/bin"
lib_path: "{{ root }}/lib"
user_home: "{{ home }}/{{ user }}"
ssh_root: "{{ user_home }}/.ssh"
ssh_key: "{{ ssh_root }}/id_rsa"

For things like configuration files, the order is preserved when loaded
There are basic checks for duplicate keys

TODO: Paste in Jinja2 templating support, or maybe just leave it out

"""
from collections import OrderedDict
from re import compile as regex_compile
from sys import stderr
from io import StringIO
from yaml import (safe_load as load_yaml_plain, YAMLError as YAMLException)

_YAML_KEY_COMPILED = regex_compile(r'^([A-Za-z0-9_]+) *:')


def objectify_yaml(yamlstring):
    """Load a YaML file as an OrderedDict, which is important if you plan to
    do nested templating on it using a templating engine like Jinja2

    Returns:
      None on error
      OrderedDict({}) on empty file or general (non-YaML) exception
      OrderedDict({contents}) on properly formatted YaML file

    This is really stupid, it only takes the YaML string, not a filepath.
    Whatever, this can be changed later I guess

    """
    # This first bit is a sanity check, making sure there are no duplicate
    # keys. It isn't a *must* have, but it can save a lot of headaches if
    # a mistake is made in the YaML file. Most YaML files are not very large
    # so performance penalty is negligible
    lines = yamlstring.splitlines()
    top_keys = []
    duped_keys = []
    for line in lines:
        matched = _YAML_KEY_COMPILED.search(line)
        if matched:
            if matched.group(1) in top_keys:
                duped_keys.append(matched.group(1))
            else:
                top_keys.append(matched.group(1))
    if duped_keys:
        stderr.write('YaML file %s contains duplicate top-level keys\n',
                     duped_keys)
        exit(1)
    yamlfd = StringIO(yamlstring)
    # 2nd pass to set up the OrderedDict
    try:
        dict_tmp = load_yaml_plain(yamlfd)
        return OrderedDict([(key, dict_tmp[key]) for key in top_keys])
    except YAMLException as err:
        stderr.write(err)
        stderr.write('\nParse error, invalid YaML\n')
        return None
    except Exception as err:
        stderr.write(err)
        stderr.write('\nUnknown error when loading YaML file\n')
        return None
