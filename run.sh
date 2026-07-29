#!/bin/bash
echo "============================================"
echo "  AI Personal Assistant - Starting..."
echo "============================================"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Launch the app
echo "Launching AI Assistant..."
python main.py
