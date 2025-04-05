import os
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

# Define common paths
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"
EXAMPLES_DIR = PROJECT_ROOT / "examples"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(exist_ok=True)

def get_project_root() -> Path:
    """Return the absolute path to the project root directory."""
    return PROJECT_ROOT

def get_config_path(filename: str) -> Path:
    """Get the path to a configuration file."""
    return CONFIG_DIR / filename

def get_output_path(filename: str) -> Path:
    """Get the path to an output file, creating directories if needed."""
    return OUTPUT_DIR / filename

def get_example_path(filename: str) -> Path:
    """Get the path to an example file."""
    return EXAMPLES_DIR / filename

def get_doc_path(filename: str) -> Path:
    """Get the path to a documentation file."""
    return DOCS_DIR / filename 