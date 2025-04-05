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
    PROJECT_ROOT,
    CONFIG_DIR,
    OUTPUT_DIR,
    EXAMPLES_DIR,
    DOCS_DIR
)

def test_project_root_constant():
    """Test that PROJECT_ROOT is set correctly."""
    assert isinstance(PROJECT_ROOT, Path)
    assert PROJECT_ROOT.is_absolute()

def test_directory_constants():
    """Test that directory constants are set correctly."""
    assert CONFIG_DIR == PROJECT_ROOT / "config"
    assert OUTPUT_DIR == PROJECT_ROOT / "output"
    assert EXAMPLES_DIR == PROJECT_ROOT / "examples"
    assert DOCS_DIR == PROJECT_ROOT / "docs"

def test_get_project_root():
    """Test getting project root."""
    assert get_project_root() == PROJECT_ROOT

def test_get_config_path():
    """Test getting config path."""
    filename = "test_config.json"
    expected_path = CONFIG_DIR / filename
    assert get_config_path(filename) == expected_path

def test_get_output_path():
    """Test getting output path."""
    filename = "test_output.txt"
    expected_path = OUTPUT_DIR / filename
    assert get_output_path(filename) == expected_path

def test_get_example_path():
    """Test getting example path."""
    filename = "test_example.py"
    expected_path = EXAMPLES_DIR / filename
    assert get_example_path(filename) == expected_path

def test_get_doc_path():
    """Test getting doc path."""
    filename = "test_doc.md"
    expected_path = DOCS_DIR / filename
    assert get_doc_path(filename) == expected_path

def test_path_with_subdirectories():
    """Test getting paths with subdirectories."""
    # Test with a path that includes subdirectories
    subpath = "subdir/file.txt"
    assert get_output_path(subpath) == OUTPUT_DIR / subpath
    assert get_config_path(subpath) == CONFIG_DIR / subpath
    assert get_example_path(subpath) == EXAMPLES_DIR / subpath
    assert get_doc_path(subpath) == DOCS_DIR / subpath 