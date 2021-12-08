FROM plone/plone-backend:{{ cookiecutter.plone_version }}

LABEL maintainer="Your contact <your@contact.email>" \
      org.label-schema.name="{{ cookiecutter.project_name }}" \
      org.label-schema.description="{{ cookiecutter.project_name }} CMS Plone Site" \
      org.label-schema.vendor="Your Name or Organization" \
      org.label-schema.docker.cmd="docker run -d -p 8080:8080 yourdockerhubnamespace/plone-{{ cookiecutter.project_name }}:latest"

# Add local {{ cookiecutter.project_name }} code
COPY . ./
RUN gosu make VENV=off VENV_FOLDER=. install
