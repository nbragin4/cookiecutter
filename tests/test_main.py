"""Collection of tests around scaffoldrom's values feature."""
from scaffoldrom.main import scaffoldrom


def test_original_scaffoldrom_options_preserved_in__scaffoldrom(
    monkeypatch,
    mocker,
    user_config_file,
):
    """Preserve original context options.

    Tests you can access the original context options via
    `context['_scaffoldrom']`.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl-_scaffoldrom')
    mock_generate_files = mocker.patch('scaffoldrom.main.generate_files')
    scaffoldrom(
        '.',
        no_input=True,
        values=False,
        config_file=user_config_file,
    )
    assert mock_generate_files.call_args[1]['context']['_scaffoldrom'][
        'test_list'
    ] == [1, 2, 3, 4]
    assert mock_generate_files.call_args[1]['context']['_scaffoldrom'][
        'test_dict'
    ] == {"foo": "bar"}


def test_values_dump_template_name(
    monkeypatch, mocker, user_config_data, user_config_file
):
    """Check that values_dump is called with a valid template_name.

    Template name must not be a relative path.

    Otherwise files such as ``..json`` are created, which are not just cryptic
    but also later mistaken for values files of other templates if invoked with
    '.' and '--values'.

    Change the current working directory temporarily to 'tests/fake-repo-tmpl'
    for this test and call scaffoldrom with '.' for the target template.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_values_dump = mocker.patch('scaffoldrom.main.dump')
    mocker.patch('scaffoldrom.main.generate_files')

    scaffoldrom(
        '.',
        no_input=True,
        values=False,
        config_file=user_config_file,
    )

    mock_values_dump.assert_called_once_with(
        user_config_data['values_dir'],
        'fake-repo-tmpl',
        mocker.ANY,
    )


def test_values_load_template_name(
    monkeypatch, mocker, user_config_data, user_config_file
):
    """Check that values_load is called correctly.

    Calls require valid template_name that is not a relative path.

    Change the current working directory temporarily to 'tests/fake-repo-tmpl'
    for this test and call scaffoldrom with '.' for the target template.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_values_load = mocker.patch('scaffoldrom.main.load')
    mocker.patch('scaffoldrom.main.generate_context').return_value = {
        'scaffoldrom': {}
    }
    mocker.patch('scaffoldrom.main.generate_files')
    mocker.patch('scaffoldrom.main.dump')

    scaffoldrom(
        '.',
        values=True,
        config_file=user_config_file,
    )

    mock_values_load.assert_called_once_with(
        user_config_data['values_dir'],
        'fake-repo-tmpl',
    )


def test_custom_values_file(monkeypatch, mocker, user_config_file):
    """Check that reply.load is called with the custom values_file."""
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_values_load = mocker.patch('scaffoldrom.main.load')
    mocker.patch('scaffoldrom.main.generate_context').return_value = {
        'scaffoldrom': {}
    }
    mocker.patch('scaffoldrom.main.generate_files')
    mocker.patch('scaffoldrom.main.dump')

    scaffoldrom(
        '.',
        values='./custom-values-file',
        config_file=user_config_file,
    )

    mock_values_load.assert_called_once_with(
        '.',
        'custom-values-file',
    )
