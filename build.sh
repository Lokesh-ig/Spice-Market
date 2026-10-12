#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

pip install -r requirements.txt
python backend/manage.py makemigrations
python backend/manage.py migrate
python backend/manage.py seed_data
