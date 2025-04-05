import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_test_data_path(filename: str) -> Path:
    """Get the path to a test data file."""
    return Path(__file__).parent / "test_data" / filename

def create_test_data_dir():
    """Create the test data directory if it doesn't exist."""
    test_data_dir = Path(__file__).parent / "test_data"
    test_data_dir.mkdir(exist_ok=True)
    return test_data_dir

@pytest.fixture
def sample_text():
    """Fixture providing a sample text for testing."""
    return "This is a sample text for testing purposes."

@pytest.fixture
def setup_env(monkeypatch):
    """Fixture to set up mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "test-api-key"))
    monkeypatch.setenv("MODEL_NAME", os.getenv("MODEL_NAME", "gpt-4o"))
    monkeypatch.setenv("PROJECT_ROOT", str(Path(__file__).parent.parent))
    return None

def test_env_variables(setup_env):
    """Test that environment variables are set correctly."""
    assert os.environ["OPENAI_API_KEY"] == os.getenv("OPENAI_API_KEY", "test-api-key")
    assert os.environ["MODEL_NAME"] == os.getenv("MODEL_NAME", "gpt-4o")
    assert os.environ["PROJECT_ROOT"] == str(Path(__file__).parent.parent) 