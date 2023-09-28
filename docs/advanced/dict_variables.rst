.. _dict-variables:

Dictionary Variables
--------------------

*New in Scaffoldrom 1.5*

Dictionary variables provide a way to define deep structured information when rendering a template.

Basic Usage
~~~~~~~~~~~

Dictionary variables are, as the name suggests, dictionaries of key-value pairs.
The dictionary values can, themselves, be other dictionaries and lists - the data structure can be as deep as you need.

For example, you could provide the following dictionary variable in your ``scaffoldrom.json``:

.. code-block:: json

    {
        "project_slug": "new_project",
        "file_types": {
            "png": {
                "name": "Portable Network Graphic",
                "library": "libpng",
                "apps": [
                    "GIMP"
                ]
            },
            "bmp": {
                "name": "Bitmap",
                "library": "libbmp",
                "apps": [
                    "Paint",
                    "GIMP"
                ]
            }
        }
    }


The above ``file_types`` dictionary variable creates ``scaffoldrom.file_types``, which can be used like this:

.. code-block:: html+jinja

    {% for extension, details in scaffoldrom.file_types|dictsort %}
    <dl>
      <dt>Format name:</dt>
      <dd>{{ details.name }}</dd>

      <dt>Extension:</dt>
      <dd>{{ extension }}</dd>

      <dt>Applications:</dt>
      <dd>
          <ul>
          {% for app in details.apps -%}
              <li>{{ app }}</li>
          {% endfor -%}
          </ul>
      </dd>
    </dl>
    {% endfor %}


Scaffoldrom is using `Jinja2's for expression <https://jinja.palletsprojects.com/en/latest/templates/#for>`_ to iterate over the items in the dictionary.
