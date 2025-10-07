#!/bin/bash

if [ ! -d "venv" ]; then
  echo "Creating venv enviroment..."
  python3 -m venv venv
fi

echo "Installing Library..."
./venv/bin/pip install -r requirements.txt

echo "The script is now executable, e.g. venv/bin/python3 txt2img.py"
echo "Hey! Export HF_TOKEN to the environment variables."
