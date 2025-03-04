"""
Main entry point for the `scaffoldrom` command.

The code in this module is also a good example of how to use Scaffoldrom as a
library rather than a script.
"""
from collections import OrderedDict
import json
import logging
import os
import re
import sys
from copy import copy

from scaffoldrom.config import get_user_config
from scaffoldrom.exceptions import InvalidModeException
from scaffoldrom.generate import generate_context, generate_files
from scaffoldrom.merging import merger
from scaffoldrom.ordered_yaml import ordered_dump
from scaffoldrom.prompt import prompt_for_config
from scaffoldrom.values import dump, load
from scaffoldrom.repository import determine_repo_dir
from scaffoldrom.utils import rmtree

logger = logging.getLogger(__name__)


def scaffoldrom(
    template,
    checkout=None,
    no_input=False,
    extra_context=None,
    values=None,
    overwrite_if_exists=False,
    output_dir='.',
    config_file=None,
    default_config=False,
    password=None,
    directory=None,
    skip_if_file_exists=False,
    accept_hooks=True,
    keep_project_on_failure=False,
):
    """
    Run Scaffoldrom just as if using it from the command line.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Do not prompt for user input.
        Use default values for template parameters taken from `scaffoldrom.yaml`, user
        config and `extra_dict`. Force a refresh of cached resources.
    :param extra_context: A dictionary of context that overrides default
        and user configuration.
    :param values: Do not prompt for input, instead read from saved json. If
        ``True`` read from the ``values_dir``.
        if it exists
    :param output_dir: Where to output the generated project dir into.
    :param config_file: User configuration file path.
    :param default_config: Use default values rather than a config file.
    :param password: The password to use when extracting the repository.
    :param directory: Relative path to a scaffoldrom template in a repository.
    :param accept_hooks: Accept pre and post hooks if set to `True`.
    :param keep_project_on_failure: If `True` keep generated project directory even when
        generation fails
    """
    # if (values or (no_input is not False)) and (extra_context is not None):
    #     err_msg = (
    #         "You can not use both values and no_input or extra_context "
    #         "at the same time."
    #     )
    #     raise InvalidModeException(err_msg)

    config_dict = get_user_config(
        config_file=config_file,
        default_config=default_config,
    )

    repo_dir, cleanup = determine_repo_dir(
        template=template,
        abbreviations=config_dict['abbreviations'],
        clone_to_dir=config_dict['scaffoldroms_dir'],
        checkout=checkout,
        no_input=no_input,
        password=password,
        directory=directory,
    )
    import_patch = _patch_import_path_for_repo(repo_dir)

    template_name = os.path.basename(os.path.abspath(repo_dir))

    if values:
        with import_patch:
            if isinstance(values, bool):
                context_from_valuesfile = load(config_dict['values_dir'], template_name)
            else:
                path, template_name = os.path.split(os.path.splitext(values)[0])
                context_from_valuesfile = load(path, template_name)

    context_file = os.path.join(repo_dir, 'scaffoldrom.yaml')
    logger.debug('context_file is %s', context_file)

    if values:
        context = generate_context(
            context_file=context_file,
            default_context=config_dict['default_context'],
            extra_context=None,
        )
        merger.merge(context_from_valuesfile, OrderedDict(scaffoldrom=(extra_context or OrderedDict())))
        logger.debug('valuesfile context: %s', context_from_valuesfile)
        items_for_prompting = {
            k: v
            for k, v in context['scaffoldrom'].items()
            if k not in context_from_valuesfile['scaffoldrom'].keys()
        }
        context_for_prompting = {}
        context_for_prompting['scaffoldrom'] = items_for_prompting
        context = merger.merge(context.copy(), context_from_valuesfile)
        logger.debug('prompting context: %s', context_for_prompting)
    else:
        context = generate_context(
            context_file=context_file,
            default_context=config_dict['default_context'],
            extra_context=extra_context,
        )
        context_for_prompting = context
    # preserve the original scaffoldrom options
    # print(context['scaffoldrom'])
    context['_scaffoldrom'] = {
        k: v for k, v in context['scaffoldrom'].items() if not k.startswith("_")
    }

    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set

    with import_patch:
        if context_for_prompting['scaffoldrom']:
            context['scaffoldrom'].update(
                prompt_for_config(context_for_prompting, no_input, global_context=context)
            )
        if "template" in context["scaffoldrom"]:
            nested_template = re.search(
                r'\((.*?)\)', context["scaffoldrom"]["template"]
            ).group(1)
            return scaffoldrom(
                template=os.path.join(repo_dir, nested_template),
                checkout=checkout,
                no_input=no_input,
                extra_context=extra_context,
                values=values,
                overwrite_if_exists=overwrite_if_exists,
                output_dir=output_dir,
                config_file=config_file,
                default_config=default_config,
                password=password,
                directory=directory,
                skip_if_file_exists=skip_if_file_exists,
                accept_hooks=accept_hooks,
                keep_project_on_failure=keep_project_on_failure,
            )

    logger.debug('context is %s', context)

    # include template dir or url in the context dict
    context['scaffoldrom']['_template'] = template

    # include output+dir in the context dict
    context['scaffoldrom']['_output_dir'] = os.path.abspath(output_dir)

    # include repo dir or url in the context dict
    context['scaffoldrom']['_repo_dir'] = repo_dir

    # include checkout details in the context dict
    context['scaffoldrom']['_checkout'] = checkout

    dump(config_dict['values_dir'], template_name, context)

    # Create project from local context and project template.
    with import_patch:
        result = generate_files(
            repo_dir=repo_dir,
            context=context,
            overwrite_if_exists=overwrite_if_exists,
            skip_if_file_exists=skip_if_file_exists,
            output_dir=output_dir,
            accept_hooks=accept_hooks,
            keep_project_on_failure=keep_project_on_failure,
        )

    # Cleanup (if required)
    if cleanup:
        rmtree(repo_dir)

    return result


class _patch_import_path_for_repo:
    def __init__(self, repo_dir):
        self._repo_dir = repo_dir
        self._path = None

    def __enter__(self):
        self._path = copy(sys.path)
        sys.path.append(self._repo_dir)

    def __exit__(self, type, value, traceback):
        sys.path = self._path
