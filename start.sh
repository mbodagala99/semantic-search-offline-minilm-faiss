#!/bin/bash
# Healthcare Search System - Startup Script
# Simple script to start the application

echo "🏥 Healthcare Search System"
echo "=========================="
echo "🚀 Starting application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if API key is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  WARNING: GEMINI_API_KEY not set. Some features may not work."
    echo "   Set it with: export GEMINI_API_KEY='your_api_key_here'"
fi

# Start the application
echo "🚀 Starting server on http://localhost:8000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python start.py
