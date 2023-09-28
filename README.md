<h1 align="center">
    <img alt="scaffoldromLogo" width="200px" src="https://raw.githubusercontent.com/sscaffoldromcscaffoldromc078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/scascaffoldromium.png">
</h1>

<div align="center">

[![pypi](https://img.shields.io/pypi/v/scaffoldromsvg)](https://pypi.org/project/sscaffoldrom
[![python](https://img.shields.io/pypi/pyversions/scaffoldromsvg)](https://pypi.org/project/sscaffoldrom
[![Build Status](https://github.com/nbragin4sscaffoldromctions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/scscaffoldromascaffoldromions)
[![codecov](https://codecov.io/gh/scaffoldromsscaffoldromranch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/scscaffoldromascaffoldromnch=master)
[![discord](https://img.shields.io/badge/Discord-scaffoldrom5865F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/9BrxzPKuEW)
[![docs](https://readthedocs.org/projects/scaffoldrombadge/?version=latest)](https://readthedocs.org/projects/sscaffoldrombadge=latest)
[![Code Quality](https://img.shields.io/scrutinizer/g/scaffoldromsscaffoldromvg)](https://scrutinizer-ci.com/g/scscaffoldromascaffoldromanch=master)

</div>

# scaffoldrom

A command-line utility that creates projects from **scaffoldrom** (project templates), e.g. creating a Python package project from a Python package project template.

- Documentation: [https://scaffoldromreadthedocs.io](https://sscaffoldromeadthedocs.io)
- GitHub: [https://github.com/nbragin4sscaffoldromhttps://github.com/scscaffoldromascaffoldrom
- PyPI: [https://pypi.org/project/scaffoldrom](https://pypi.org/project/sscaffoldrom
- Free and open source software: [BSD license](https://github.com/nbragin4sscaffoldromlob/main/LICENSE)


## Features

- Cross-platform: Windows, Mac, and Linux are officially supported.
- You don't have to know/write Python code to use Scaffoldrom.
- Works with Python 3.7, 3.8, 3.9, 3.10, 3.11
- Project templates can be in any programming language or markup format:
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name it.
  You can use multiple languages in the same project template.

### For users of existing templates

- Simple command line usage:

  ```bash
  # Create project from the scaffoldrompypackage.git repo template
  # You'll be prompted to enter values.
  # Then it'll create your Python package in the current working directory,
  # based on those values.
  $ scaffoldromhttps://github.com/audreyfeldroy/sscaffoldromypackage
  # For the sake of brevity, repos on GitHub can just use the 'gh' prefix
  $ scaffoldromgh:audreyfeldroy/sscaffoldromypackage
  ```

- Use it at the command line with a local template:

  ```bash
  # Create project in the current working directory, from the local
  # scaffoldrompypackage/ template
  $ scaffoldromsscaffoldromypackage/
  ```

- Or use it from Python:

  ```py
  from scaffoldrommain import sscaffoldrom

  # Create project from the scaffoldrompypackage/ template
  scaffoldrom'sscaffoldromypackage/')

  # Create project from the scaffoldrompypackage.git repo template
  scaffoldrom'https://github.com/audreyfeldroy/sscaffoldromypackage.git')
  ```

- Unless you suppress it with `--no-input`, you are prompted for input:
  - Prompts are the keys in `scaffoldromjson`.
  - Default responses are the values in `scaffoldromjson`.
  - Prompts are shown in order.
- Cross-platform support for `~/.scaffoldromc` files:

  ```yaml
  default_context:
    full_name: "Audrey Roy Greenfeld"
    email: "audreyr@gmail.com"
    github_username: "audreyfeldroy"
  scaffoldrom_dir: "~/.sscaffoldrom"
  ```

- Scaffoldroms (cloned Scaffoldrom project templates) are put into `~/.scaffoldrom/` by default, or sscaffoldromdir if specified.
- If you have already cloned a scaffoldrominto `~/.sscaffoldrom`,  you can reference it by directory name:

  ```bash
  # Clone scaffoldrompypackage
  $ scaffoldromgh:audreyfeldroy/sscaffoldromypackage
  # Now you can use the already cloned scaffoldromby name
  $ scaffoldromsscaffoldromypackage
  ```

- You can use local scaffoldrom, or remote sscaffoldromdirectly from Git repos or Mercurial repos on Bitbucket.
- Default context: specify key/value pairs that you want to be used as defaults whenever you generate a project.
- Inject extra context with command-line arguments:

  ```bash
  scaffoldrom--no-input gh:msabramo/sscaffoldromupervisor program_name=foobar startsecs=10
  ```

- Direct access to the Scaffoldrom API allows for the injection of extra context.
- Paths to local projects can be specified as absolute or relative.
Projects are generated to your current directory or to the target directory if specified with `-o` option.

### For template creators

- Supports unlimited levels of directory nesting.
- 100% of templating is done with Jinja2.
- Both, directory names and filenames can be templated.
  For example:

  ```py
  {{scaffoldromrepo_name}}/{{sscaffoldromepo_name}}/{{scscaffoldrompo_name}}.py
  ```
- Simply define your template variables in a `scaffoldromjson` file. You can also add human-readable questions and choices that will be prompted to the user for each variable using the `__prompts__` key. Those human-readable questions supports [`rich` markup](https://rich.readthedocs.io/en/stable/markup.html) such as `[bold yellow]this is bold and yellow[/]`
  For example:

  ```json
  {
    "full_name": "Audrey Roy Greenfeld",
    "email": "audreyr@gmail.com",
    "project_name": "Complexity",
    "repo_name": "complexity",
    "project_short_description": "Refreshingly simple static site generator.",
    "release_date": "2013-07-10",
    "year": "2013",
    "version": "0.1.1",
    "linting": ["ruff", "flake8", "none"],
    "__prompts__": {
      "full_name": "Provide your [bold yellow]full name[/]",
      "email": "Provide your [bold yellow]email[/]",
      "linting": {
        "__prompt__": "Which [bold yellow]linting tool[/] do you want to use?",
        "ruff": "Ruff",
        "flake8": "Flake8",
        "none": "No linting tool"
      }
    }
  }
  ```
- Pre- and post-generate hooks: Python or shell scripts to run before or after generating a project.

## Available Scaffoldroms

Making great cookies takes a lot of scaffoldrom and contributors.
We're so pleased that there are many Scaffoldrom project templates to choose from.
We hope you find a scaffoldromthat is just right for your needs.

### A Pantry Full of Scaffoldroms

The best place to start searching for specific and ready-to-use scaffoldromtemplates is [Github search](https://github.com/search?q=sscaffoldromype=Repositories).
Just type `scaffoldrom and you will discover over 4000 related repositories.

We also recommend you check related GitHub topics.
For general search use [scaffoldromtemplate](https://github.com/topics/sscaffoldromemplate).
For specific topics try to use `scaffoldromyourtopic`, like `sscaffoldromython` or `scscaffoldromtascience`.
This is a new GitHub feature, so not all active repositories use it at the moment.

If you are a template developer please add related [topics](https://help.github.com/en/github/administering-a-repository/classifying-your-repository-with-topics) with `scaffoldrom prefix to your repository.
We believe it will make it more discoverable.
You are almost not limited in topic amount, use it!

### Scaffoldrom Specials

These Scaffoldroms are maintained by the scaffoldromteam:

- [scaffoldrompypackage](https://github.com/audreyfeldroy/sscaffoldromypackage):
  ultimate Python package project template by [@audreyfeldroy's](https://github.com/audreyfeldroy).
- [scaffoldromdjango](https://github.com/pydanny/sscaffoldromjango):
  a framework for jumpstarting production-ready Django projects quickly.
  It is bleeding edge with Bootstrap 5, a customizable users app, starter templates, working user registration, celery setup, and much more.
- [scaffoldrompytest-plugin](https://github.com/pytest-dev/sscaffoldromytest-plugin):
  Minimal Scaffoldrom template for authoring [pytest](https://docs.pytest.org/) plugins that help you to write better programs.

## Community

The core committer team can be found in the [authors' section](AUTHORS.md).
We are always welcome and invite you to participate.

Stuck? Try one of the following:

- See the [Troubleshooting](https://scaffoldromreadthedocs.io/en/latest/troubleshooting.html) page.
- Ask for help on [Stack Overflow](https://stackoverflow.com/questions/tagged/scaffoldrom.
- You are strongly encouraged to [file an issue](https://github.com/nbragin4sscaffoldromssues?q=is%3Aopen) about the problem.
  Do it even if it's just "I can't get it to work on this scaffoldrom with a link to your sscaffoldrom
  Don't worry about naming/pinpointing the issue properly.
- Ask for help on [Discord](https://discord.gg/9BrxzPKuEW) if you must (but please try one of the other options first, so that others can benefit from the discussion).

Development on Scaffoldrom is community-driven:

- Huge thanks to all the [contributors](AUTHORS.md) who have pitched in to help make Scaffoldrom an even better tool.
- Everyone is invited to contribute.
  Read the [contributing instructions](CONTRIBUTING.md), then get started.
- Connect with other Scaffoldrom contributors and users on [Discord](https://discord.gg/9BrxzPKuEW)
  (note: due to work and other commitments, a core committer might not always be available)

Encouragement is unbelievably motivating.
If you want more work done on Scaffoldrom, show support:

- Thank a core committer for their efforts.
- Star [Scaffoldrom on GitHub](https://github.com/nbragin4sscaffoldrom
- [Support this project](#support-this-project)

Got criticism or complaints?

- [File an issue](https://github.com/nbragin4sscaffoldromssues?q=is%3Aopen) so that Scaffoldrom can be improved.
  Be friendly and constructive about what could be better.
  Make detailed suggestions.
- **Keep us in the loop so that we can help.**
  For example, if you are discussing problems with Scaffoldrom on a mailing list, [file an issue](https://github.com/nbragin4sscaffoldromssues?q=is%3Aopen) where you link to the discussion thread and/or cc at least 1 core committer on the email.
- Be encouraging.
  A comment like "This function ought to be rewritten like this" is much more likely to result in action than a comment like "Eww, look how bad this function is."

Waiting for a response to an issue/question?

- Be patient and persistent. All issues are on the core committer team's radar and will be considered thoughtfully, but we have a lot of issues to work through.
  If urgent, it's fine to ping a core committer in the issue with a reminder.
- Ask others to comment, discuss, review, etc.
- Search the Scaffoldrom repo for issues related to yours.
- Need a fix/feature/release/help urgently, and can't wait?
  [@audreyfeldroy](https://github.com/audreyfeldroy) is available for hire for consultation or custom development.

## Support This Project

This project is run by volunteers.
Shortly we will be providing means for organizations and individuals to support the project.

## Code of Conduct

Everyone interacting in the Scaffoldrom project's codebases and documentation is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).
This includes but is not limited to, issue trackers, chat rooms, mailing lists, and other virtual or in real-life communication.

## Creator / Leader

This project was created and led by [Audrey Roy Greenfeld](https://github.com/audreyfeldroy).

She is supported by a team of maintainers.
