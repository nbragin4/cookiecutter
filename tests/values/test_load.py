"""test_load."""
import yaml
import os

import pytest

from scaffoldrom import values


@pytest.fixture
def template_name():
    """Fixture to return a valid template_name."""
    return 'cookiedozer_load'


@pytest.fixture
def values_file(values_test_dir, template_name):
    """Fixture to return a actual file name of the dump."""
    file_name = f'{template_name}.yaml'
    return os.path.join(values_test_dir, file_name)


def test_type_error_if_no_template_name(values_test_dir):
    """Test that values.load raises if the template_name is not a valid str."""
    with pytest.raises(TypeError):
        values.load(values_test_dir, None)


def test_value_error_if_key_missing_in_context(mocker, values_test_dir):
    """Test that values.load raises if the loaded context does not contain \
    'scaffoldrom'."""
    result = values.load(values_test_dir, 'invalid_values')
    assert 'scaffoldrom' in result.keys()


def test_io_error_if_no_values_file(mocker, values_test_dir):
    """Test that values.load raises if it cannot find a values file."""
    with pytest.raises(IOError):
        values.load(values_test_dir, 'no_values')


def test_run_yaml_load(
    mocker, mock_user_config, template_name, context, values_test_dir, values_file
):
    """Test that values.load runs yaml.load under the hood and that the context \
    is correctly loaded from the file in values_dir."""
    spy_get_values_file = mocker.spy(values, 'get_file_name')

    mock_yaml_load = mocker.patch('yaml.load', side_effect=yaml.load)

    loaded_context = values.load(values_test_dir, template_name)

    assert not mock_user_config.called
    spy_get_values_file.assert_called_once_with(values_test_dir, template_name)

    assert mock_yaml_load.call_count == 1
    (args, kwargs) = mock_yaml_load.call_args_list[0]
    assert args[0].name == values_file
    assert loaded_context == context
