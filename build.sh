#!/bin/bash

# Build the project
set -o errexit  # exit on error
echo "Building the project JDA..."




pip install -r requirements.txt

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Ensure default superuser exists
python3 manage.py shell <<'PY'
from django.contrib.auth import get_user_model
User = get_user_model()
username = "aroniabackoffice"
password = "aroniabackoffice"
email = "admin@aroniatravel.com"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f"Created superuser {username}")
else:
    print(f"Superuser {username} already exists")

