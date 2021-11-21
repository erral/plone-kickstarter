# kickstarting plone with make & pip

This cookiecutter template helps in

- building and running Plone using pip and a Makefile
- launching and debugging Plone from within VisualCode

## Prerequisites

- cookiecutter

    $ pip3 install cookiecutter

- (optional) plonecli and bobtemplates.plone (>= 6.0b10)

Best is to install the two tools into your standard python3 (not the venv inside the project)

## Usage

### create the project

first create your Plone project, lets call it "acme.foo" using plonecli and bobtemplates.plone

    $ plonecli create addon acme.foo

answer all questions and use Plone 6.0.0a1 

Then add the magic to the newly created project by applying this cookiecutter template:

    $ cookiecutter -f https://github.com/bluedynamics/plone-kickstarter

You have to answer the project package with the same name as the addon name, so `acme.foo` in this case.

### build and run

Enter the created project

    $ cd acme.foo

create a virtual env and activate it

Use the Makefile 

    $ make run

This should install, build instance and run

The Makefile has the targets

- install
- instance
- run
- test
- style (applies black and isort)

## VisualCode support

### Prerequisite

install the official Microsoft Python plugin

### Usage

- start vscode with

    $ code .

- select the python environment that you have used to build the project

- When you click on the debug icon you can see two run configurations in the dropdown box at the top:

    - Python: Plone
    - Python: Test Plone

With those you can run and test Plone, you can set breakpoints have access to the interactive debugger of VisualCode, have fun

## Contributors

- Jens Klein
- Philipp Auersperg