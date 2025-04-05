#!/bin/bash

# Install the package in development mode
pip install -e .

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your OpenAI API key"
fi

# Create necessary directories if they don't exist
mkdir -p src/reports

echo "Installation complete!"
echo "To run the example: python -m src.examples.example_profile" 