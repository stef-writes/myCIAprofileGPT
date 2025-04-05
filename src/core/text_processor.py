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
        content: Union[str, bytes],
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
        # Convert bytes to string if necessary
        if isinstance(content, bytes):
            content = content.decode('utf-8')
            
        # Clean and normalize text
        content = content.strip()
        
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
    
    @staticmethod
    def from_file(file_path: str, format: str = "plain") -> TextInput:
        """
        Process text from a file.
        
        Args:
            file_path: Path to the text file
            format: Format of the text
            
        Returns:
            TextInput object with processed text and metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        metadata = {
            "file_path": file_path,
            "file_size": os.path.getsize(file_path)
        }
        
        return TextProcessor.process_text(
            content=content,
            source="file",
            metadata=metadata,
            format=format
        )
    
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
    
    def process(self) -> str:
        """Process the text and return the normalized version."""
        # Add any text processing logic here
        return self.text.strip()
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get the metadata associated with the text."""
        return self.metadata 