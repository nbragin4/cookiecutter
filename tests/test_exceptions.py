"""Collection of tests around general exception handling."""
from jinja2.exceptions import UndefinedError

from scaffoldrom import exceptions


def test_undefined_variable_to_str():
    """Verify string representation of errors formatted in expected form."""
    undefined_var_error = exceptions.UndefinedVariableInTemplate(
        'Beautiful is better than ugly',
        UndefinedError('Errors should never pass silently'),
        {'scaffoldrom': {'foo': 'bar'}},
    )

    expected_str = (
        "Beautiful is better than ugly. "
        "Error message: Errors should never pass silently. "
        "Context: {'scaffoldrom': {'foo': 'bar'}}"
    )

    assert str(undefined_var_error) == expected_str
