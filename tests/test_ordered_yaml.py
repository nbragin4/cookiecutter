"""
tests_ordered_yaml.

Test formerly known from a unittest residing in test_generate.py named
TestYaml.test_ordered_yaml
"""
from collections import OrderedDict

from scaffoldrom.ordered_yaml import ordered_dump, ordered_load


def test_ordered_load():
    """test yaml loading"""
    yaml_str = 'a: 1\nb: 2\nc: 3\n'
    expected_dict = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    assert ordered_load(yaml_str) == expected_dict

def test_ordered_dump():
    """test yaml dumping"""
    data = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    expected_yaml_str = 'a: 1\nb: 2\nc: 3\n'
    assert ordered_dump(data) == expected_yaml_str
