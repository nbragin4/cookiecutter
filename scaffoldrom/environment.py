"""Jinja2 environment and extensions loading."""
import copy
from collections import OrderedDict
from jinja2 import Environment, StrictUndefined, Template

from scaffoldrom.exceptions import UnknownExtension

class ScaffoldromTemplate(Template):
    """Custom template class provide flexible way to access scaffoldrom variables in context"""
    def new_context(
        self,
        vars = None,
        shared: bool = False,
        locals = None,
    ):
        """Create a new :class:`Context` for this template.  The vars
        provided will be passed to the template.  Per default the globals
        are added to the context.  If shared is set to `True` the data
        is passed as is to the context without adding the globals.

        `locals` can be a dict of local variables for internal usage.
        """
        vars.update(copy.deepcopy(vars.get('scaffoldrom', OrderedDict({}))))
        return super().new_context(vars=vars, shared=shared, locals=locals)

class ExtensionLoaderMixin:
    """Mixin providing sane loading of extensions specified in a given context.

    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    """

    def __init__(self, **kwargs):
        """Initialize the Jinja2 Environment object while loading extensions.

        Does the following:

        1. Establishes default_extensions (currently just a Time feature)
        2. Reads extensions set in the scaffoldrom.yaml _extensions key.
        3. Attempts to load the extensions. Provides useful error if fails.
        """
        context = kwargs.pop('context', {})

        default_extensions = [
            'scaffoldrom.extensions.YamlifyExtension',
            'scaffoldrom.extensions.JsonifyExtension',
            'scaffoldrom.extensions.RandomStringExtension',
            'scaffoldrom.extensions.SlugifyExtension',
            'scaffoldrom.extensions.TimeExtension',
            'scaffoldrom.extensions.UUIDExtension',
        ]
        extensions = default_extensions + self._read_extensions(context)

        try:
            super().__init__(extensions=extensions, **kwargs)
        except ImportError as err:
            raise UnknownExtension(f'Unable to load extension: {err}') from err

    def _read_extensions(self, context):
        """Return list of extensions as str to be passed on to the Jinja2 env.

        If context does not contain the relevant info, return an empty
        list instead.
        """
        try:
            extensions = context['scaffoldrom']['_extensions']
        except KeyError:
            return []
        else:
            return [str(ext) for ext in extensions]


class StrictEnvironment(ExtensionLoaderMixin, Environment):
    """Create strict Jinja2 environment.

    Jinja2 environment will raise error on undefined variable in template-
    rendering context.
    """

    def __init__(self, **kwargs):
        """Set the standard Scaffoldrom StrictEnvironment.

        Used to update context to access variables outside of scaffoldrom var
        Also loading extensions defined in scaffoldrom.yaml's _extensions key.
        """
        self.template_class = ScaffoldromTemplate
        context = kwargs.pop('context', {})
        scaffoldrom: OrderedDict = copy.deepcopy(context.get('scaffoldrom', OrderedDict({})))
        scaffoldrom.update(context)
        del context
        kwargs["context"]=scaffoldrom

        super().__init__(undefined=StrictUndefined, **kwargs)
