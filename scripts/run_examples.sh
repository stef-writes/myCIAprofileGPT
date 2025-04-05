#!/bin/bash

# Ensure script fails on any error
set -e

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
}

# Function to activate virtual environment
activate_venv() {
    echo "Activating virtual environment..."
    source venv/bin/activate
}

# Function to install package in development mode
install_package() {
    echo "Installing package in development mode..."
    pip install -e .
}

# Function to run an example
run_example() {
    echo "Running example: $1"
    python "src/examples/$1"
}

# Main execution
check_venv
activate_venv
install_package

# Check if an example name was provided
if [ $# -eq 0 ]; then
    echo "Running default example (example_profile.py)..."
    run_example "example_profile.py"
else
    run_example "$1"
fi 