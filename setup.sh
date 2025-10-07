#!/bin/bash

if [ ! -d "venv" ]; then
  echo "Creating venv enviroment..."
  python3 -m venv venv
fi

echo "Installing Library..."
./venv/bin/pip install -r requirements.txt
