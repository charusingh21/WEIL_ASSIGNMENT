#!/bin/bash

# Activate virtual environment (if applicable)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask application
python app.py
