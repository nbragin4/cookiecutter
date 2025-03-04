"""Collection of tests around loading scaffoldrom config."""
from pathlib import Path

import pytest
import yaml

from scaffoldrom import config
from scaffoldrom.exceptions import ConfigDoesNotExistException, InvalidConfiguration


def test_merge_configs():
    """Verify default and user config merged in expected way."""
    default = {
        'scaffoldroms_dir': '/home/example/some-path-to-templates',
        'values_dir': '/home/example/some-path-to-values-files',
        'default_context': {},
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
        },
    }

    user_config = {
        'default_context': {
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
        },
        'abbreviations': {
            'gl': 'https://gitlab.com/hackebrot/{0}.git',
            'pytest-plugin': 'https://github.com/pytest-dev/pytest-plugin.git',
        },
    }

    expected_config = {
        'scaffoldroms_dir': '/home/example/some-path-to-templates',
        'values_dir': '/home/example/some-path-to-values-files',
        'default_context': {
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/hackebrot/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
            'pytest-plugin': 'https://github.com/pytest-dev/pytest-plugin.git',
        },
    }

    assert config.merge_configs(default, user_config) == expected_config


def test_get_config():
    """Verify valid config opened and rendered correctly."""
    conf = config.get_config('tests/test-config/valid-config.yaml')
    expected_conf = {
        'scaffoldroms_dir': '/home/example/some-path-to-templates',
        'values_dir': '/home/example/some-path-to-values-files',
        'default_context': {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example',
            'project': {
                'description': 'description',
                'tags': [
                    'first',
                    'second',
                    'third',
                ],
            },
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
            'helloworld': 'https://github.com/hackebrot/helloworld',
        },
    }
    assert conf == expected_conf


def test_get_config_does_not_exist():
    """Check that `exceptions.ConfigDoesNotExistException` is raised when \
    attempting to get a non-existent config file."""
    expected_error_msg = 'Config file tests/not-exist.yaml does not exist.'
    with pytest.raises(ConfigDoesNotExistException) as exc_info:
        config.get_config('tests/not-exist.yaml')
    assert str(exc_info.value) == expected_error_msg


def test_invalid_config():
    """An invalid config file should raise an `InvalidConfiguration` \
    exception."""
    expected_error_msg = (
        'Unable to parse YAML file tests/test-config/invalid-config.yaml.'
    )
    with pytest.raises(InvalidConfiguration) as exc_info:
        config.get_config('tests/test-config/invalid-config.yaml')
        assert expected_error_msg in str(exc_info.value)
        assert isinstance(exc_info.value.__cause__, yaml.YAMLError)


def test_get_config_with_defaults():
    """A config file that overrides 1 of 3 defaults."""
    conf = config.get_config('tests/test-config/valid-partial-config.yaml')
    default_scaffoldroms_dir = Path('~/.scaffoldroms').expanduser()
    default_values_dir = Path('~/.scaffoldrom_values').expanduser()
    expected_conf = {
        'scaffoldroms_dir': str(default_scaffoldroms_dir),
        'values_dir': str(default_values_dir),
        'default_context': {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example',
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
        },
    }
    assert conf == expected_conf
