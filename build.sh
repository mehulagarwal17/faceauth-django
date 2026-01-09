#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --settings=flogin.production_settings

# Run migrations
python manage.py migrate --settings=flogin.production_settings
