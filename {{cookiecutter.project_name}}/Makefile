# Makefile to configure and run Plone instance

## Defensive settings for make: https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
# for Makefile debugging purposes add -x to the .SHELLFLAGS
.SHELLFLAGS:=-eu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# Colors
OK_COLOR=`tput setaf 2`
# WARN_YELLOW=`tput setaf 3`
# ERROR_COLOR=`tput setaf 1`
NO_COLOR=`tput sgr0`


# Specifcs of this Makefile
INSTANCE_FOLDER=instance
{%- if cookiecutter.addon == "on" %}
PIP_REQUIREMENTS_IN_FILE=requirements_barebone.txt
{%- else %}
PIP_REQUIREMENTS_IN_FILE=requirements.txt
{%- endif %}

PIP_PARAMS= --pre --use-deprecated legacy-resolver

# targets and prerequisites
# target has to be one file, otherwise step gets executes for each file separate
PREPARE_PREREQUISITES=.make-pip.sentinel .make-mxdev.sentinel ${PIP_REQUIREMENTS_IN_FILE} constraints.txt sources.ini{%- if cookiecutter.addon == "on" %} setup.cfg{%- endif %}
PREPARE_TARGET=requirements-dev.txt
INSTALL_PREREQUSISTES=${PREPARE_TARGET}
INSTALL_TARGET=.installed.txt
INSTANCE_PREREQUISITES=${INSTALL_TARGET} instance.yaml
INSTANCE_TARGET=${INSTANCE_FOLDER}/etc/zope.ini ${INSTANCE_FOLDER}/etc/zope.conf ${INSTANCE_FOLDER}/etc/site.zcml
{%- if cookiecutter.addon == "on" %}
TEST_PREREQUISITES=${INSTALL_TARGET}
{%- endif %}
RUN_PREREQUISITES=${INSTANCE_TARGET}

# for clean, what to remove
CLEAN_FILES=${INSTALL_PREREQUSISTES} .installed.txt .make-*.sentinel ${INSTANCE_TARGET}

# install and run
.PHONY: all
all: {%- if cookiecutter.addon == "on" %}test {%- endif %}run

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.make-pip.sentinel: constraints.txt
	@echo "$(OK_COLOR)Install pip according to constraints.txt$(NO_COLOR)"
	@pip install -c constraints.txt pip wheel
	@touch .make-pip.sentinel

.make-mxdev.sentinel: .make-pip.sentinel
	@echo "$(OK_COLOR)Install mxdev$(NO_COLOR)"
	@pip install -c constraints.txt mxdev
	@touch .make-mxdev.sentinel

.PHONY: prepare
prepare: ${PREPARE_TARGET} ## prepare soures and dependencies

${PREPARE_TARGET}: ${PREPARE_PREREQUISITES}
	@echo "$(OK_COLOR)Prepare sources and dependencies$(NO_COLOR)"
	@mxdev -c sources.ini

.PHONY: install
install: ${INSTALL_TARGET} ## pip install all dependencies and scripts

${INSTALL_TARGET}: ${PREPARE_TARGET}
	@echo "$(OK_COLOR)Install dependencies and scripts$(NO_COLOR)"
	@pip install -r ${PREPARE_TARGET} ${PIP_PARAMS}
	# @head -2 skel/settings.json >.vscode/settings.json
	# @python -c "import sys; [print(f'        \"{p}\",') for p in sys.path if p]" >>.vscode/settings.json
	# @tail -2 skel/settings.json >>.vscode/settings.json
	@pip freeze >${INSTALL_TARGET}

.make-cookiecutter.sentinel:
	@echo "$(OK_COLOR)Install cookiecutter$(NO_COLOR)"
	@pip install git+https://github.com/cookiecutter/cookiecutter.git#egg=cookiecutter
	@touch .make-cookiecutter.sentinel

instance.yaml:
	@touch instance.yaml

.PHONY: instance
instance: ${INSTANCE_TARGET} ## create configuration for an zope (plone) instance

${INSTANCE_TARGET}: ${INSTANCE_PREREQUISITES} .make-cookiecutter.sentinel
	@echo "$(OK_COLOR)Create Plone/Zope configuration$(NO_COLOR)"
	@cookiecutter -f --no-input --config-file instance.yaml https://github.com/bluedynamics/cookiecutter-zope-instance

{%- if cookiecutter.addon == "on" %}
.PHONY: test
test: ${TEST_PREREQUISITES}  ## run tests
	@echo "$(OK_COLOR)Run addon tests$(NO_COLOR)"
	@zope-testrunner --test-path=src

{%- endif %}
.PHONY: run
run: ${RUN_PREREQUISITES} ## run Plone
	@echo "$(OK_COLOR)Run Plone$(NO_COLOR)"
	@runwsgi -v instance/etc/zope.ini

.PHONY: clean
clean:  ## remove instance configuration (keeps data)
	@echo "$(OK_COLOR)Remove Plone/Zope configuration (keeps data) and sentinel files.$(NO_COLOR)"
	rm ${CLEAN_FILES}

{%- if cookiecutter.addon == "on" %}
.PHONY: style
style:  ## format code (black, isort, zpretty)
	@echo "$(OK_COLOR)Apply style guide rules to code in ./src/*$(NO_COLOR)"
	@isort src
	@black src
	@find src -name "*.zcml"|xargs zpretty -iz
	@find src -name "*.xml"|grep -v locales|xargs zpretty -ix
{%- endif %}
