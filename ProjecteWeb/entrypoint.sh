#!/bin/bash

# Inicia el servidor de Django en segundo plano
poetry run python manage.py runserver 0.0.0.0:8000 &

# Ejecuta fetch_data.main()
poetry run python -c "from scripts.fetch_data import main; main()"

# Espera a que termine el servidor de Django
wait
