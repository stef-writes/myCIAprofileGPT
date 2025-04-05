"""
Text Processor Module

This module handles text input processing and validation for the CIA Profile Generator.
It provides a clean interface for processing text from various sources (files, API, etc.)
and preparing it for analysis.
"""

from typing import Optional, Union, Dict, Any
from pydantic import BaseModel, Field
import json
import os
import datetime
from pathlib import Path
from src.utils.paths import get_project_root, get_output_path

class TextInput(BaseModel):
    """Model for text input with metadata."""
    content: str = Field(..., description="The actual text content to analyze")
    source: str = Field(..., description="Source of the text (e.g., 'file', 'api', 'direct')")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the text")
    format: str = Field(default="plain", description="Format of the text (e.g., 'plain', 'markdown', 'html')")

class TextProcessor:
    """Handles text input processing and validation."""
    
    @staticmethod
    def process_text(
        content: Union[str, bytes, memoryview],
        source: str = "direct",
        metadata: Optional[Dict[str, Any]] = None,
        format: str = "plain"
    ) -> TextInput:
        """
        Process and validate text input.
        
        Args:
            content: The text content to process
            source: Source of the text
            metadata: Additional metadata about the text
            format: Format of the text
            
        Returns:
            TextInput object with processed text and metadata
        """
        # Convert bytes or memoryview to string if necessary
        if isinstance(content, memoryview):
            content = content.tobytes().decode('utf-8')
        elif isinstance(content, bytes):
            content = content.decode('utf-8')
            
        # Clean and normalize text
        content = str(content).strip()
        
        # Create metadata if not provided
        if metadata is None:
            metadata = {}
            
        # Add basic metadata
        metadata.update({
            "length": len(content),
            "processed_timestamp": datetime.datetime.now().isoformat()
        })
        
        return TextInput(
            content=content,
            source=source,
            metadata=metadata,
            format=format
        )
    
    @classmethod
    def from_text(cls, content: str, source: str = "web", format: str = "plain") -> "TextProcessor":
        """Create a TextProcessor instance from text content."""
        return cls(text=content, source=source, format=format)
    
    @classmethod
    def from_file(cls, file_path: str, source: str = "file", format: str = "plain") -> "TextProcessor":
        """Create a TextProcessor instance from a file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return cls(text=content, source=source, format=format)
    
    @staticmethod
    def from_json(json_data: Union[str, Dict]) -> TextInput:
        """
        Process text from JSON data.
        
        Args:
            json_data: JSON string or dictionary containing text data
            
        Returns:
            TextInput object with processed text and metadata
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
            
        return TextProcessor.process_text(
            content=data.get("content", ""),
            source=data.get("source", "api"),
            metadata=data.get("metadata", {}),
            format=data.get("format", "plain")
        )

    def __init__(self, text: str, source: str = "web", format: str = "plain"):
        self.text = text
        self.source = source
        self.format = format
        self.metadata = {
            "source": source,
            "format": format,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def process(self) -> str:
        """Process the text and return the normalized version."""
        # Add any text processing logic here
        return str(self.text).strip()
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get the metadata associated with the text."""
        return self.metadata 

def read_text_file(file_path: str) -> str:
    """Read text from a file with proper path resolution."""
    # Convert string path to Path object
    path = Path(file_path)
    
    # If path is not absolute, assume it's relative to project root
    if not path.is_absolute():
        path = get_project_root() / path
    
    with open(path, 'r', encoding='utf-8') as f:
        return f.read() 