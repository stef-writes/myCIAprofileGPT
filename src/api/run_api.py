#!/usr/bin/env python3
"""
Script to run the CIA Profile Generator API server.
"""

import uvicorn
from src.api.text_api import app

if __name__ == "__main__":
    uvicorn.run(
        "src.api.text_api:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        reload_dirs=["src"]
    ) 