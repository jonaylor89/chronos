FROM python:3.7

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD gunicorn --bind :$PORT --workers 1 --threads 8 src.chronos.chronos:app
