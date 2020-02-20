#!/bin/bash
echo "Create python environment using virtual env..."

pip install virtualenv
virtualenv env
source venv/bin/activate
pip install -r requirements.txt

echo "env folder created"
