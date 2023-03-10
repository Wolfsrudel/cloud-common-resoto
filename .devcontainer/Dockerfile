FROM mcr.microsoft.com/devcontainers/python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends vim

COPY resotocore/requirements*.txt /tmp/resoto-requirements/resotocore/
COPY resotoeventlog/requirements*.txt /tmp/resoto-requirements/resotoeventlog/
COPY resotolib/requirements*.txt /tmp/resoto-requirements/resotolib/
COPY resotometrics/requirements*.txt /tmp/resoto-requirements/resotometrics/
COPY resotoshell/requirements*.txt /tmp/resoto-requirements/resotoshell/
COPY resotoworker/requirements*.txt /tmp/resoto-requirements/resotoworker/

# Install infrequently changing requirements
RUN grep -r -h -v resoto /tmp/resoto-requirements/ >> /tmp/resoto-requirements.txt \ 
    && su vscode -c 'pip3 install --no-warn-script-location -U pip wheel poetry' \
    && su vscode -c 'pip3 --disable-pip-version-check --no-cache-dir install --no-warn-script-location -U -r /tmp/resoto-requirements.txt' \ 
    && rm -rf /tmp/resoto-requirements.txt /tmp/resoto-requirements