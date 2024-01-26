#!/bin/bash

# Build the project
set -o errexit  # exit on error
echo "Building the project Aronia..."




pip install -r requirements.txt

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
