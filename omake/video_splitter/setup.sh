#!/bin/bash

if [ ! -d "venv" ]; then
  echo "Creating venv enviroment..."
  python3 -m venv venv
fi

echo "Installing Library..."
./venv/bin/pip install -r requirements.txt

echo "The script is now executable, e.g. venv/bin/python3 run.py mnt/g/AI/source_images/_vid/output/i2v_????"
