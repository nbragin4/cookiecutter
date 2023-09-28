"""test_dump."""
import json
import os

import pytest

from scaffoldrom import values


@pytest.fixture
def template_name():
    """Fixture to return a valid template_name."""
    return 'cookiedozer'


@pytest.fixture
def values_file(values_test_dir, template_name):
    """Fixture to return a actual file name of the dump."""
    file_name = f'{template_name}.json'
    return os.path.join(values_test_dir, file_name)


@pytest.fixture(autouse=True)
def remove_values_dump(request, values_file):
    """Remove the values file created by tests."""

    def fin_remove_values_file():
        if os.path.exists(values_file):
            os.remove(values_file)

    request.addfinalizer(fin_remove_values_file)


def test_type_error_if_no_template_name(values_test_dir, context):
    """Test that values.dump raises if the template_name is not a valid str."""
    with pytest.raises(TypeError):
        values.dump(values_test_dir, None, context)


def test_type_error_if_not_dict_context(values_test_dir, template_name):
    """Test that values.dump raises if the context is not of type dict."""
    with pytest.raises(TypeError):
        values.dump(values_test_dir, template_name, 'not_a_dict')


def test_value_error_if_key_missing_in_context(values_test_dir, template_name):
    """Test that values.dump raises if the context does not contain a key \
    named 'scaffoldrom'."""
    with pytest.raises(ValueError):
        values.dump(values_test_dir, template_name, {'foo': 'bar'})


@pytest.fixture
def mock_ensure_failure(mocker):
    """Replace scaffoldrom.values.make_sure_path_exists function.

    Used to mock internal function and limit test scope.
    Always return expected value: False
    """
    return mocker.patch(
        'scaffoldrom.values.make_sure_path_exists', side_effect=OSError
    )


@pytest.fixture
def mock_ensure_success(mocker):
    """Replace scaffoldrom.values.make_sure_path_exists function.

    Used to mock internal function and limit test scope.
    Always return expected value: True
    """
    return mocker.patch('scaffoldrom.values.make_sure_path_exists', return_value=True)


def test_ioerror_if_values_dir_creation_fails(mock_ensure_failure, values_test_dir):
    """Test that values.dump raises when the values_dir cannot be created."""
    with pytest.raises(OSError):
        values.dump(values_test_dir, 'foo', {'scaffoldrom': {'hello': 'world'}})

    mock_ensure_failure.assert_called_once_with(values_test_dir)


def test_run_json_dump(
    mocker,
    mock_ensure_success,
    mock_user_config,
    template_name,
    context,
    values_test_dir,
    values_file,
):
    """Test that values.dump runs json.dump under the hood and that the context \
    is correctly written to the expected file in the values_dir."""
    spy_get_values_file = mocker.spy(values, 'get_file_name')

    mock_json_dump = mocker.patch('json.dump', side_effect=json.dump)

    values.dump(values_test_dir, template_name, context)

    assert not mock_user_config.called
    mock_ensure_success.assert_called_once_with(values_test_dir)
    spy_get_values_file.assert_called_once_with(values_test_dir, template_name)

    assert mock_json_dump.call_count == 1
    (dumped_context, outfile_handler), kwargs = mock_json_dump.call_args
    assert outfile_handler.name == values_file
    assert dumped_context == context
