"""Tests for `scaffoldrom.prompt` module."""
import platform
from collections import OrderedDict

import click
import pytest

from scaffoldrom import prompt, exceptions, environment


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    """Fixture. Overwrite windows end of line to linux standard."""
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


class TestRenderVariable:
    """Class to unite simple and complex tests for render_variable function."""

    @pytest.mark.parametrize(
        'raw_var, rendered_var',
        [
            (1, '1'),
            (True, True),
            ('foo', 'foo'),
            ('{{scaffoldrom.project}}', 'foobar'),
            (None, None),
        ],
    )
    def test_convert_to_str(self, mocker, raw_var, rendered_var):
        """Verify simple items correctly rendered to strings."""
        env = environment.StrictEnvironment()
        from_string = mocker.patch(
            'scaffoldrom.prompt.StrictEnvironment.from_string', wraps=env.from_string
        )
        context = {'project': 'foobar'}

        result = prompt.render_variable(env, raw_var, context)
        assert result == rendered_var

        # Make sure that non None non str variables are converted beforehand
        if raw_var is not None and not isinstance(raw_var, bool):
            if not isinstance(raw_var, str):
                raw_var = str(raw_var)
            from_string.assert_called_once_with(raw_var)
        else:
            assert not from_string.called

    @pytest.mark.parametrize(
        'raw_var, rendered_var',
        [
            ({1: True, 'foo': False}, {'1': True, 'foo': False}),
            (
                {'{{scaffoldrom.project}}': ['foo', 1], 'bar': False},
                {'foobar': ['foo', '1'], 'bar': False},
            ),
            (['foo', '{{scaffoldrom.project}}', None], ['foo', 'foobar', None]),
        ],
    )
    def test_convert_to_str_complex_variables(self, raw_var, rendered_var):
        """Verify tree items correctly rendered."""
        env = environment.StrictEnvironment()
        context = {'project': 'foobar'}

        result = prompt.render_variable(env, raw_var, context)
        assert result == rendered_var


class TestPrompt:
    """Class to unite user prompt related tests."""

    @pytest.mark.parametrize(
        'context',
        [
            {'scaffoldrom': {'full_name': 'Your Name'}},
            {'scaffoldrom': {'full_name': 'Řekni či napiš své jméno'}},
        ],
        ids=['ASCII default prompt/input', 'Unicode default prompt/input'],
    )
    def test_prompt_for_config(self, monkeypatch, context):
        """Verify `prompt_for_config` call `read_user_variable` on text request."""
        monkeypatch.setattr(
            'scaffoldrom.prompt.read_user_variable',
            lambda var, default, prompts, prefix: default,
        )

        scaffoldrom_dict = prompt.prompt_for_config(context)
        assert scaffoldrom_dict == context['scaffoldrom']

    @pytest.mark.parametrize(
        'context',
        [
            {
                'scaffoldrom': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    'nothing': 'ok',
                    '__prompts__': {
                        'full_name': 'Name please',
                        'check': 'Checking',
                    },
                }
            },
        ],
        ids=['ASCII default prompt/input'],
    )
    def test_prompt_for_config_with_human_prompts(self, monkeypatch, context):
        """Verify call `read_user_variable` on request when human-readable prompts."""
        monkeypatch.setattr(
            'scaffoldrom.prompt.read_user_variable',
            lambda var, default, prompts, prefix: default,
        )
        monkeypatch.setattr(
            'scaffoldrom.prompt.read_user_yes_no',
            lambda var, default, prompts, prefix: default,
        )
        monkeypatch.setattr(
            'scaffoldrom.prompt.read_user_choice',
            lambda var, default, prompts, prefix: default,
        )

        scaffoldrom_dict = prompt.prompt_for_config(context)
        assert scaffoldrom_dict == context['scaffoldrom']

    @pytest.mark.parametrize(
        'context',
        [
            {
                'scaffoldrom': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    '__prompts__': {
                        'check': 'Checking',
                    },
                }
            },
            {
                'scaffoldrom': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    '__prompts__': {
                        'full_name': 'Name please',
                        'check': {'__prompt__': 'Checking', 'yes': 'Yes', 'no': 'No'},
                    },
                }
            },
            {
                'scaffoldrom': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    '__prompts__': {
                        'full_name': 'Name please',
                        'check': {'no': 'No'},
                    },
                }
            },
        ],
    )
    def test_prompt_for_config_with_human_choices(self, monkeypatch, context):
        """Test prompts when human-readable labels for user choices."""
        runner = click.testing.CliRunner()
        with runner.isolation(input="\n\n\n"):
            scaffoldrom_dict = prompt.prompt_for_config(context)

        assert dict(scaffoldrom_dict) == {'full_name': 'Your Name', 'check': 'yes'}

    def test_prompt_for_config_dict(self, monkeypatch):
        """Verify `prompt_for_config` call `read_user_variable` on dict request."""
        monkeypatch.setattr(
            'scaffoldrom.prompt.read_user_dict',
            lambda var, default, prompts, prefix: {"key": "value", "integer": 37},
        )
        context = {'scaffoldrom': {'details': {}}}

        scaffoldrom_dict = prompt.prompt_for_config(context)
        assert scaffoldrom_dict == {'details': {'key': 'value', 'integer': 37}}

    def test_should_render_dict(self):
        """Verify template inside dictionary variable rendered."""
        context = {
            'scaffoldrom': {
                'project_name': 'Slartibartfast',
                'details': {
                    '{{scaffoldrom.project_name}}': '{{scaffoldrom.project_name}}'
                },
            }
        }

        scaffoldrom_dict = prompt.prompt_for_config(context, no_input=True)
        assert scaffoldrom_dict == {
            'project_name': 'Slartibartfast',
            'details': {'Slartibartfast': 'Slartibartfast'},
        }

    def test_should_render_deep_dict(self):
        """Verify nested structures like dict in dict, rendered correctly."""
        context = {
            'scaffoldrom': {
                'project_name': "Slartibartfast",
                'details': {
                    "key": "value",
                    "integer_key": 37,
                    "other_name": '{{scaffoldrom.project_name}}',
                    "dict_key": {
                        "deep_key": "deep_value",
                        "deep_integer": 42,
                        "deep_other_name": '{{scaffoldrom.project_name}}',
                        "deep_list": [
                            "deep value 1",
                            "{{scaffoldrom.project_name}}",
                            "deep value 3",
                        ],
                    },
                    "list_key": [
                        "value 1",
                        "{{scaffoldrom.project_name}}",
                        "value 3",
                    ],
                },
            }
        }

        scaffoldrom_dict = prompt.prompt_for_config(context, no_input=True)
        assert scaffoldrom_dict == {
            'project_name': "Slartibartfast",
            'details': {
                "key": "value",
                "integer_key": "37",
                "other_name": "Slartibartfast",
                "dict_key": {
                    "deep_key": "deep_value",
                    "deep_integer": "42",
                    "deep_other_name": "Slartibartfast",
                    "deep_list": ["deep value 1", "Slartibartfast", "deep value 3"],
                },
                "list_key": ["value 1", "Slartibartfast", "value 3"],
            },
        }

    def test_should_render_deep_dict_with_human_prompts(self):
        """Verify dict rendered correctly when human-readable prompts."""
        context = {
            'scaffoldrom': {
                'project_name': "Slartibartfast",
                'details': {
                    "key": "value",
                    "integer_key": 37,
                    "other_name": '{{scaffoldrom.project_name}}',
                    "dict_key": {
                        "deep_key": "deep_value",
                    },
                },
                '__prompts__': {'project_name': 'Project name'},
            }
        }
        scaffoldrom_dict = prompt.prompt_for_config(context, no_input=True)
        assert scaffoldrom_dict == {
            'project_name': "Slartibartfast",
            'details': {
                "key": "value",
                "integer_key": "37",
                "other_name": "Slartibartfast",
                "dict_key": {
                    "deep_key": "deep_value",
                },
            },
        }

    def test_internal_use_no_human_prompts(self):
        """Verify dict rendered correctly when human-readable prompts empty."""
        context = {
            'scaffoldrom': {
                'project_name': "Slartibartfast",
                '__prompts__': {},
            }
        }
        scaffoldrom_dict = prompt.prompt_for_config(context, no_input=True)
        assert scaffoldrom_dict == {
            'project_name': "Slartibartfast",
        }

    def test_prompt_for_templated_config(self, monkeypatch):
        """Verify Jinja2 templating works in unicode prompts."""
        monkeypatch.setattr(
            'scaffoldrom.prompt.read_user_variable',
            lambda var, default, prompts, prefix: default,
        )
        context = {
            'scaffoldrom': OrderedDict(
                [
                    ('project_name', 'A New Project'),
                    (
                        'pkg_name',
                        '{{ scaffoldrom.project_name|lower|replace(" ", "") }}',
                    ),
                ]
            )
        }

        exp_scaffoldrom_dict = {
            'project_name': 'A New Project',
            'pkg_name': 'anewproject',
        }
        scaffoldrom_dict = prompt.prompt_for_config(context)
        assert scaffoldrom_dict == exp_scaffoldrom_dict

    def test_dont_prompt_for_private_context_var(self, monkeypatch):
        """Verify `read_user_variable` not called for private context variables."""
        monkeypatch.setattr(
            'scaffoldrom.prompt.read_user_variable',
            lambda var, default: pytest.fail(
                'Should not try to read a response for private context var'
            ),
        )
        context = {'scaffoldrom': {'_copy_without_render': ['*.html']}}
        scaffoldrom_dict = prompt.prompt_for_config(context)
        assert scaffoldrom_dict == {'_copy_without_render': ['*.html']}

    def test_should_render_private_variables_with_two_underscores(self):
        """Test rendering of private variables with two underscores.

        There are three cases:
        1. Variables beginning with a single underscore are private and not rendered.
        2. Variables beginning with a double underscore are private and are rendered.
        3. Variables beginning with anything other than underscores are not private and
           are rendered.
        """
        context = {
            'scaffoldrom': OrderedDict(
                [
                    ('foo', 'Hello world'),
                    ('bar', 123),
                    ('rendered_foo', '{{ scaffoldrom.foo|lower }}'),
                    ('rendered_bar', 123),
                    ('_hidden_foo', '{{ scaffoldrom.foo|lower }}'),
                    ('_hidden_bar', 123),
                    ('__rendered_hidden_foo', '{{ scaffoldrom.foo|lower }}'),
                    ('__rendered_hidden_bar', 123),
                ]
            )
        }
        scaffoldrom_dict = prompt.prompt_for_config(context, no_input=True)
        assert scaffoldrom_dict == OrderedDict(
            [
                ('foo', 'Hello world'),
                ('bar', '123'),
                ('rendered_foo', 'hello world'),
                ('rendered_bar', '123'),
                ('_hidden_foo', '{{ scaffoldrom.foo|lower }}'),
                ('_hidden_bar', 123),
                ('__rendered_hidden_foo', 'hello world'),
                ('__rendered_hidden_bar', '123'),
            ]
        )

    def test_should_not_render_private_variables(self):
        """Verify private(underscored) variables not rendered by `prompt_for_config`.

        Private variables designed to be raw, same as context input.
        """
        context = {
            'scaffoldrom': {
                'project_name': 'Skip render',
                '_skip_jinja_template': '{{scaffoldrom.project_name}}',
                '_skip_float': 123.25,
                '_skip_integer': 123,
                '_skip_boolean': True,
                '_skip_nested': True,
            }
        }
        scaffoldrom_dict = prompt.prompt_for_config(context, no_input=True)
        assert scaffoldrom_dict == context['scaffoldrom']


DEFAULT_PREFIX = '  [dim][1/1][/] '


class TestReadUserChoice:
    """Class to unite choices prompt related tests."""

    def test_should_invoke_read_user_choice(self, mocker):
        """Verify correct function called for select(list) variables."""
        prompt_choice = mocker.patch(
            'scaffoldrom.prompt.prompt_choice_for_config',
            wraps=prompt.prompt_choice_for_config,
        )

        read_user_choice = mocker.patch('scaffoldrom.prompt.read_user_choice')
        read_user_choice.return_value = 'all'

        read_user_variable = mocker.patch('scaffoldrom.prompt.read_user_variable')

        choices = ['landscape', 'portrait', 'all']
        context = {'scaffoldrom': {'orientation': choices}}

        scaffoldrom_dict = prompt.prompt_for_config(context)

        assert not read_user_variable.called
        assert prompt_choice.called
        read_user_choice.assert_called_once_with(
            'orientation', choices, {}, DEFAULT_PREFIX
        )
        assert scaffoldrom_dict == {'orientation': 'all'}

    def test_should_invoke_read_user_variable(self, mocker):
        """Verify correct function called for string input variables."""
        read_user_variable = mocker.patch('scaffoldrom.prompt.read_user_variable')
        read_user_variable.return_value = 'Audrey Roy'

        prompt_choice = mocker.patch('scaffoldrom.prompt.prompt_choice_for_config')

        read_user_choice = mocker.patch('scaffoldrom.prompt.read_user_choice')

        context = {'scaffoldrom': {'full_name': 'Your Name'}}

        scaffoldrom_dict = prompt.prompt_for_config(context)

        assert not prompt_choice.called
        assert not read_user_choice.called
        read_user_variable.assert_called_once_with(
            'full_name', 'Your Name', {}, DEFAULT_PREFIX
        )
        assert scaffoldrom_dict == {'full_name': 'Audrey Roy'}

    def test_should_render_choices(self, mocker):
        """Verify Jinja2 templating engine works inside choices variables."""
        read_user_choice = mocker.patch('scaffoldrom.prompt.read_user_choice')
        read_user_choice.return_value = 'anewproject'

        read_user_variable = mocker.patch('scaffoldrom.prompt.read_user_variable')
        read_user_variable.return_value = 'A New Project'

        rendered_choices = ['foo', 'anewproject', 'bar']

        context = {
            'scaffoldrom': OrderedDict(
                [
                    ('project_name', 'A New Project'),
                    (
                        'pkg_name',
                        [
                            'foo',
                            '{{ scaffoldrom.project_name|lower|replace(" ", "") }}',
                            'bar',
                        ],
                    ),
                ]
            )
        }

        expected = {
            'project_name': 'A New Project',
            'pkg_name': 'anewproject',
        }
        scaffoldrom_dict = prompt.prompt_for_config(context)

        read_user_variable.assert_called_once_with(
            'project_name', 'A New Project', {}, '  [dim][1/2][/] '
        )
        read_user_choice.assert_called_once_with(
            'pkg_name', rendered_choices, {}, '  [dim][2/2][/] '
        )
        assert scaffoldrom_dict == expected


class TestPromptChoiceForConfig:
    """Class to unite choices prompt related tests with config test."""

    @pytest.fixture
    def choices(self):
        """Fixture. Just populate choices variable."""
        return ['landscape', 'portrait', 'all']

    @pytest.fixture
    def context(self, choices):
        """Fixture. Just populate context variable."""
        return {'scaffoldrom': {'orientation': choices}}

    def test_should_return_first_option_if_no_input(self, mocker, choices, context):
        """Verify prompt_choice_for_config return first list option on no_input=True."""
        read_user_choice = mocker.patch('scaffoldrom.prompt.read_user_choice')

        expected_choice = choices[0]

        actual_choice = prompt.prompt_choice_for_config(
            scaffoldrom_dict=context,
            env=environment.StrictEnvironment(),
            key='orientation',
            options=choices,
            no_input=True,  # Suppress user input
        )

        assert not read_user_choice.called
        assert expected_choice == actual_choice

    def test_should_read_user_choice(self, mocker, choices, context):
        """Verify prompt_choice_for_config return user selection on no_input=False."""
        read_user_choice = mocker.patch('scaffoldrom.prompt.read_user_choice')
        read_user_choice.return_value = 'all'

        expected_choice = 'all'

        actual_choice = prompt.prompt_choice_for_config(
            scaffoldrom_dict=context,
            env=environment.StrictEnvironment(),
            key='orientation',
            options=choices,
            no_input=False,  # Ask the user for input
        )
        read_user_choice.assert_called_once_with('orientation', choices, None, '')
        assert expected_choice == actual_choice


class TestReadUserYesNo(object):
    """Class to unite boolean prompt related tests."""

    @pytest.mark.parametrize(
        'run_as_docker',
        (
            True,
            False,
        ),
    )
    def test_should_invoke_read_user_yes_no(self, mocker, run_as_docker):
        """Verify correct function called for boolean variables."""
        read_user_yes_no = mocker.patch('scaffoldrom.prompt.read_user_yes_no')
        read_user_yes_no.return_value = run_as_docker

        read_user_variable = mocker.patch('scaffoldrom.prompt.read_user_variable')

        context = {'scaffoldrom': {'run_as_docker': run_as_docker}}

        scaffoldrom_dict = prompt.prompt_for_config(context)

        assert not read_user_variable.called
        read_user_yes_no.assert_called_once_with(
            'run_as_docker', run_as_docker, {}, DEFAULT_PREFIX
        )
        assert scaffoldrom_dict == {'run_as_docker': run_as_docker}

    def test_boolean_parameter_no_input(self):
        """Verify boolean parameter sent to prompt for config with no input."""
        context = {
            'scaffoldrom': {
                'run_as_docker': True,
            }
        }
        scaffoldrom_dict = prompt.prompt_for_config(context, no_input=True)
        assert scaffoldrom_dict == context['scaffoldrom']


@pytest.mark.parametrize(
    'context',
    (
        {'scaffoldrom': {'foo': '{{scaffoldrom.nope}}'}},
        {'scaffoldrom': {'foo': ['123', '{{scaffoldrom.nope}}', '456']}},
        {'scaffoldrom': {'foo': {'{{scaffoldrom.nope}}': 'value'}}},
        {'scaffoldrom': {'foo': {'key': '{{scaffoldrom.nope}}'}}},
    ),
    ids=[
        'Undefined variable in scaffoldrom dict',
        'Undefined variable in scaffoldrom dict with choices',
        'Undefined variable in scaffoldrom dict with dict_key',
        'Undefined variable in scaffoldrom dict with key_value',
    ],
)
def test_undefined_variable(context):
    """Verify `prompt.prompt_for_config` raises correct error."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        prompt.prompt_for_config(context, no_input=True)

    error = err.value
    assert error.message == "Unable to render variable 'foo'"
    assert error.context == context
