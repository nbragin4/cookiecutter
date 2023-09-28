"""Test scaffoldrom invocation with nested configuration structure."""
import os

from scaffoldrom import main


def test_scaffoldrom_nested_templates(mocker):
    """Verify scaffoldrom nested configuration files mechanism."""
    mock_generate_files = mocker.patch("scaffoldrom.main.generate_files")
    main_dir = os.path.join("tests", "fake-nested-templates")
    main.scaffoldrom(main_dir, no_input=True)
    assert mock_generate_files.call_args[1]["repo_dir"] == os.path.join(
        main_dir, "fake-project"
    )
