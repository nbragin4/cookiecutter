.. _`template extensions`:

Template Extensions
-------------------

*New in Scaffoldrom 1.4*

A template may extend the Scaffoldrom environment with custom `Jinja2 extensions`_.
It can add extra filters, tests, globals or even extend the parser.

To do so, a template author must specify the required extensions in ``scaffoldrom.yaml`` as follows:

.. code-block:: json

    {
        "project_slug": "Foobar",
        "year": "{% now 'utc', '%Y' %}",
        "_extensions": ["jinja2_time.TimeExtension"]
    }

On invocation Scaffoldrom tries to import the extensions and add them to its environment respectively.

In the above example, Scaffoldrom provides the additional tag `now`_, after installing the `jinja2_time.TimeExtension`_ and enabling it in ``scaffoldrom.yaml``.

Please note that Scaffoldrom will **not** install any dependencies on its own!
As a user you need to make sure you have all the extensions installed, before running Scaffoldrom on a template that requires custom Jinja2 extensions.

By default Scaffoldrom includes the following extensions:

- ``scaffoldrom.extensions.JsonifyExtension``
- ``scaffoldrom.extensions.RandomStringExtension``
- ``scaffoldrom.extensions.SlugifyExtension``
- ``scaffoldrom.extensions.TimeExtension``
- ``scaffoldrom.extensions.UUIDExtension``

.. warning::

    The above is just an example to demonstrate how this is used. There is no
    need to require ``jinja2_time.TimeExtension``, since its functionality is
    included by default (by ``scaffoldrom.extensions.TimeExtension``) without
    needing an extra install.

Jsonify extension
~~~~~~~~~~~~~~~~~

The ``scaffoldrom.extensions.JsonifyExtension`` extension provides a ``jsonify`` filter in templates that converts a Python object to JSON:

.. code-block:: jinja

    {% {'a': True} | jsonify %}

Would output:

.. code-block:: json

    {"a": true}

Random string extension
~~~~~~~~~~~~~~~~~~~~~~~

*New in Scaffoldrom 1.7*

The ``scaffoldrom.extensions.RandomStringExtension`` extension provides a ``random_ascii_string`` method in templates that generates a random fixed-length string, optionally with punctuation.

Generate a random n-size character string.
Example for n=12:

.. code-block:: jinja

    {{ random_ascii_string(12) }}

Outputs:

.. code-block:: text

    bIIUczoNvswh

The second argument controls if punctuation and special characters ``!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~`` should be present in the result:

.. code-block:: jinja

    {{ random_ascii_string(12, punctuation=True) }}

Outputs:

.. code-block:: text

    fQupUkY}W!)!

Slugify extension
~~~~~~~~~~~~~~~~~

The ``scaffoldrom.extensions.SlugifyExtension`` extension provides a ``slugify`` filter in templates that converts string into its dashed ("slugified") version:

.. code-block:: jinja

    {% "It's a random version" | slugify %}

Would output:

::

    it-s-a-random-version

It is different from a mere replace of spaces since it also treats some special characters differently such as ``'`` in the example above.
The function accepts all arguments that can be passed to the ``slugify`` function of `python-slugify`_.
For example to change the output from ``it-s-a-random-version``` to ``it_s_a_random_version``, the ``separator`` parameter would be passed: ``slugify(separator='_')``.

.. _`Jinja2 extensions`: https://jinja.palletsprojects.com/en/latest/extensions/
.. _`now`: https://github.com/hackebrot/jinja2-time#now-tag
.. _`jinja2_time.TimeExtension`: https://github.com/hackebrot/jinja2-time
.. _`python-slugify`: https://pypi.org/project/python-slugify

UUID4 extension
~~~~~~~~~~~~~~~~~~~~~~~

*New in Scaffoldrom 1.x*

The ``scaffoldrom.extensions.UUIDExtension`` extension provides a ``uuid4()``
method in templates that generates a uuid4.

Generate a uuid4 string:

.. code-block:: jinja

    {{ uuid4() }}

Outputs:

.. code-block:: text

    83b5de62-31b4-4a1e-83fa-8c548de65a11
