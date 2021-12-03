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
PACKAGENAME={{ cookiecutter.project_package }}
INSTANCE_FOLDER=instance

PIP_VERSION=21.3.1
PIP_PARAMS= --pre --use-deprecated legacy-resolver

# targets and prerequisites
# target has to be one file, otherwise step gets executes for each file separate
PREPARE_PREREQUISITES=requirements.txt constraints.txt setup.cfg sources.ini
PREPARE_TARGET=requirements-dev.txt
INSTALL_PREREQUSISTES=${PREPARE_TARGET}
INSTALL_TARGET=.installed.txt
INSTANCE_PREREQUISITES=${INSTALL_TARGET} instance.yaml
INSTANCE_TARGET=${INSTANCE_FOLDER}/etc/zope.ini ${INSTANCE_FOLDER}/etc/zope.conf ${INSTANCE_FOLDER}/etc/site.zcml
TEST_PREREQUISITES=${INSTALL_TARGET}
RUN_PREREQUISITES=${INSTANCE_TARGET}

# for clean, what to remove
CLEAN_FILES=${INSTALL_PREREQUSISTES} .installed.txt .has_cookiecutter ${INSTANCE_TARGET}

# install and run
.PHONY: all
all: prepare install instance test run

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: prepare
prepare: ${PREPARE_TARGET} ## prepare soures and dependencies

${PREPARE_TARGET}: ${PREPARE_PREREQUISITES}
	@pip install -U "pip==${PIP_VERSION}" wheel mxdev
	@mxdev -c sources.ini

.PHONY: install
install: ${INSTALL_TARGET} ## pip install all dependencies and scripts

${INSTALL_TARGET}: ${PREPARE_TARGET}
	@pip install -r ${PREPARE_TARGET} ${PIP_PARAMS}
	# @head -2 skel/settings.json >.vscode/settings.json
	# @python -c "import sys; [print(f'        \"{p}\",') for p in sys.path if p]" >>.vscode/settings.json
	# @tail -2 skel/settings.json >>.vscode/settings.json
	@pip freeze >${INSTALL_TARGET}

.has_cookiecutter:
	@pip install git+https://github.com/cookiecutter/cookiecutter.git#egg=cookiecutter
	@touch .has_cookiecutter

instance.yaml:
	@touch instance.yaml

.PHONY: instance
instance: ${INSTANCE_TARGET} ## create configuration for an zope (plone) instance

${INSTANCE_TARGET}: ${INSTANCE_PREREQUISITES} .has_cookiecutter
	@cookiecutter -f --no-input --config-file instance.yaml devsrc/cookiecutter-zope-instance

.PHONY: test
test: ${TEST_PREREQUISITES}  ## run tests
	@zope-testrunner --test-path=src

.PHONY: run
run: ${RUN_PREREQUISITES} ## run Plone
	@runwsgi -v instance/etc/zope.ini

.PHONY: clean
clean:  ## remove instance configuration (keep data)
	@rm ${CLEAN_FILES}

.PHONY: style
style:  ## format code (black, isort, zpretty)
	@isort src
	@black src
	@find src -name "*.zcml"|xargs zpretty -iz
	@find src -name "*.xml"|grep -v locales|xargs zpretty -ix
