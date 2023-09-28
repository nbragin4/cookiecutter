.. _tutorial2:

==================================
Create a Scaffoldrom From Scratch
==================================

In this tutorial, we are creating `scaffoldrom-website-simple`, a scaffoldrom for generating simple, bare-bones websites.

Step 1: Name Your Scaffoldrom
------------------------------

Create the directory for your scaffoldrom and cd into it:

.. code-block:: bash

    $ mkdir scaffoldrom-website-simple
    $ cd scaffoldrom-website-simple/

Step 2: Create scaffoldrom.json
----------------------------------

`scaffoldrom.json` is a JSON file that contains fields which can be referenced in the scaffoldrom template. For each, default value is defined and user will be prompted for input during scaffoldrom execution. Only mandatory field is `project_slug` and it should comply with package naming conventions defined in `PEP8 Naming Conventions <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_ .

.. code-block:: json

    {
      "project_name": "Scaffoldrom Website Simple",
      "project_slug": "{{ scaffoldrom.project_name.lower().replace(' ', '_') }}",
      "author": "Anonymous"
    }


Step 3: Create project_slug Directory
---------------------------------------

Create a directory called `{{ scaffoldrom.project_slug }}`.

This value will be replaced with the repo name of projects that you generate from this scaffoldrom.

Step 4: Create index.html
--------------------------

Inside of `{{ scaffoldrom.project_slug }}`, create `index.html` with following content:

.. code-block:: html

    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>{{ scaffoldrom.project_name }}</title>
        </head>

        <body>
            <h1>{{ scaffoldrom.project_name }}</h1>
            <p>by {{ scaffoldrom.author }}</p>
        </body>
    </html>

Step 5: Pack scaffoldrom into ZIP
----------------------------------
There are many ways to run Scaffoldrom templates, and they are described in details in `Usage chapter <https://scaffoldrom.readthedocs.io/en/latest/usage.html#grab-a-scaffoldrom-template>`_. In this tutorial we are going to ZIP scaffoldrom and then run it for testing.

By running following command `scaffoldrom.zip` will get generated which can be used to run scaffoldrom. Script will generate `scaffoldrom.zip` ZIP file and echo full path to the file.

.. code-block:: bash

   $ (SOURCE_DIR=$(basename $PWD) ZIP=scaffoldrom.zip && # Set variables
   pushd .. && # Set parent directory as working directory
   zip -r $ZIP $SOURCE_DIR --exclude $SOURCE_DIR/$ZIP --quiet && # ZIP scaffoldrom
   mv $ZIP $SOURCE_DIR/$ZIP && # Move ZIP to original directory
   popd && # Restore original work directory
   echo  "Scaffoldrom full path: $PWD/$ZIP")

Step 6: Run scaffoldrom
------------------------
Set your work directory to whatever directory you would like to run scaffoldrom at. Use scaffoldrom full path and run the following command:

.. code-block:: bash

   $ scaffoldrom <replace with Scaffoldrom full path>

You can expect similar output:

.. code-block:: bash

   $ scaffoldrom /Users/admin/scaffoldrom-website-simple/scaffoldrom.zip
   project_name [Scaffoldrom Website Simple]: Test web
   project_slug [test_web]:
   author [Anonymous]: Scaffoldrom Developer

Resulting directory should be inside your work directory with a name that matches `project_slug` you defined. Inside that directory there should be `index.html` with generated source:

.. code-block:: html

    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Test web</title>
        </head>

        <body>
            <h1>Scaffoldrom Developer</h1>
            <p>by Test web</p>
        </body>
    </html>
