.. _user-config:

User Config
===========

*New in Scaffoldrom 0.7*

If you use Scaffoldrom a lot, you'll find it useful to have a user config file.
By default Scaffoldrom tries to retrieve settings from a `.scaffoldromrc` file in your home directory.

*New in Scaffoldrom 1.3*

You can also specify a config file on the command line via ``--config-file``.

.. code-block:: bash

    scaffoldrom --config-file /home/audreyr/my-custom-config.yaml scaffoldrom-pypackage

Or you can set the ``SCAFFOLDROM_CONFIG`` environment variable:

.. code-block:: bash

    export SCAFFOLDROM_CONFIG=/home/audreyr/my-custom-config.yaml

If you wish to stick to the built-in config and not load any user config file at all, use the CLI option ``--default-config`` instead.
Preventing Scaffoldrom from loading user settings is crucial for writing integration tests in an isolated environment.

Example user config:

.. code-block:: yaml

    default_context:
        full_name: "Audrey Roy"
        email: "audreyr@example.com"
        github_username: "audreyr"
    scaffoldroms_dir: "/home/audreyr/my-custom-scaffoldroms-dir/"
    values_dir: "/home/audreyr/my-custom-values-dir/"
    abbreviations:
        pp: https://github.com/audreyfeldroy/scaffoldrom-pypackage.git
        gh: https://github.com/{0}.git
        bb: https://bitbucket.org/{0}

Possible settings are:

``default_context``:
    A list of key/value pairs that you want injected as context whenever you generate a project with Scaffoldrom.
    These values are treated like the defaults in ``scaffoldrom.json``, upon generation of any project.
``scaffoldroms_dir``
    Directory where your scaffoldroms are cloned to when you use Scaffoldrom with a repo argument.
``values_dir``
    Directory where Scaffoldrom dumps context data to, which you can fetch later on when using the
    :ref:`values feature <values-feature>`.
``abbreviations``
    A list of abbreviations for scaffoldroms.
    Abbreviations can be simple aliases for a repo name, or can be used as a prefix, in the form ``abbr:suffix``.
    Any suffix will be inserted into the expansion in place of the text ``{0}``, using standard Python string formatting.
    With the above aliases, you could use the ``scaffoldrom-pypackage`` template simply by saying ``scaffoldrom pp``, or ``scaffoldrom gh:audreyr/scaffoldrom-pypackage``.
    The ``gh`` (GitHub), ``bb`` (Bitbucket), and ``gl`` (Gitlab) abbreviations shown above are actually **built in**, and can be used without defining them yourself.

Read also: :ref:`injecting-extra-content`
