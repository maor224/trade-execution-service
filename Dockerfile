FROM python:3.13.2-slim

WORKDIR /home/service

RUN pip install poetry

COPY pyproject.toml poetry.lock /home/service/

RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi

RUN rm -rf poetry.lock pyproject.toml
COPY ./app /home/service/app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
