"""Provide templating functionality for use in YaML loading"""

from os.path import expanduser
from jinja2 import Template

from objectify.log import error_frame


def _recursive_template(data, template_vars=None, user_path_expand=True):
    """data is an arbitrary data structure, template_vars is a dict

    The `data` object is traversed and each instance of a Jinja2 variable
    that is found in template_vars is replaced (templated)

    This is a recursive function with the end-case being when the object is
    a simple string or unicode string type
    """

    def _handle_list(data, template_vars):
        """Handle the case where data is a list"""
        tmp_list = []
        data.reverse()
        while data:
            item = data.pop()
            item = recursive_template(item, template_vars)
            tmp_list.append(item)
        return tmp_list

    def _handle_str(data, template_vars):
        """Handle a simple string value"""
        tmpl = Template(data)
        data = tmpl.render(template_vars)
        if user_path_expand is True:
            data = expanduser(data)
        return data

    def _handle_numeric(data, template_vars):
        """Handle a simple integer type"""
        return data

    def _handle_dict(data, template_vars):
        """Handle a dict value by going deeper/recursing"""
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = recursive_template(value, template_vars)
            return data

    if template_vars is None:
        template_vars = {}

    elif not isinstance(template_vars, dict):
        raise RuntimeError('template_vars must be an instance of dict()')

    type_handlers = {
        'str': _handle_str,
        'dict': _handle_dict,
        'OrderedDict': _handle_dict,
        'list': _handle_list,
        'int': _handle_numeric,
        'float': _handle_numeric
    }

    handler_key = type(data).__name__
    handler = type_handlers[handler_key]
    return handler(data, template_vars)

    error_frame('unexpected and unsupported type "{}" encountered'.format(
        type(data)))
    raise RuntimeError('unable to template object')


def recursive_template(data, template_vars=None, user_path_expand=True):
    """data is an arbitrary data structure, template_vars is a dict

    The `data` object is traversed and each instance of a Jinja2 variable
    that is found in template_vars is replaced (templated)

    This is a recursive function with the end-case being when the object is
    a simple string or unicode string type
    """
    # These conditionals can be cleaned up a little bit
    # Note there is no use for `elif` because each block returns making
    # the `else` implied
    # def _handle_list(data, template_vars):
    #     tmp_list = []
    #     data.reverse()
    #     while data:
    #         item = data.pop()
    #         item = recursive_template(item, template_vars)
    #         tmp_list.append(item)
    #     return tmp_list

    # def _handle_str(data, template_vars, user_path_expand=user_path_expand):
    #     tmpl = Template(data)
    #     data = tmpl.render(template_vars)
    #     if user_path_expand is True:
    #         data = expanduser(data)
    #     return data

    # def _handle_numeric(data):
    #     return data

    # def _handle_dict(data, template_vars):
    #     if isinstance(data, dict):
    #         for key, value in data.items():
    #             data[key] = recursive_template(value, template_vars)
    #         return data

    if template_vars is None:
        template_vars = {}

    elif not isinstance(template_vars, dict):
        raise RuntimeError('template_vars must be an instance of dict()')

    if isinstance(data, str):
        tmpl = Template(data)
        data = tmpl.render(template_vars)
        if user_path_expand is True:
            data = expanduser(data)
        return data

    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = recursive_template(value, template_vars)
        return data

    if isinstance(data, list):
        # Not supporting sets and tuples since YaML doesn't support them
        tmp_list = []
        data.reverse()
        while data:
            item = data.pop()
            item = recursive_template(item, template_vars)
            tmp_list.append(item)
        return tmp_list

    if isinstance(data, (int, float)):
        return data

    error_frame('unexpected and unsupported type "{}" encountered'.format(
        type(data)))
    raise RuntimeError('unable to template object')
