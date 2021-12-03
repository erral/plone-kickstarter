# kickstarting plone with make & pip

This cookiecutter template helps in

- building and running Plone using pip and a Makefile
- launching and debugging Plone from within VisualCode

## Prerequisites

- `cookiecutter` (temporary the current unreleased version from github, due to unreleased bugfixes).

  ```bash
  pip3 install git+https://github.com/cookiecutter/cookiecutter.git#egg=cookiecutter
  ```

- (optional) `plonecli` and `bobtemplates.plone` (>= 6.0b10)

  Best is to install the two tools into your standard Python 3 (not the venv inside the project).


## Usage

### create the project

First create your Plone project, let's call it "acme.foo" using *plonecli* and *bobtemplates.plone*:

```bash
    plonecli create addon acme.foo
```

Answer all questions and use Plone latest Plone 6 (6.0.0a1 at the time of writing).

Then add the magic to the newly created project by applying this cookiecutter template:

```bash
    cookiecutter -f https://github.com/bluedynamics/plone-kickstarter
```

You have to answer the project package with the same name as the addon name, so `acme.foo` in this case.

### build and run

Enter the created project

```bash
    cd acme.foo
```

Create a Python 3 *virtualenv* and activate it.

Use the Makefile

```bash
    $ make run
```

This installs, builds the instance and run Plone.

The Makefile has the targets

- install
- instance
- run
- test
- style (applies black, isort and zpretty)
- help

## VisualCode support

### Prerequisite

Install the official Microsoft Python plugin.

### Usage

- Start vscode with

    ```bash
    code .
    ```

- Select the python environment that you have used to build the project (your virtalenv).

- When you click on the debug icon you can see two run configurations in the dropdown box at the top:

  - Python: Plone
  - Python: Test Plone

With those you can run and test Plone, you can set breakpoints have access to the interactive debugger of VisualCode.

Have fun!

## Contributors

- Philipp Auersperg
- Jens Klein
