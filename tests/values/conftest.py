"""pytest fixtures for testing scaffoldrom's values feature."""
import pytest


@pytest.fixture
def context():
    """Fixture to return a valid context as known from a scaffoldrom.json."""
    return {
        'scaffoldrom': {
            'email': 'raphael@hackebrot.de',
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
            'version': '0.1.0',
        }
    }


@pytest.fixture
def values_test_dir():
    """Fixture to test directory."""
    return 'tests/test-values/'


@pytest.fixture
def mock_user_config(mocker):
    """Fixture to mock user config."""
    return mocker.patch('scaffoldrom.main.get_user_config')
