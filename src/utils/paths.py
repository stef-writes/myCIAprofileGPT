import os
import sys
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory.
    
    Tries multiple methods in order:
    1. Environment variable PROJECT_ROOT
    2. Looking for setup.py in parent directories
    3. Fallback to src parent directory
    """
    # Try to get from environment variable first
    project_root = os.environ.get("PROJECT_ROOT")
    if project_root:
        return Path(project_root)
    
    # Otherwise, try to find it by looking for setup.py
    current_dir = Path(__file__).resolve().parent
    while current_dir.parent != current_dir:
        if (current_dir / "setup.py").exists():
            return current_dir
        current_dir = current_dir.parent
    
    # If all else fails, return the src parent directory
    return Path(__file__).resolve().parent.parent

# Get the project root directory
PROJECT_ROOT = get_project_root()

# Define common paths
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"
EXAMPLES_DIR = PROJECT_ROOT / "examples"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(exist_ok=True)

def get_config_path(filename: str = None) -> Path:
    """Get the path to a configuration file or directory.
    
    Args:
        filename: Optional filename to append to the config path.
                 If None, returns the config directory path.
    """
    if filename is None:
        return CONFIG_DIR
    return CONFIG_DIR / filename

def get_output_path(filename: str = None) -> Path:
    """Get the path to an output file or directory.
    
    Args:
        filename: Optional filename to append to the output path.
                 If None, returns the output directory path.
    """
    if filename is None:
        return OUTPUT_DIR
    return OUTPUT_DIR / filename

def get_example_path(filename: str = None) -> Path:
    """Get the path to an example file or directory.
    
    Args:
        filename: Optional filename to append to the examples path.
                 If None, returns the examples directory path.
    """
    if filename is None:
        return EXAMPLES_DIR
    return EXAMPLES_DIR / filename

def get_doc_path(filename: str = None) -> Path:
    """Get the path to a documentation file or directory.
    
    Args:
        filename: Optional filename to append to the docs path.
                 If None, returns the docs directory path.
    """
    if filename is None:
        return DOCS_DIR
    return DOCS_DIR / filename

def get_script_path(filename: str = None) -> Path:
    """Get the path to a script file or directory.
    
    Args:
        filename: Optional filename to append to the scripts path.
                 If None, returns the scripts directory path.
    """
    if filename is None:
        return SCRIPTS_DIR
    return SCRIPTS_DIR / filename

def get_src_path(filename: str = None) -> Path:
    """Get the path to a source file or directory.
    
    Args:
        filename: Optional filename to append to the src path.
                 If None, returns the src directory path.
    """
    if filename is None:
        return SRC_DIR
    return SRC_DIR / filename 