"""Test main scaffoldrom invocation with user input enabled (mocked)."""
import os

import pytest

from scaffoldrom import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """Remove special directories which are created during the tests."""
    yield
    if os.path.isdir('fake-project'):
        utils.rmtree('fake-project')
    if os.path.isdir('fake-project-input-extra'):
        utils.rmtree('fake-project-input-extra')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_scaffoldrom_local_with_input(monkeypatch):
    """Verify simple scaffoldrom run results, without extra_context provided."""
    monkeypatch.setattr(
        'scaffoldrom.prompt.read_user_variable',
        lambda var, default, prompts, prefix: default,
    )
    main.scaffoldrom('tests/fake-repo-pre/', no_input=False)
    assert os.path.isdir('tests/fake-repo-pre/{{scaffoldrom.repo_name}}')
    assert not os.path.isdir('tests/fake-repo-pre/fake-project')
    assert os.path.isdir('fake-project')
    assert os.path.isfile('fake-project/README.rst')
    assert not os.path.exists('fake-project/json/')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_scaffoldrom_input_extra_context(monkeypatch):
    """Verify simple scaffoldrom run results, with extra_context provided."""
    monkeypatch.setattr(
        'scaffoldrom.prompt.read_user_variable',
        lambda var, default, prompts, prefix: default,
    )
    main.scaffoldrom(
        'tests/fake-repo-pre',
        no_input=False,
        extra_context={'repo_name': 'fake-project-input-extra'},
    )
    assert os.path.isdir('fake-project-input-extra')
