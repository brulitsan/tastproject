FROM python:3.10 as builder

WORKDIR /app

RUN pip install poetry==1.7.1

COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml

# Only application
FROM builder as slim

COPY . /app/
WORKDIR /app/testproject

RUN poetry install --all-extras

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

CMD ["poetry", "run", "python", "manage.py", "runserver"]
