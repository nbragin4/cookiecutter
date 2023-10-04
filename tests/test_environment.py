"""Collection of tests around loading extensions."""
import pytest

from scaffoldrom.environment import StrictEnvironment
from scaffoldrom.exceptions import UnknownExtension


def test_env_should_raise_for_unknown_extension():
    """Test should raise if extension not installed in system."""
    context = {'scaffoldrom': {'_extensions': ['foobar']}}

    with pytest.raises(UnknownExtension) as err:
        StrictEnvironment(context=context, keep_trailing_newline=True)

    assert 'Unable to load extension: ' in str(err.value)


def test_env_should_come_with_default_extensions():
    """Verify default extensions loaded with StrictEnvironment."""
    env = StrictEnvironment(keep_trailing_newline=True)
    assert 'scaffoldrom.extensions.YamlifyExtension' in env.extensions
    assert 'scaffoldrom.extensions.JsonifyExtension' in env.extensions
    assert 'scaffoldrom.extensions.RandomStringExtension' in env.extensions
    assert 'scaffoldrom.extensions.SlugifyExtension' in env.extensions
    assert 'scaffoldrom.extensions.TimeExtension' in env.extensions
    assert 'scaffoldrom.extensions.UUIDExtension' in env.extensions
