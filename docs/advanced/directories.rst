.. _directories:

Organizing scaffoldroms in directories
---------------------------------------

*New in Scaffoldrom 1.7*

Scaffoldrom introduces the ability to organize several templates in one repository or zip file, separating them by directories.
This allows using symlinks for general files.
Here's an example repository demonstrating this feature::

    https://github.com/user/repo-name.git
        ├── directory1-name/
        |   ├── {{scaffoldrom.project_slug}}/
        |   └── scaffoldrom.json
        └── directory2-name/
            ├── {{scaffoldrom.project_slug}}/
            └── scaffoldrom.json

To activate one of templates within a subdirectory, use the ``--directory`` option:

.. code-block:: bash

    scaffoldrom https://github.com/user/repo-name.git --directory="directory1-name"
