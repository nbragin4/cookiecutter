"""Testing invalid scaffoldrom template repositories."""
import pytest

from scaffoldrom import exceptions, main


def test_should_raise_error_if_repo_does_not_exist():
    """Scaffoldrom invocation with non-exist repository should raise error."""
    with pytest.raises(exceptions.RepositoryNotFound):
        main.scaffoldrom('definitely-not-a-valid-repo-dir')
