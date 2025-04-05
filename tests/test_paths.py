import os
import pytest
from pathlib import Path
from unittest.mock import patch, PropertyMock, MagicMock

from src.utils.paths import (
    get_project_root,
    get_config_path,
    get_output_path,
    get_example_path,
    get_doc_path,
    get_script_path,
    get_src_path,
    PROJECT_ROOT,
    CONFIG_DIR,
    OUTPUT_DIR,
    EXAMPLES_DIR,
    DOCS_DIR,
    SCRIPTS_DIR,
    SRC_DIR
)

def test_project_root_constant():
    """Test that PROJECT_ROOT is set correctly."""
    assert isinstance(PROJECT_ROOT, Path)
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()

def test_directory_constants():
    """Test that all directory constants are set correctly."""
    assert isinstance(CONFIG_DIR, Path)
    assert isinstance(OUTPUT_DIR, Path)
    assert isinstance(EXAMPLES_DIR, Path)
    assert isinstance(DOCS_DIR, Path)
    assert isinstance(SCRIPTS_DIR, Path)
    assert isinstance(SRC_DIR, Path)
    
    # All directories should be under PROJECT_ROOT
    assert CONFIG_DIR.parent == PROJECT_ROOT
    assert OUTPUT_DIR.parent == PROJECT_ROOT
    assert EXAMPLES_DIR.parent == PROJECT_ROOT
    assert DOCS_DIR.parent == PROJECT_ROOT
    assert SCRIPTS_DIR.parent == PROJECT_ROOT
    assert SRC_DIR.parent == PROJECT_ROOT

@patch.dict(os.environ, {"PROJECT_ROOT": "/test/project/root"})
def test_get_project_root_from_env():
    """Test getting project root from environment variable."""
    # Clear the module-level PROJECT_ROOT to force recalculation
    import src.utils.paths
    src.utils.paths.PROJECT_ROOT = None
    
    assert str(get_project_root()) == "/test/project/root"

def test_get_project_root_from_setup_py(tmp_path):
    """Test getting project root by finding setup.py."""
    # Create a temporary directory structure
    project_root = tmp_path / "project"
    project_root.mkdir()
    (project_root / "setup.py").touch()
    
    # Clear the module-level PROJECT_ROOT to force recalculation
    import src.utils.paths
    src.utils.paths.PROJECT_ROOT = None
    
    with patch.dict(os.environ, {}, clear=True):  # Clear environment variables
        with patch("src.utils.paths.__file__", str(project_root / "src" / "utils" / "paths.py")):
            assert get_project_root() == project_root

def test_get_project_root_fallback(tmp_path):
    """Test getting project root fallback when setup.py not found."""
    # Create a temporary directory structure without setup.py
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    
    # Clear the module-level PROJECT_ROOT to force recalculation
    import src.utils.paths
    src.utils.paths.PROJECT_ROOT = None
    
    with patch.dict(os.environ, {}, clear=True):  # Clear environment variables
        with patch("src.utils.paths.__file__", str(src_dir / "utils" / "paths.py")):
            assert get_project_root() == src_dir

def test_get_config_path():
    """Test getting config path with and without filename."""
    # Test getting directory
    assert get_config_path() == CONFIG_DIR
    
    # Test getting file path
    filename = "test_config.json"
    assert get_config_path(filename) == CONFIG_DIR / filename

def test_get_output_path():
    """Test getting output path with and without filename."""
    # Test getting directory
    assert get_output_path() == OUTPUT_DIR
    
    # Test getting file path
    filename = "test_output.txt"
    assert get_output_path(filename) == OUTPUT_DIR / filename

def test_get_example_path():
    """Test getting example path with and without filename."""
    # Test getting directory
    assert get_example_path() == EXAMPLES_DIR
    
    # Test getting file path
    filename = "test_example.py"
    assert get_example_path(filename) == EXAMPLES_DIR / filename

def test_get_doc_path():
    """Test getting doc path with and without filename."""
    # Test getting directory
    assert get_doc_path() == DOCS_DIR
    
    # Test getting file path
    filename = "test_doc.md"
    assert get_doc_path(filename) == DOCS_DIR / filename

def test_get_script_path():
    """Test getting script path with and without filename."""
    # Test getting directory
    assert get_script_path() == SCRIPTS_DIR
    
    # Test getting file path
    filename = "test_script.sh"
    assert get_script_path(filename) == SCRIPTS_DIR / filename

def test_get_src_path():
    """Test getting src path with and without filename."""
    # Test getting directory
    assert get_src_path() == SRC_DIR
    
    # Test getting file path
    filename = "test_source.py"
    assert get_src_path(filename) == SRC_DIR / filename 