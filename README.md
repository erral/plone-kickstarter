# Kickstarting Plone 6 (backend)

Bakes a configuration to start Plone 6 using *make*, *mxdev*, *pip*, *cookiecutter* and *WSGI*.

This cookiecutter templates result helps in

- building Plone or an add-on for Plone using pip, mxdev and a Makefile
- running Plone (with add-on)
- developing an addon with above tools
- launching and debugging Plone from within VisualCode

## Prerequisites

- `cookiecutter` (temporary the current unreleased version from github, due to unreleased bugfixes we depend on).

  ```bash
  pip install git+https://github.com/cookiecutter/cookiecutter.git#egg=cookiecutter
  ```

- (optional, for mode *addon*) `plonecli` (and `bobtemplates.plone` (>= 6.0b10) if you want to crate a plone customization or addon.

  Best is to install the two tools into your standard Python 3 (not the venv inside the project).

## Options

`project_name`
    Name of the project or addon.
    In mode *standalone* just the target folder name;
    in mode *addon* the dotted name of the package.

`mode`
    - `standalone` (default): generate a build system for a Plone site,
      but folder does not direcly contain a source package (like generated with *plonecli*).
    - `addon`: generate a integrated build for an addon.

`requirements-out`
    *mexdev* is used to help with development with sources on top f stable constraints.
    It generates a pip requirements file.
    Configure here how the file is named.
    Default: `requirements-mxdev.txt`.
`admin_user`
    *cookiecutter-zope-instance* is used to generate an instance configuration for the Plone/Zope application server.
    It creates an initial user with full access.
    This is the username.
    Default: `admin`.
`admin_user`
    *cookiecutter-zope-instance* is used to generate an instance configuration for the Plone/Zope application server.
    It creates an initial user with full access.
    This is the password.
    If empty a password is generated.
    Default: empty.
`plone_version`
    Plone Release to be used in the constraints file.
    Default: Should be most recent version, except short after a new release (PR's welcome).
`listen`
    *host:port* for the WSGI server to listen on.
    Usually "localhost:8080" for local development or "0.0.0.0:8080" if the port needs to be accessible from the outside.
    Default: `localhost:8080`

These options can be stored in a `plone-kickstarter.yaml`:

```YML
    default_context:
        project_name: 'admin'
        mode: 'addon'
        admin_user: 'admin
```

Pass additional parameters `--no-input --config-file plone-kickstarter.yaml`.
*cookicutter* takes the stored values or the defaults and does not ask further questions.

## Usage

```bash
    cookiecutter -f https://github.com/bluedynamics/plone-kickstarter
```

It supports two mode: ``standalone`` and ``addon``.

**standalone** creates a setup for a minimal vanilla Plone site.
The setup can then be enhanced for your needs.

**addon** is meant to add a the setup to a prior created plonecli code.

### Create a vanilla Plone site

- Ensure Python 3.9 is installed (including pip).
- Run cookiecutter with option `mode` set to ``standalone``.
- Enter generated direcory.
- Run ``make run``

### Create a Plone addon

#### TL/DR

```bash
pip install plonecli "bobtemplates.plone>=6.0b10" git+https://github.com/cookiecutter/cookiecutter.git#egg=cookiecutter
plonecli create addon acme.foo
# (set Plone verson to 6.0.0a2, otherwise answer questions with defaults)
cookiecutter -f https://github.com/bluedynamics/plone-kickstarter.git
# (select addon mode, otherwse defaults)
cd acme.foo
make run
```

#### Detailed

Install *plonecli*

```bash
pip install plonecli "bobtemplates.plone>=6.0b10"
```

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
