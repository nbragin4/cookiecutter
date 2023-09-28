"""Tests for `repository_has_scaffoldrom_json` function."""
import pytest

from scaffoldrom.repository import repository_has_scaffoldrom_json


def test_valid_repository():
    """Validate correct response if `scaffoldrom.yaml` file exist."""
    assert repository_has_scaffoldrom_json('tests/fake-repo')


@pytest.mark.parametrize(
    'invalid_repository', (['tests/fake-repo-bad', 'tests/unknown-repo'])
)
def test_invalid_repository(invalid_repository):
    """Validate correct response if `scaffoldrom.yaml` file not exist."""
    assert not repository_has_scaffoldrom_json(invalid_repository)
