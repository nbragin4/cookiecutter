"""
scaffoldrom.values.

-------------------
"""
from collections import OrderedDict
import os
from scaffoldrom.ordered_yaml import ordered_load, ordered_dump

from scaffoldrom.utils import make_sure_path_exists


def get_file_name(values_dir, template_name):
    """Get the name of file."""
    suffix = '.yaml' if not template_name.endswith('.yaml') else ''
    file_name = f'{template_name}{suffix}'
    return os.path.join(values_dir, file_name)


def dump(values_dir: "os.PathLike[str]", template_name: str, context: dict):
    """Write json data to file."""
    make_sure_path_exists(values_dir)

    if not isinstance(template_name, str):
        raise TypeError('Template name is required to be of type str')

    if not isinstance(context, dict):
        raise TypeError('Context is required to be of type dict')

    if 'scaffoldrom' not in context:
        raise ValueError('Context is required to contain a scaffoldrom key')

    values_file = get_file_name(values_dir, template_name)

    with open(values_file, 'w', encoding="utf-8") as outfile:
        ordered_dump(context, outfile, indent=2)


def load(values_dir, template_name):
    """Read json data from file."""
    if not isinstance(template_name, str):
        raise TypeError('Template name is required to be of type str')

    values_file = get_file_name(values_dir, template_name)

    with open(values_file, encoding="utf-8") as infile:
        context: OrderedDict = ordered_load(infile)

    if 'scaffoldrom' not in context:
        context = OrderedDict({'scaffoldrom': context})
        #raise ValueError('Context is required to contain a scaffoldrom key')

    spec = context['scaffoldrom'].pop('spec', OrderedDict({}) )
    context['scaffoldrom'].update(spec)

    return context
