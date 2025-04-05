import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(autouse=True)
def setup_test_env():
    """Automatically set up test environment variables before each test."""
    # Set test environment variables
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "test-api-key")
    os.environ["MODEL_NAME"] = os.getenv("MODEL_NAME", "gpt-4o")
    os.environ["PROJECT_ROOT"] = str(Path(__file__).parent.parent)
    
    # Mock OpenAI client
    with patch("openai.OpenAI") as mock:
        mock_instance = MagicMock()
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )
        mock.return_value = mock_instance
        yield mock
    
    # Clean up after tests
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    if "MODEL_NAME" in os.environ:
        del os.environ["MODEL_NAME"]
    if "PROJECT_ROOT" in os.environ:
        del os.environ["PROJECT_ROOT"]

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for testing."""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a test response",
                    "role": "assistant"
                }
            }
        ]
    }

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch("openai.OpenAI") as mock:
        mock_instance = MagicMock()
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )
        mock.return_value = mock_instance
        yield mock_instance 