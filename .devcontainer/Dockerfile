ARG PYTHON_VERSION=3.11
FROM mcr.microsoft.com/vscode/devcontainers/python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED 1
ENV FORWARDED_ALLOW_IPS *

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y install --no-install-recommends postgresql-client
