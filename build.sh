#!/bin/bash
# Exit immediately if a command exits with a non-zero status
# set -e

# Upgrade pip, then install specific versions of setuptools and wheel
pip install --upgrade pip
pip install setuptools==57.5.0 wheel==0.36.2

# Install the dependencies from requirements.txt
#!/bin/bash
# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear
