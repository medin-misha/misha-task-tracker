FROM python:3.12

RUN pip install poetry
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
RUN poetry install

COPY app app

WORKDIR app
RUN chmod +x run.sh

ENTRYPOINT [ "bash", "-c", "/app/run.sh" ]