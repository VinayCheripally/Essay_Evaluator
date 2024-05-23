#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

# Upgrade pip, then install specific versions of setuptools and wheel
pip install --upgrade pip
pip install setuptools==57.5.0 wheel==0.36.2

# Install the dependencies from requirements.txt
pip install --upgrade -r /vercel/path0/requirements.txt

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
