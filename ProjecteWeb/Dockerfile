FROM python:3.11.9

WORKDIR /app

# Instal·lar pip i poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copiem fitxers de dependències
COPY pyproject.toml poetry.lock requirements.txt ./

# Instal·lar dependències bàsiques amb pip per seguretat
RUN pip install -r requirements.txt

# Configurar Poetry per no crear virtualenv
RUN poetry config virtualenvs.create false

# Instal·lar només dependències de producció
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Copiem tot el projecte
COPY . .

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
