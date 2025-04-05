import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from src.ciabot.core.text_processor import (
    TextInput,
    TextProcessor,
    read_text_file
)
import json
import datetime
from unittest.mock import MagicMock

# Tests for TextInput model
def test_text_input_validation():
    """Test TextInput model validation."""
    # Valid input
    text_input = TextInput(
        content="Test content",
        source="test",
        metadata={"key": "value"},
        format="plain"
    )
    assert text_input.content == "Test content"
    assert text_input.source == "test"
    assert text_input.metadata == {"key": "value"}
    assert text_input.format == "plain"
    
    # Test default values
    text_input = TextInput(content="Test", source="test")
    assert text_input.metadata == {}
    assert text_input.format == "plain"
    
    # Test invalid input
    with pytest.raises(ValueError):
        TextInput(source="test")  # Missing required content

# Tests for TextProcessor static methods
def test_process_text_static():
    """Test the static process_text method."""
    # Test string input
    result = TextProcessor.process_text("Test content")
    assert isinstance(result, TextInput)
    assert result.content == "Test content"
    assert result.source == "direct"
    assert "length" in result.metadata
    assert "processed_timestamp" in result.metadata
    
    # Test bytes input
    result = TextProcessor.process_text(b"Test content")
    assert result.content == "Test content"
    
    # Test memoryview input
    result = TextProcessor.process_text(memoryview(b"Test content"))
    assert result.content == "Test content"
    
    # Test with metadata
    metadata = {"custom": "value"}
    result = TextProcessor.process_text("Test", metadata=metadata)
    assert result.metadata["custom"] == "value"
    assert "length" in result.metadata
    assert "processed_timestamp" in result.metadata

def test_from_json():
    """Test the static from_json method."""
    # Test with JSON string
    json_str = '{"content": "Test", "source": "api", "metadata": {"key": "value"}}'
    result = TextProcessor.from_json(json_str)
    assert isinstance(result, TextInput)
    assert result.content == "Test"
    assert result.source == "api"
    assert result.metadata["key"] == "value"
    
    # Test with dictionary
    json_dict = {
        "content": "Test",
        "source": "api",
        "metadata": {"key": "value"}
    }
    result = TextProcessor.from_json(json_dict)
    assert isinstance(result, TextInput)
    assert result.content == "Test"
    assert result.source == "api"
    assert result.metadata["key"] == "value"

# Tests for TextProcessor instance methods
def test_text_processor_initialization():
    """Test TextProcessor instance initialization."""
    processor = TextProcessor(text="Test text")
    assert processor.text == "Test text"
    assert processor.source == "web"
    assert processor.format == "plain"
    assert "timestamp" in processor.metadata

def test_process_instance():
    """Test the instance process method."""
    processor = TextProcessor("  Test content  ")
    result = processor.process()
    assert result == "Test content"

def test_get_metadata():
    """Test the instance get_metadata method."""
    processor = TextProcessor("Test", source="test", format="markdown")
    metadata = processor.get_metadata()
    assert metadata["source"] == "test"
    assert metadata["format"] == "markdown"
    assert "timestamp" in metadata

# Tests for TextProcessor class methods
def test_from_text_classmethod():
    """Test the from_text class method."""
    processor = TextProcessor.from_text("Test content", source="web", format="markdown")
    assert processor.text == "Test content"
    assert processor.source == "web"
    assert processor.format == "markdown"
    assert "timestamp" in processor.metadata

def test_from_file_classmethod():
    """Test the from_file class method."""
    mock_content = "Test file content"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        processor = TextProcessor.from_file("test.txt")
        assert processor.text == mock_content
        assert processor.source == "file"
        assert processor.format == "plain"

# Tests for read_text_file function
@patch("src.ciabot.core.text_processor.get_project_root")
def test_read_text_file(mock_get_project_root):
    """Test reading text from file."""
    # Mock project root
    mock_get_project_root.return_value = Path("/project/root")
    
    # Test with absolute path
    mock_content = "Test file content"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = read_text_file("/absolute/path/test.txt")
        assert result == mock_content
    
    # Test with relative path
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = read_text_file("relative/path/test.txt")
        assert result == mock_content
        # Verify path was resolved relative to project root
        mock_get_project_root.assert_called()

# Tests for error handling
def test_error_handling():
    """Test error handling in text processing."""
    # Test invalid file path
    with pytest.raises(FileNotFoundError):
        TextProcessor.from_file("nonexistent.txt")
    
    # Test invalid JSON
    with pytest.raises(json.JSONDecodeError):
        TextProcessor.from_json("invalid json")
    
    # Test invalid file encoding
    mock_file = MagicMock()
    mock_file.read.side_effect = UnicodeDecodeError('utf-8', b"\x80invalid", 0, 1, "invalid start byte")
    mock_file.__enter__.return_value = mock_file
    
    with patch("builtins.open", return_value=mock_file):
        with pytest.raises(UnicodeDecodeError):
            TextProcessor.from_file("test.txt") 