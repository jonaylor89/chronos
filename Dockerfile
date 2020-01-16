FROM python:3.7

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "src.chronos.chronos:app"]
