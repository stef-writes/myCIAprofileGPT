"""
Text API Module

This module provides API endpoints for text processing and analysis.
It serves as the interface between the frontend and the core analysis functionality.
"""

from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from pathlib import Path
from src.core.text_processor import TextProcessor
from src.core.ciaprofile import (
    generate_profile_prompt,
    analyze_text_with_reasoning,
    generate_structured_profile,
    generate_detailed_report,
    generate_intelligence_report,
    calculate_metrics,
    generate_security_profile
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CIA Profile Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TextRequest(BaseModel):
    """Model for text analysis requests."""
    content: str
    source: str = "web"
    format: str = "plain"

class AnalysisResponse(BaseModel):
    """Model for analysis responses."""
    structured_profile: Dict[str, Any]
    reasoning: str
    detailed_report: str
    intelligence_report: str
    metrics: Dict[str, Any]
    security_profile: Dict[str, Any]

def safe_model_dump(obj: Any, default_value: Any = None) -> Any:
    """Safely convert a Pydantic model to a dict or return the object as is."""
    try:
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()
        return obj
    except Exception as e:
        logger.error(f"Error in safe_model_dump: {str(e)}")
        return default_value

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest) -> AnalysisResponse:
    """
    Analyze text and generate a comprehensive profile.
    
    Args:
        request: TextRequest containing the text to analyze
        
    Returns:
        AnalysisResponse containing all analysis results
    """
    try:
        # Process the text
        processor = TextProcessor.from_text(
            content=request.content,
            source=request.source,
            format=request.format
        )
        
        # Generate profile prompt
        try:
            prompt = generate_profile_prompt(processor.text)
            logger.info("Generated profile prompt successfully")
        except Exception as e:
            logger.error(f"Error generating profile prompt: {str(e)}")
            prompt = "Error generating prompt"
        
        # Analyze text with reasoning
        try:
            reasoning = analyze_text_with_reasoning(processor.text, prompt)
            reasoning = safe_model_dump(reasoning, "Error in reasoning analysis")
            if not isinstance(reasoning, str):
                reasoning = str(reasoning)
            logger.info("Completed reasoning analysis")
        except Exception as e:
            logger.error(f"Error in reasoning analysis: {str(e)}")
            reasoning = f"Error in reasoning analysis: {str(e)}"
        
        # Generate structured profile
        try:
            profile = generate_structured_profile(processor.text)
            structured_profile = safe_model_dump(profile, {"error": "Failed to generate structured profile"})
            logger.info("Generated structured profile")
        except Exception as e:
            logger.error(f"Error generating structured profile: {str(e)}")
            structured_profile = {"error": f"Failed to generate structured profile: {str(e)}"}
        
        # Generate detailed report
        try:
            detailed = generate_detailed_report(processor.text)
            detailed = safe_model_dump(detailed, "Error generating detailed report")
            if not isinstance(detailed, str):
                detailed = str(detailed)
            logger.info("Generated detailed report")
        except Exception as e:
            logger.error(f"Error generating detailed report: {str(e)}")
            detailed = f"Error generating detailed report: {str(e)}"
        
        # Generate intelligence report
        try:
            intelligence = generate_intelligence_report(processor.text)
            intelligence = safe_model_dump(intelligence, "Error generating intelligence report")
            if not isinstance(intelligence, str):
                intelligence = str(intelligence)
            logger.info("Generated intelligence report")
        except Exception as e:
            logger.error(f"Error generating intelligence report: {str(e)}")
            intelligence = f"Error generating intelligence report: {str(e)}"
        
        # Calculate metrics
        try:
            metrics = calculate_metrics(processor.text)
            metrics_dict = safe_model_dump(metrics, {"error": "Failed to calculate metrics"})
            logger.info("Calculated metrics")
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            metrics_dict = {"error": f"Failed to calculate metrics: {str(e)}"}
        
        # Generate security profile
        try:
            security = generate_security_profile(processor.text)
            security_profile = safe_model_dump(security, {"error": "Failed to generate security profile"})
            logger.info("Generated security profile")
        except Exception as e:
            logger.error(f"Error generating security profile: {str(e)}")
            security_profile = {"error": f"Failed to generate security profile: {str(e)}"}
        
        response = AnalysisResponse(
            structured_profile=structured_profile,
            reasoning=reasoning,
            detailed_report=detailed,
            intelligence_report=intelligence,
            metrics=metrics_dict,
            security_profile=security_profile
        )
        logger.info("Successfully created analysis response")
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze_text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

# Mount static files after API routes
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static") 