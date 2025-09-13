#!/bin/bash
# Healthcare Search System - Stop Script
# Simple script to stop the application

echo "🛑 Healthcare Search System - Stopping..."
echo "========================================"

# Check if application is running
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "ℹ️  Application is not running on port 8000"
    exit 0
fi

echo "🔄 Stopping application..."

# Try graceful stop first
echo "📡 Attempting graceful stop..."
pkill -f "python start.py" 2>/dev/null

# Wait a moment
sleep 2

# Check if still running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "⚠️  Graceful stop failed, forcing stop..."
    pkill -f uvicorn 2>/dev/null
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

# Final check
sleep 1
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "❌ Failed to stop application. Try manually:"
    echo "   lsof -i:8000"
    echo "   kill -9 <PID>"
    exit 1
else
    echo "✅ Application stopped successfully"
fi

