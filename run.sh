#!/bin/bash

echo "Starting DiaTrack Health Server..."

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the app
echo "Launching Flask app..."
python app.py
