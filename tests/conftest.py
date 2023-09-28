"""pytest fixtures which are globally available throughout the suite."""
import os
import shutil

import pytest

from scaffoldrom import utils
from scaffoldrom.config import DEFAULT_CONFIG


USER_CONFIG = """
scaffoldroms_dir: '{scaffoldroms_dir}'
values_dir: '{values_dir}'
"""


@pytest.fixture(autouse=True)
def isolated_filesystem(monkeypatch, tmp_path):
    """Ensure filesystem isolation, set the user home to a tmp_path."""
    root_path = tmp_path.joinpath("home")
    root_path.mkdir()
    scaffoldroms_dir = root_path.joinpath(".scaffoldroms/")
    values_dir = root_path.joinpath(".scaffoldrom_values/")
    monkeypatch.setitem(DEFAULT_CONFIG, 'scaffoldroms_dir', str(scaffoldroms_dir))
    monkeypatch.setitem(DEFAULT_CONFIG, 'values_dir', str(values_dir))

    monkeypatch.setenv("HOME", str(root_path))
    monkeypatch.setenv("USERPROFILE", str(root_path))


def backup_dir(original_dir, backup_dir):
    """Generate backup directory based on original directory."""
    # If the default original_dir is pre-existing, move it to a temp location
    if not os.path.isdir(original_dir):
        return False

    # Remove existing stale backups before backing up.
    if os.path.isdir(backup_dir):
        utils.rmtree(backup_dir)

    shutil.copytree(original_dir, backup_dir)
    return True


def restore_backup_dir(original_dir, backup_dir, original_dir_found):
    """Restore default contents."""
    original_dir_is_dir = os.path.isdir(original_dir)
    if original_dir_found:
        # Delete original_dir if a backup exists
        if original_dir_is_dir and os.path.isdir(backup_dir):
            utils.rmtree(original_dir)
    else:
        # Delete the created original_dir.
        # There's no backup because it never existed
        if original_dir_is_dir:
            utils.rmtree(original_dir)

    # Restore the user's default original_dir contents
    if os.path.isdir(backup_dir):
        shutil.copytree(backup_dir, original_dir)
    if os.path.isdir(original_dir):
        utils.rmtree(backup_dir)


@pytest.fixture(scope='function')
def clean_system(request):
    """Fixture. Simulates a clean system with no configured or cloned scaffoldroms.

    It runs code which can be regarded as setup code as known from a unittest
    TestCase. Additionally it defines a local function referring to values
    which have been stored to local variables in the setup such as the location
    of the scaffoldroms on disk. This function is registered as a teardown
    hook with `request.addfinalizer` at the very end of the fixture. Pytest
    runs the named hook as soon as the fixture is out of scope, when the test
    finished to put it another way.

    During setup:

    * Back up the `~/.scaffoldromrc` config file to `~/.scaffoldromrc.backup`
    * Back up the `~/.scaffoldroms/` dir to `~/.scaffoldroms.backup/`
    * Back up the `~/.scaffoldrom_values/` dir to
      `~/.scaffoldrom_values.backup/`
    * Starts off a test case with no pre-existing `~/.scaffoldromrc` or
      `~/.scaffoldroms/` or `~/.scaffoldrom_values/`

    During teardown:

    * Delete `~/.scaffoldroms/` only if a backup is present at
      `~/.scaffoldroms.backup/`
    * Delete `~/.scaffoldrom_values/` only if a backup is present at
      `~/.scaffoldrom_values.backup/`
    * Restore the `~/.scaffoldromrc` config file from
      `~/.scaffoldromrc.backup`
    * Restore the `~/.scaffoldroms/` dir from `~/.scaffoldroms.backup/`
    * Restore the `~/.scaffoldrom_values/` dir from
      `~/.scaffoldrom_values.backup/`

    """
    # If ~/.scaffoldromrc is pre-existing, move it to a temp location
    user_config_path = os.path.expanduser('~/.scaffoldromrc')
    user_config_path_backup = os.path.expanduser('~/.scaffoldromrc.backup')
    if os.path.exists(user_config_path):
        user_config_found = True
        shutil.copy(user_config_path, user_config_path_backup)
        os.remove(user_config_path)
    else:
        user_config_found = False

    # If the default scaffoldroms_dir is pre-existing, move it to a
    # temp location
    scaffoldroms_dir = os.path.expanduser('~/.scaffoldroms')
    scaffoldroms_dir_backup = os.path.expanduser('~/.scaffoldroms.backup')
    scaffoldroms_dir_found = backup_dir(scaffoldroms_dir, scaffoldroms_dir_backup)

    # If the default scaffoldrom_values_dir is pre-existing, move it to a
    # temp location
    scaffoldrom_values_dir = os.path.expanduser('~/.scaffoldrom_values')
    scaffoldrom_values_dir_backup = os.path.expanduser('~/.scaffoldrom_values.backup')
    scaffoldrom_values_dir_found = backup_dir(
        scaffoldrom_values_dir, scaffoldrom_values_dir_backup
    )

    def restore_backup():
        # If it existed, restore ~/.scaffoldromrc
        # We never write to ~/.scaffoldromrc, so this logic is simpler.
        if user_config_found and os.path.exists(user_config_path_backup):
            shutil.copy(user_config_path_backup, user_config_path)
            os.remove(user_config_path_backup)

        # Carefully delete the created ~/.scaffoldroms dir only in certain
        # conditions.
        restore_backup_dir(
            scaffoldroms_dir, scaffoldroms_dir_backup, scaffoldroms_dir_found
        )

        # Carefully delete the created ~/.scaffoldrom_values dir only in
        # certain conditions.
        restore_backup_dir(
            scaffoldrom_values_dir,
            scaffoldrom_values_dir_backup,
            scaffoldrom_values_dir_found,
        )

    request.addfinalizer(restore_backup)


@pytest.fixture(scope='session')
def user_dir(tmp_path_factory):
    """Fixture that simulates the user's home directory."""
    return tmp_path_factory.mktemp('user_dir')


@pytest.fixture(scope='session')
def user_config_data(user_dir):
    """Fixture that creates 2 Scaffoldrom user config dirs.

     It will create it in the user's home directory.

    * `scaffoldroms_dir`
    * `scaffoldrom_values`

    :returns: Dict with name of both user config dirs
    """
    scaffoldroms_dir = user_dir.joinpath('scaffoldroms')
    scaffoldroms_dir.mkdir()
    values_dir = user_dir.joinpath('scaffoldrom_values')
    values_dir.mkdir()
    return {
        'scaffoldroms_dir': str(scaffoldroms_dir),
        'values_dir': str(values_dir),
    }


@pytest.fixture(scope='session')
def user_config_file(user_dir, user_config_data):
    """Fixture that creates a config file called `config`.

     It will create it in the user's home directory, with YAML from
     `user_config_data`.

    :param user_dir: Simulated user's home directory
    :param user_config_data: Dict of config values
    :returns: String of path to config file
    """
    config_file = user_dir.joinpath('config')

    config_text = USER_CONFIG.format(**user_config_data)
    config_file.write_text(config_text)
    return str(config_file)


@pytest.fixture
def output_dir(tmp_path):
    """Fixture to prepare test output directory."""
    output_path = tmp_path.joinpath("output")
    output_path.mkdir()
    return str(output_path)


@pytest.fixture
def clone_dir(tmp_path):
    """Simulate creation of a directory called `clone_dir` inside of `tmp_path`. \
    Returns a str to said directory."""
    clone_dir = tmp_path.joinpath("clone_dir")
    clone_dir.mkdir()
    return clone_dir
