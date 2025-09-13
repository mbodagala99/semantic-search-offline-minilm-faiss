#!/bin/bash

# Healthcare Search Assistant Chat UI - Startup Script

echo "🚀 Starting Healthcare Search Assistant Chat UI..."
echo ""

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "❌ Virtual environment not found. Please run from project root:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source ../venv/bin/activate

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing FastAPI dependencies..."
    pip install fastapi uvicorn python-multipart jinja2 aiofiles
fi

# Start the server
echo "🌟 Starting FastAPI server..."
echo ""
echo "📱 Frontend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo "🔧 ReDoc: http://localhost:8000/api/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=" * 60

python start_server.py
