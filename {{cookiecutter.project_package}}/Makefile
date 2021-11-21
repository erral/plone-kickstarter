### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`


# Specifcs of this Makefile
PIP_VERSION=21.3
PIP_PARAMS=--src devsrc --use-deprecated legacy-resolver

# install and run
.PHONY: all
all: install instance run

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: .installed.txt ## pip install all dependencies and scripts

.installed.txt: requirements_barebone.txt constraints.txt sources.ini setup.cfg
	@pip install -U "pip==${PIP_VERSION}" wheel
	@mxdev -c sources.ini
	@pip install -r requirements-dev.txt ${PIP_PARAMS}
	@pip freeze >.installed.txt


.PHONY: instance
instance: instance/etc/zope.ini  ## create configuration for an zope (plone) instance

instance/etc/zope.ini: install
	@mkwsgiinstance -d instance -u admin:admin
	@cp skel/zope.ini instance/etc/
	@mkdir -p instance/etc/package-includes
	@cp skel/project-configure.zcml instance/etc/package-includes/{{cookiecutter.project_package}}-configure.zcml

test: install
	@zope-testrunner --test-path=src

run: instance  ## run Plone
	@runwsgi -v instance/etc/zope.ini

.PHONY: clean
clean: install  ## remove instance configuration (keep data)
	@rm -fr instance/etc instance/inituser
	@pip uninstall -y -r requirements-dev.txt
	@rm .installed.txt

.PHONY: style
style: install  ## format code (black, isort, zpretty)
	@isort src
	@black src
	@find src -name "*.zcml"|xargs zpretty -iz
	@find src -name "*.xml"|grep -v locales|xargs zpretty -ix
