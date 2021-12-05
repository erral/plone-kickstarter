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

##############################################################################
# Specifcs of this Makefile
CONSTRAINTS=constraints.txt
{%- if cookiecutter.mode == "addon" %}
PIP_REQUIREMENTS_IN_FILE=requirements_barebone.txt
ADDONFOLDER=./src
{%- else %}
PIP_REQUIREMENTS_IN_FILE=requirements.txt
{%- endif %}
INSTANCE_FOLDER=instance

PIP_PARAMS= --pre --use-deprecated legacy-resolver
##############################################################################

# targets and prerequisites
# target has to be one file, otherwise step gets executes for each file separate
PREPARE_PREREQUISITES=${PIP_REQUIREMENTS_IN_FILE} ${CONSTRAINTS} sources.ini{%- if cookiecutter.mode == "addon" %} setup.cfg{%- endif %}
PREPARE_TARGET={{ cookiecutter.requirements_out }}
INSTALL_PREREQUSISTES=${PREPARE_TARGET}
INSTALL_TARGET=.installed.txt
INSTANCE_PREREQUISITES=${INSTALL_TARGET} instance.yaml
INSTANCE_TARGET=${INSTANCE_FOLDER}/etc/zope.ini ${INSTANCE_FOLDER}/etc/zope.conf ${INSTANCE_FOLDER}/etc/site.zcml
{%- if cookiecutter.mode == "addon" %}
TEST_PREREQUISITES=${INSTALL_TARGET}
{%- endif %}
RUN_PREREQUISITES=${INSTANCE_TARGET}


# install and run
.PHONY: all
all: {%- if cookiecutter.mode == "addon" %}test {%- endif %}run

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

SENTINELFOLDER=.make-sentinels/
SENTINEL=${SENTINELFOLDER}ABOUT.txt
${SENTINEL}:
	@mkdir -p ${SENTINELFOLDER}
	@echo "Sentinels for the Makefile process." > ${SENTINEL}

PIP_SENTINEL=${SENTINELFOLDER}pip.sentinel
${PIP_SENTINEL}: ${CONSTRAINTS} ${SENTINEL}
	@echo "$(OK_COLOR)Install pip according to ${CONSTRAINTS}$(NO_COLOR)"
	@pip install -c ${CONSTRAINTS} pip wheel
	@touch ${PIP_SENTINEL}

MXDEV_SENTINEL=${SENTINELFOLDER}mxdev.sentinel
${MXDEV_SENTINEL}: ${PIP_SENTINEL}
	@echo "$(OK_COLOR)Install mxdev$(NO_COLOR)"
	@pip install mxdev
	@touch ${MXDEV_SENTINEL}

.PHONY: prepare
prepare: ${PREPARE_TARGET} ## prepare soures and dependencies

${PREPARE_PREREQUISITES}:
	@touch $@

${PREPARE_TARGET}: ${MXDEV_SENTINEL} ${PREPARE_PREREQUISITES}
	@echo "$(OK_COLOR)Prepare sources and dependencies$(NO_COLOR)"
	@mxdev -c sources.ini

.PHONY: install
install: ${INSTALL_TARGET} ## pip install all dependencies and scripts

${INSTALL_TARGET}: ${PREPARE_TARGET}
	@echo "$(OK_COLOR)Install dependencies and scripts$(NO_COLOR)"
	@pip install -r ${PREPARE_TARGET} ${PIP_PARAMS}
	@pip freeze >${INSTALL_TARGET}

COOKIECUTTER_SENTINEL=${SENTINELFOLDER}cookiecutter.sentinel
${COOKIECUTTER_SENTINEL}:
	@echo "$(OK_COLOR)Install cookiecutter$(NO_COLOR)"
	@pip install git+https://github.com/cookiecutter/cookiecutter.git#egg=cookiecutter
	@touch ${COOKIECUTTER_SENTINEL}

instance.yaml:
	@touch instance.yaml

.PHONY: instance
instance: ${INSTANCE_TARGET} ## create configuration for an zope (plone) instance

${INSTANCE_TARGET}: ${INSTANCE_PREREQUISITES} ${COOKIECUTTER_SENTINEL}
	@echo "$(OK_COLOR)Create Plone/Zope configuration$(NO_COLOR)"
	@cookiecutter -f --no-input --config-file instance.yaml https://github.com/bluedynamics/cookiecutter-zope-instance

{%- if cookiecutter.mode == "addon" %}

TESTRUNNER_SENTINEL=${SENTINELFOLDER}testrunner.sentinel
${TESTRUNNER_SENTINEL}: ${PIP_SENTINEL}
	@echo "$(OK_COLOR)Install zope.testrunner$(NO_COLOR)"
	@pip install zope.testrunner
	@touch ${TESTRUNNER_SENTINEL}

.PHONY: test
test: ${TEST_PREREQUISITES} ${TESTRUNNER_SENTINEL} ## run tests
	@echo "$(OK_COLOR)Run addon tests$(NO_COLOR)"
	@zope-testrunner --auto-color --auto-progress --test-path=${ADDONFOLDER}

.PHONY: test-ignore-warnings
test-ignore-warnings: ${TEST_PREREQUISITES} ${TESTRUNNER_SENTINEL}  ## run tests (hide warnins)
	@echo "$(OK_COLOR)Run addon tests$(NO_COLOR)"
	@PYTHONWARNINGS=ignore zope-testrunner --auto-color --auto-progress --test-path=${ADDONFOLDER}

BLACK_SENTINEL=${SENTINELFOLDER}black.sentinel
${BLACK_SENTINEL}: ${PIP_SENTINEL}
	@echo "$(OK_COLOR)Install black$(NO_COLOR)"
	@pip install black
	@touch ${BLACK_SENTINEL}

ISORT_SENTINEL=${SENTINELFOLDER}isort.sentinel
${ISORT_SENTINEL}: ${PIP_SENTINEL}
	@echo "$(OK_COLOR)Install isort$(NO_COLOR)"
	@pip install isort
	@touch ${ISORT_SENTINEL}

ZPRETTY_SENTINEL=${SENTINELFOLDER}zpretty.sentinel
${ZPRETTY_SENTINEL}: ${PIP_SENTINEL}
	@echo "$(OK_COLOR)Install zpretty$(NO_COLOR)"
	@pip install zpretty
	@touch ${ZPRETTY_SENTINEL}

.PHONY: apply-style-black
apply-style-black: ${BLACK_SENTINEL}  ## apply/format code style black (to Python files)
	@echo "$(OK_COLOR)Apply style black rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@black ${ADDONFOLDER}

.PHONY: apply-style-isort
apply-style-isort: ${ISORT_SENTINEL} ## apply/format code style isort (sorted imports in Python files)
	@echo "$(OK_COLOR)Apply style isort rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@isort ${ADDONFOLDER}

.PHONY: apply-style-zpretty
apply-style-zpretty: ${ZPRETTY_SENTINEL}   ## apply/format code style zpretty (to XML/ZCML files)
	@echo "$(OK_COLOR)Apply style zpretty rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@find ${ADDONFOLDER} -name "*.zcml"|xargs zpretty -iz
	@find ${ADDONFOLDER} -name "*.xml"|grep -v locales|xargs zpretty -ix

.PHONY: style ## apply code styles black, isort and zpretty
style: apply-style-black apply-style-isort apply-style-zpretty

.PHONY: format ## alias for "style"
style: style

.PHONY: lint-black
lint-black: ${BLACK_SENTINEL}  ## lint code-style black (to Python files)
	@echo "$(OK_COLOR)Lint black rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@black --check ${ADDONFOLDER}

.PHONY: lint-isort
lint-isort: ${ISORT_SENTINEL} ## lint code-style isort (sorted imports in Python files)
	@echo "$(OK_COLOR)Apply style isort rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@isort --check-only ${ADDONFOLDER}

.PHONY: lint-zpretty
lint-zpretty: ${ZPRETTY_SENTINEL}   ## lint code-style zpretty (to XML/ZCML files)
	@echo "$(OK_COLOR)Apply style zpretty rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@find ${ADDONFOLDER} -name "*.zcml"|xargs zpretty --check -z
	@find ${ADDONFOLDER} -name "*.xml"|grep -v locales|xargs zpretty --check -x

.PHONY: lint ## lint all: check if complies with code-styles black, isort and zpretty
liny: lint-black lint-isort lint-zpretty
{%- endif %}

.PHONY: run
run: ${RUN_PREREQUISITES} ## run/start Plone
	@echo "$(OK_COLOR)Run Plone$(NO_COLOR)"
	@runwsgi -v instance/etc/zope.ini

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	@echo "$(OK_COLOR)Remove Python file artifacts (like byte-code) of code in current directory.$(NO_COLOR)"
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-make
clean-make:  ## remove make artifact	@echo "$(OK_COLOR)Remove Plone/Zope configuration (keeps data) and sentinel files.$(NO_COLOR)"
	rm -rf ${INSTALL_PREREQUSISTES} ${INSTANCE_TARGET} ${SENTINELFOLDER}

.PHONY: clean-instance
clean-instance:  ## remove instance configuration (keeps data)
	@echo "$(OK_COLOR)Remove Plone/Zope configuration (keeps data) and sentinel files.$(NO_COLOR)"
	rm -f ${INSTANCE_TARGET}

.PHONY: clean
clean:  clean-pyc clean-make clean-instance  ## clean all (except local database and pip installed packages)
