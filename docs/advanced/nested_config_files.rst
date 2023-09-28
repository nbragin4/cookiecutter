.. _nested-config-files:

Nested configuration files
----------------------------------------------

If you wish to create a hierarchy of templates and use scaffoldrom to choose among them,
you need just to specify the key ``template`` in the main configuration file to reach
the other ones.

Let's imagine to have the following structure::

    main-directory/
        ├── project-1
        │   ├── scaffoldrom.json
        │   ├── {{scaffoldrom.project_slug}}
        |	│   ├── ...
        ├── project-2
        │   ├── scaffoldrom.json
        │   ├── {{scaffoldrom.project_slug}}
        |	│   ├── ...
        └── scaffoldrom.json

It is possible to specify in the main ``scaffoldrom.json`` how to reach the other
config files as follows:

.. code-block:: JSON

    {
        "template": [
            "Project 1 (./project-1)",
            "Project 2 (./project-2)"
        ]
    }

Then, when ``scaffoldrom`` is launched in the main directory it will ask to choice
among the possible templates:

.. code-block:: bash

    Select template:
    1 - Project 1 (./project-1)
    2 - Project 2 (./project-2)
    Choose from 1, 2 [1]:

Once a template is chosen, for example ``1``, it will continue to ask the info required by
``scaffoldrom.json`` in the ``project-1`` folder, such as ``project-slug``
