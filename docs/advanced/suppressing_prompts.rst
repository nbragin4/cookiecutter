.. _suppressing-command-line-prompts:

Suppressing Command-Line Prompts
--------------------------------

To suppress the prompts asking for input, use ``no_input``.

Note: this option will force a refresh of cached resources.

Basic Example: Using the Defaults
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scaffoldrom will pick a default value if used with ``no_input``:

.. code-block:: python

    from scaffoldrom.main import scaffoldrom
    scaffoldrom(
        'scaffoldrom-django',
        no_input=True,
    )

In this case it will be using the default defined in ``scaffoldrom.json`` or ``.scaffoldromrc``.

.. note::
   values from ``scaffoldrom.json`` will be overridden by values from  ``.scaffoldromrc``

Advanced Example: Defaults + Extra Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you combine an ``extra_context`` dict with the ``no_input`` argument, you can programmatically create the project with a set list of context parameters and without any command line prompts:

.. code-block:: python

    scaffoldrom('scaffoldrom-pypackage/',
                 no_input=True,
                 extra_context={'project_name': 'TheGreatest'})


See also :ref:`injecting-extra-content` and the :ref:`API Reference <apiref>` for more details.
