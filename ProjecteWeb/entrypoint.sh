#!/bin/bash

# Apply database migrations
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Start Django server in the background
poetry run python manage.py runserver 0.0.0.0:8000 &

# Run your custom data fetching script
poetry run python -c "from scripts.fetch_data import main; main()"

# Wait for the background server process to finish
wait
