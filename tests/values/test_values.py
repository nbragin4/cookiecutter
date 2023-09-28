"""test_values."""
import os

import pytest

from scaffoldrom import exceptions, main, values


@pytest.mark.parametrize("values_file_name", ['bar', 'bar.json'])
def test_get_values_file_name(values_file_name):
    """Make sure that values.get_file_name generates a valid json file path."""
    exp_values_file_path = os.path.join('foo', 'bar.json')
    values_file_path = values.get_file_name('foo', values_file_name)
    assert values_file_path == exp_values_file_path


@pytest.mark.parametrize(
    'invalid_kwargs',
    (
        {'no_input': True},
        {'extra_context': {}},
        {'no_input': True, 'extra_context': {}},
    ),
)
def test_raise_on_invalid_mode(invalid_kwargs):
    """Test `scaffoldrom` raise exception on unacceptable `values` request."""
    with pytest.raises(exceptions.InvalidModeException):
        main.scaffoldrom('foo', values=True, **invalid_kwargs)


def test_main_does_not_invoke_dump_but_load(mocker):
    """Test `scaffoldrom` calling correct functions on `values`."""
    mock_prompt = mocker.patch('scaffoldrom.main.prompt_for_config')
    mock_gen_context = mocker.patch('scaffoldrom.main.generate_context')
    mock_gen_files = mocker.patch('scaffoldrom.main.generate_files')
    mock_values_dump = mocker.patch('scaffoldrom.main.dump')
    mock_values_load = mocker.patch('scaffoldrom.main.load')

    main.scaffoldrom('tests/fake-repo-tmpl/', values=True)

    assert not mock_prompt.called
    assert mock_gen_context.called
    assert mock_values_dump.called
    assert mock_values_load.called
    assert mock_gen_files.called


def test_main_does_not_invoke_load_but_dump(mocker):
    """Test `scaffoldrom` calling correct functions on non-values launch."""
    mock_prompt = mocker.patch('scaffoldrom.main.prompt_for_config')
    mock_gen_context = mocker.patch('scaffoldrom.main.generate_context')
    mock_gen_files = mocker.patch('scaffoldrom.main.generate_files')
    mock_values_dump = mocker.patch('scaffoldrom.main.dump')
    mock_values_load = mocker.patch('scaffoldrom.main.load')

    main.scaffoldrom('tests/fake-repo-tmpl/', values=False)

    assert mock_prompt.called
    assert mock_gen_context.called
    assert mock_values_dump.called
    assert not mock_values_load.called
    assert mock_gen_files.called
