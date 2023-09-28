.. _injecting-extra-content:

Injecting Extra Context
-----------------------

You can specify an ``extra_context`` dictionary that will override values from ``scaffoldrom.json`` or ``.scaffoldromrc``:

.. code-block:: python

    scaffoldrom(
        'scaffoldrom-pypackage/',
        extra_context={'project_name': 'TheGreatest'},
    )

This works as command-line parameters as well:

.. code-block:: bash

    scaffoldrom --no-input scaffoldrom-pypackage/ project_name=TheGreatest

You will also need to add these keys to the ``scaffoldrom.json`` or ``.scaffoldromrc``.


Example: Injecting a Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have ``scaffoldrom.json`` that has the following keys:

.. code-block:: JSON

    {
        "timestamp": "{{ scaffoldrom.timestamp }}"
    }


This Python script will dynamically inject a timestamp value as the project is
generated:

.. code-block:: python

    from scaffoldrom.main import scaffoldrom

    from datetime import datetime

    scaffoldrom(
        'scaffoldrom-django',
        extra_context={'timestamp': datetime.utcnow().isoformat()}
    )

How this works:

1. The script uses ``datetime`` to get the current UTC time in ISO format.
2. To generate the project, ``scaffoldrom()`` is called, passing the timestamp
   in as context via the ``extra_context``` dict.
