"""Tests around locally cached scaffoldrom template repositories."""
import os
from pathlib import Path

import pytest

from scaffoldrom import exceptions, repository


@pytest.fixture
def template():
    """Fixture. Return simple string as template name."""
    return 'scaffoldrom-pytest-plugin'


@pytest.fixture
def cloned_scaffoldrom_path(user_config_data, template):
    """Fixture. Prepare folder structure for tests in this file."""
    scaffoldroms_dir = user_config_data['scaffoldroms_dir']

    cloned_template_path = os.path.join(scaffoldroms_dir, template)
    if not os.path.exists(cloned_template_path):
        os.mkdir(cloned_template_path)  # might exist from other tests.

    subdir_template_path = os.path.join(cloned_template_path, 'my-dir')
    if not os.path.exists(subdir_template_path):
        os.mkdir(subdir_template_path)
    Path(subdir_template_path, 'scaffoldrom.yaml').touch()  # creates file

    return subdir_template_path


def test_should_find_existing_scaffoldrom(
    template, user_config_data, cloned_scaffoldrom_path
):
    """Find `scaffoldrom.yaml` in sub folder created by `cloned_scaffoldrom_path`."""
    project_dir, cleanup = repository.determine_repo_dir(
        template=template,
        abbreviations={},
        clone_to_dir=user_config_data['scaffoldroms_dir'],
        checkout=None,
        no_input=True,
        directory='my-dir',
    )

    assert cloned_scaffoldrom_path == project_dir
    assert not cleanup


def test_local_repo_typo(template, user_config_data, cloned_scaffoldrom_path):
    """Wrong pointing to `scaffoldrom.yaml` sub-directory should raise."""
    with pytest.raises(exceptions.RepositoryNotFound) as err:
        repository.determine_repo_dir(
            template=template,
            abbreviations={},
            clone_to_dir=user_config_data['scaffoldroms_dir'],
            checkout=None,
            no_input=True,
            directory='wrong-dir',
        )

    wrong_full_scaffoldrom_path = os.path.join(
        os.path.dirname(cloned_scaffoldrom_path), 'wrong-dir'
    )
    assert str(err.value) == (
        'A valid repository for "{}" could not be found in the following '
        'locations:\n{}'.format(
            template,
            '\n'.join(
                [os.path.join(template, 'wrong-dir'), wrong_full_scaffoldrom_path]
            ),
        )
    )
