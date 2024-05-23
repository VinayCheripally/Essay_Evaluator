#!/bin/bash
# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install the dependencies from requirements.txt
pip install --upgrade -r /vercel/path0/requirements.txt
