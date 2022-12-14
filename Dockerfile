FROM python:3.10.8-alpine3.16 as python

RUN apk add gcc g++ make linux-headers

# Poetry configuration
ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools wheel \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy app files
COPY . /app
WORKDIR /app

# Install dependencies
RUN poetry install

ENTRYPOINT [ "poetry", "run", "python", "almond/bot.py" ]