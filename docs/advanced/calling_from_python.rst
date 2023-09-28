.. _calling-from-python:

Calling Scaffoldrom Functions From Python
------------------------------------------

You can use Scaffoldrom from Python:

.. code-block:: python

    from scaffoldrom.main import scaffoldrom

    # Create project from the scaffoldrom-pypackage/ template
    scaffoldrom('scaffoldrom-pypackage/')

    # Create project from the scaffoldrom-pypackage.git repo template
    scaffoldrom('https://github.com/audreyfeldroy/scaffoldrom-pypackage.git')

This is useful if, for example, you're writing a web framework and need to provide developers with a tool similar to `django-admin.py startproject` or `npm init`.

See the :ref:`API Reference <apiref>` for more details.
