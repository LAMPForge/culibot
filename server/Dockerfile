FROM --platform=$BUILDPLATFORM docker.io/python:3.11.0-bullseye
LABEL org.opencontainers.image.source=https://github.com/LAMPForge/culi-chatbot
LABEL org.opencontainers.image.description="Culi Chatbot"
LABEL org.opencontainers.image.licenses=Apache-2.0

RUN pip install "poetry==1.4.2"

WORKDIR /app/server

ADD poetry.lock .
ADD pyproject.toml .

RUN poetry config virtualenvs.in-project true && \
    poetry install --without test,docs --no-root

ADD app app


ARG RELEASE_VERSION
ENV RELEASE_VERSION=${RELEASE_VERSION}

CMD ["poetry", "run", "uvicorn", "culi.main:app", "--host", "0.0.0.0", "--port", "10000"]