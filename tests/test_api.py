import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from openai import OpenAI
from src.api.text_api import app

client = TestClient(app)

@pytest.fixture
def mock_openai():
    """Mock OpenAI client for testing."""
    with patch("openai.OpenAI") as mock:
        mock_instance = MagicMock()
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )
        mock.return_value = mock_instance
        yield mock

def test_api_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_process_text_endpoint(mock_openai):
    """Test the text processing endpoint."""
    test_text = "This is a test text"
    response = client.post("/api/analyze", json={"content": test_text})
    assert response.status_code == 200
    assert "structured_profile" in response.json()

@pytest.mark.asyncio
async def test_process_text_endpoint_empty(mock_openai):
    """Test the text processing endpoint with empty text."""
    response = client.post("/api/analyze", json={"content": ""})
    assert response.status_code == 200
    assert "structured_profile" in response.json()

@pytest.mark.asyncio
async def test_process_text_endpoint_invalid():
    """Test the text processing endpoint with invalid input."""
    response = client.post("/api/analyze", json={"invalid": "data"})
    assert response.status_code == 422  # Validation error

def test_openai_integration(mock_openai):
    """Test OpenAI integration using the mocked client."""
    # Use the mocked client from the fixture
    client = mock_openai.return_value
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Write a one-sentence bedtime story about a unicorn."
            }
        ]
    )
    assert completion.choices[0].message.content is not None 