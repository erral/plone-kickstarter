# Kickstarting Plone with MMPCR

MMPCR stand for the *M*ake, *M*xdev, *P*ip, *C*ookiecutter, *R*unswsgi process.
Let's bake a MMCP setup for Plone.

This cookiecutter template helps in

- building Plone or an add-on for Plone using pip, mxdev and a Makefile
- running Plone (with add-on)
- developing an addon with above tools
- launching and debugging Plone from within VisualCode

## Prerequisites

- `cookiecutter` (temporary the current unreleased version from github, due to unreleased bugfixes we depend on).

  ```bash
  pip install git+https://github.com/cookiecutter/cookiecutter.git#egg=cookiecutter
  ```

- (optional, for mode *addon*) `plonecli` and `bobtemplates.plone` (>= 6.0b10) if you want to crate a plone customization or addon.

  Best is to install the two tools into your standard Python 3 (not the venv inside the project).

## Usage

```bash
    cookiecutter -f https://github.com/bluedynamics/plone-kickstarter
```

It supports two mode: ``standalone`` and ``addon``.

**standalone** creates a setup for a minimal vanilla Plone site.
The setup can then be enhanced for your needs.

**addon** is meant to add a the setup to a prior created plonecli code.

### Create a vanilla Plone site

- Run cookiecutter with option `mode` set to ``standalone``.
- Enter generated direcory.
- Create a Pythn 3.9 virtualenv and activate it.
- Run ``make run``

### Create a Plone addon

First create your Plone project, let's call it "acme.foo" using *plonecli* and *bobtemplates.plone*:

```bash
    plonecli create addon acme.foo
```

Answer all questions and use Plone latest Plone 6 (6.0.0a2 at the time of writing).

Then add the magic to the newly created project by applying this cookiecutter template:

```bash
    cookiecutter -f https://github.com/bluedynamics/plone-kickstarter
```

You have to answer the project package with the same name as the addon name, so `acme.foo` in this case.

Run cookiecutter with option `mode` set to ``addon``.

For details on the usage of the Makefile read the generated file `README_USAGE.md`.

Enter the created project

```bash
    cd acme.foo
```

Create a Python 3 *virtualenv* and activate it.

Use the Makefile

```bash
    make run
```

For details on the usage of the Makefile read the generated file `README_USAGE.md`.

## Visual Studio Code support

### Prerequisite

Install the official Microsoft Python plugin.

### Usage in VSCode

- Start VSCode in your projetc folder with

  ```bash
  code .
  ```

- Select the python environment that you have used to build the project (your virtalenv).

- When you click on the debug icon you can see up to two run configurations in the dropdown box at the top:

  - `Python: Plone ($PROJECTNAME)`
  - `Python: Test Plone  ($PROJECTNAME)` (only in mode addon)

With those you can run and test Plone, you can set breakpoints have access to the interactive debugger of VisualCode.

Have fun!

## Contributors

- Philipp Auersperg @zworkb
- Jens Klein @jensens
