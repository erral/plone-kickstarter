FROM plone/plone-backend:{{ cookiecutter.plone_version }}

LABEL maintainer="Your contact <your@contact.email>" \
      org.label-schema.name="{{ cookiecutter.project_name }}" \
      org.label-schema.description="{{ cookiecutter.project_name }} CMS Plone Site" \
      org.label-schema.vendor="Your Name or Organization" \
      org.label-schema.docker.cmd="docker run -d -p 8080:8080 yourdockerhubnamespace/plone-{{ cookiecutter.project_name }}:latest"

# if used in GitLabCI we need this build arg
# ARG CI_JOB_TOKEN

# Add local code
COPY . ./
RUN apt-get update \
    && apt-get -y upgrade -y \
    && apt-get -y install make \
#    && echo "token=${CI_TOKEN}" \
#    && git config --global url."https://gitlab-ci-token:${CI_JOB_TOKEN}@git.akbild.ac.at".insteadOf ssh://git@git.akbild.ac.at \
    && make VENV=off VENV_FOLDER=. install
