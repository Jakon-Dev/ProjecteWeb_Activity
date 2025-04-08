FROM python:3.11.9

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]

# docker build -t webpage .
# docker run -p 8000:8000 webpage