#!/usr/bin/env python3
"""
Startup script for Healthcare Search Assistant Chat UI
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from backend.app import app

if __name__ == "__main__":
    print("🚀 Starting Healthcare Search Assistant Chat UI...")
    print("📱 Frontend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/api/docs")
    print("🔧 ReDoc: http://localhost:8000/api/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
