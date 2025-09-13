#!/usr/bin/env python3
"""
Simple Consolidated Startup Script for Healthcare Search System
Starts both API and Chat UI in one application
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Change to project root directory
os.chdir(project_root)

import uvicorn
from chat_ui.backend.app import app

def main():
    """Main startup function"""
    print("🏥 Healthcare Search System")
    print("=" * 40)
    print("🚀 Starting consolidated application...")
    print("📱 Chat UI: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/api/docs")
    print("💚 Health Check: http://localhost:8000/api/health")
    print("=" * 40)
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start the consolidated server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
