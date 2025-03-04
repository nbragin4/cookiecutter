"""Tests around detection whether scaffoldrom templates are cached locally."""
import os
from pathlib import Path

import pytest

from scaffoldrom import repository


@pytest.fixture
def template():
    """Fixture. Return simple string as template name."""
    return 'scaffoldrom-pytest-plugin'


@pytest.fixture
def cloned_scaffoldrom_path(user_config_data, template):
    """Fixture. Create fake project directory in special user folder."""
    scaffoldroms_dir = user_config_data['scaffoldroms_dir']

    cloned_template_path = os.path.join(scaffoldroms_dir, template)
    os.mkdir(cloned_template_path)

    Path(cloned_template_path, "scaffoldrom.yaml").touch()  # creates file

    return cloned_template_path


def test_should_find_existing_scaffoldrom(
    template, user_config_data, cloned_scaffoldrom_path
):
    """
    Should find folder created by `cloned_scaffoldrom_path` and return it.

    This folder is considered like previously cloned project directory.
    """
    project_dir, cleanup = repository.determine_repo_dir(
        template=template,
        abbreviations={},
        clone_to_dir=user_config_data['scaffoldroms_dir'],
        checkout=None,
        no_input=True,
    )

    assert cloned_scaffoldrom_path == project_dir
    assert not cleanup
