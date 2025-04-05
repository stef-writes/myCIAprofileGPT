# CIABot Chat Interface Setup Guide

This guide provides step-by-step instructions for setting up CIABot with a chat interface. Follow these instructions carefully to ensure a smooth setup process with no errors.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Git**
   ```bash
   git --version
   ```

3. **Docker and Docker Compose** (for containerized deployment)
   ```bash
   docker --version
   docker-compose --version
   ```

4. **OpenAI API Key**
   - Sign up for an OpenAI account at https://platform.openai.com/
   - Create an API key in the OpenAI dashboard
   - Save the API key securely

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ciabot.git
cd ciabot
```

## Step 2: Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Step 3: Install Dependencies

Create a `requirements.txt` file with the following content:

```
fastapi==0.100.0
uvicorn==0.22.0
pydantic==2.0.0
python-dotenv==0.19.0
openai==1.0.0
sqlalchemy==2.0.0
alembic==1.11.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.0.1
redis==4.5.0
celery==5.3.0
gunicorn==21.2.0
prometheus-client==0.17.0
sentry-sdk==1.25.0
httpx==0.24.0
pytest==7.3.1
pytest-asyncio==0.21.0
black==23.3.0
isort==5.12.0
mypy==1.3.0
flake8==6.0.0
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Step 4: Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ciabot

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
```

Replace `your_openai_api_key` with your actual OpenAI API key and `your_jwt_secret_key` with a secure random string.

## Step 5: Set Up Database

### Option 1: Local PostgreSQL

1. Install PostgreSQL if not already installed
2. Create a database and user:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE ciabot;
CREATE USER ciabot_user WITH PASSWORD 'ciabot_password';
GRANT ALL PRIVILEGES ON DATABASE ciabot TO ciabot_user;
```

### Option 2: Docker PostgreSQL

```bash
docker run --name ciabot-postgres -e POSTGRES_USER=ciabot_user -e POSTGRES_PASSWORD=ciabot_password -e POSTGRES_DB=ciabot -p 5432:5432 -d postgres:13
```

## Step 6: Set Up Redis

### Option 1: Local Redis

1. Install Redis if not already installed
2. Start Redis server:

```bash
redis-server
```

### Option 2: Docker Redis

```bash
docker run --name ciabot-redis -p 6379:6379 -d redis:6
```

## Step 7: Create Configuration Files

### Create `src/config.py`:

```python
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL")
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application
    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Rate Limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_period: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Create `src/api/chat_api.py`:

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
from ciabot.core.text_processor import TextProcessor
from ciabot.core.ciaprofile import (
    generate_profile_prompt,
    analyze_text_with_reasoning,
    generate_structured_profile,
    generate_detailed_report,
    generate_intelligence_report,
    calculate_metrics,
    generate_security_profile
)
from src.config import settings

app = FastAPI()

class ChatRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
    tone: str = "balanced"

class ChatResponse(BaseModel):
    session_id: str
    analysis_id: str
    prompt: str
    reasoning: str
    profile: Dict[str, Any]
    detailed_report: str
    intelligence_report: str
    metrics: Dict[str, Any]
    security_profile: Dict[str, Any]

@app.post("/analyze", response_model=ChatResponse)
async def analyze_text(request: ChatRequest):
    # Generate a unique ID for this analysis
    analysis_id = str(uuid.uuid4())
    
    # Process the text input
    text_input = TextProcessor.from_chat_input(
        content=request.text,
        session_id=request.session_id
    )
    
    # Generate profile prompt
    prompt = generate_profile_prompt(text_input.content, request.tone)
    
    # Analyze text with reasoning
    reasoning = analyze_text_with_reasoning(text_input.content, prompt)
    
    # Generate structured profile
    profile = generate_structured_profile(text_input.content, request.tone)
    if not profile:
        raise HTTPException(status_code=500, detail="Failed to generate profile")
    
    # Convert profile to dictionary for JSON response
    profile_dict = profile.model_dump()
    
    # Generate detailed report
    detailed_report = generate_detailed_report(profile, request.tone)
    
    # Generate intelligence report
    intel_report = generate_intelligence_report(text_input.content)
    
    # Calculate metrics
    metrics = calculate_metrics(text_input.content)
    metrics_dict = metrics.model_dump() if metrics else {}
    
    # Generate security profile
    security_profile = generate_security_profile(text_input.content)
    security_dict = security_profile.model_dump() if security_profile else {}
    
    # Return the response
    return ChatResponse(
        session_id=text_input.metadata.get("session_id", ""),
        analysis_id=analysis_id,
        prompt=prompt,
        reasoning=reasoning,
        profile=profile_dict,
        detailed_report=detailed_report,
        intelligence_report=intel_report,
        metrics=metrics_dict,
        security_profile=security_dict
    )
```

### Create `src/api/session_manager.py`:

```python
from typing import Dict, List, Optional
import datetime

class AnalysisSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.datetime.now()
        self.analyses: List[Dict] = []
        self.context: Dict = {}
    
    def add_analysis(self, analysis: Dict):
        self.analyses.append(analysis)
    
    def update_context(self, context: Dict):
        self.context.update(context)
    
    def get_history(self) -> List[Dict]:
        return self.analyses

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, AnalysisSession] = {}
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> AnalysisSession:
        if not session_id:
            session_id = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if session_id not in self.sessions:
            self.sessions[session_id] = AnalysisSession(session_id)
        
        return self.sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[AnalysisSession]:
        return self.sessions.get(session_id)
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        now = datetime.datetime.now()
        to_remove = []
        
        for session_id, session in self.sessions.items():
            age = now - session.created_at
            if age.total_seconds() > max_age_hours * 3600:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            del self.sessions[session_id]
```

### Create `src/main.py`:

```python
import uvicorn
from api.chat_api import app
from api.session_manager import SessionManager

# Initialize the session manager
session_manager = SessionManager()

# Make the session manager available to the API
app.state.session_manager = session_manager

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Step 8: Update TextProcessor

Add the following method to `src/ciabot/core/text_processor.py`:

```python
@classmethod
def from_chat_input(cls, content: str, session_id: str = None, format: str = "chat") -> TextInput:
    """Create a TextInput from direct chat input."""
    # Generate a session ID if not provided
    if not session_id:
        session_id = f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Process the text
    return cls.process_text(
        content=content,
        source="chat",
        metadata={
            "session_id": session_id,
            "input_type": "chat",
            "timestamp": datetime.datetime.now().isoformat()
        },
        format=format
    )
```

## Step 9: Run the Application

### Option 1: Direct Run

```bash
# Make sure you're in the project root directory
python -m src.main
```

### Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create a `docker-compose.yml`:

```yaml
version: '3'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://ciabot_user:ciabot_password@db:5432/ciabot
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=ciabot_user
      - POSTGRES_PASSWORD=ciabot_password
      - POSTGRES_DB=ciabot
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Run with Docker Compose:

```bash
docker-compose up -d
```

## Step 10: Test the API

Use curl or a tool like Postman to test the API:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message.", "tone": "balanced"}'
```

## Step 11: Troubleshooting

If you encounter any issues:

1. **Database Connection Issues**
   - Check that PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure the database and user exist

2. **Redis Connection Issues**
   - Check that Redis is running
   - Verify Redis URL in `.env`

3. **OpenAI API Issues**
   - Verify your API key is correct
   - Check your OpenAI account status
   - Ensure you have sufficient credits

4. **Application Errors**
   - Check the application logs
   - Verify all dependencies are installed
   - Ensure all configuration files are in place

## Step 12: Next Steps

Once the basic setup is working, consider:

1. **Adding Authentication**
   - Implement user registration and login
   - Add JWT token validation
   - Set up role-based access control

2. **Implementing Rate Limiting**
   - Add Redis-based rate limiting
   - Configure limits based on user roles

3. **Setting Up Monitoring**
   - Add Prometheus metrics
   - Configure Sentry for error tracking
   - Set up logging aggregation

4. **Creating a Frontend**
   - Design a user-friendly chat interface
   - Implement real-time updates
   - Add visualization for analysis results

## Conclusion

You now have a fully functional CIABot with a chat interface. The setup includes all necessary components for a production-ready application, including database persistence, session management, and API endpoints. Follow the troubleshooting steps if you encounter any issues, and consider the next steps to enhance the application further. 