#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to create and activate virtual environment
setup_venv() {
    echo "Setting up virtual environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$PROJECT_ROOT/venv" ]; then
        python3 -m venv "$PROJECT_ROOT/venv"
        echo "Created new virtual environment"
    fi
    
    # Activate virtual environment
    source "$PROJECT_ROOT/venv/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    pip install -r "$PROJECT_ROOT/config/requirements.txt"
    
    echo "Virtual environment is ready!"
}

# Function to run tests
run_tests() {
    source "$PROJECT_ROOT/venv/bin/activate"
    pytest "$@"
}

# Main script logic
case "$1" in
    "setup")
        setup_venv
        ;;
    "test")
        shift  # Remove 'test' from arguments
        run_tests "$@"
        ;;
    "activate")
        source "$PROJECT_ROOT/venv/bin/activate"
        echo "Virtual environment activated. Use 'deactivate' to exit."
        ;;
    *)
        echo "Usage:"
        echo "  $0 setup    - Create and setup virtual environment"
        echo "  $0 test     - Run tests (with optional pytest arguments)"
        echo "  $0 activate - Activate virtual environment"
        ;;
esac 