# 🏥 Healthcare Search System - Setup Instructions

## 🚀 Quick Start

### Prerequisites
- Python 3.13.3 or higher
- Virtual environment activated
- GEMINI_API_KEY set (optional but recommended)

### 1. Initial Setup (First Time Only)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set API key (optional but recommended)
export GEMINI_API_KEY="your_api_key_here"
```

### 2. Start Application
```bash
# Method 1: Using startup script (Recommended)
./start.sh

# Method 2: Direct Python command
source venv/bin/activate
python start.py
```

### 3. Stop Application
```bash
# Method 1: Using stop script (Recommended)
./stop.sh

# Method 2: If running in foreground
Ctrl+C

# Method 3: Force stop if stuck
pkill -f "python start.py"
lsof -ti:8000 | xargs kill -9
```

## 🌐 Access the Application

Once started, open your browser to:
- **🌐 Chat UI**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/api/docs
- **💚 Health Check**: http://localhost:8000/api/health
- **🔍 Search API**: http://localhost:8000/api/search
- **📊 Available Indexes**: http://localhost:8000/api/indices

## 🔧 Application Control

### Starting the Application
| Method | Command | Description |
|--------|---------|-------------|
| **Startup Script** | `./start.sh` | ✅ **Recommended** - Handles everything |
| **Direct Python** | `python start.py` | Manual start after activating venv |
| **Development** | `uvicorn chat_ui.backend.app:app --reload` | Auto-reload for development |

### Stopping the Application
| Method | Command | Description |
|--------|---------|-------------|
| **Stop Script** | `./stop.sh` | ✅ **Recommended** - Graceful + force stop |
| **Graceful** | `Ctrl+C` | If running in foreground |
| **Force Stop** | `pkill -f "python start.py"` | If stuck or background |

### Checking Status
| Command | Description |
|---------|-------------|
| `curl http://localhost:8000/api/health` | Check if application is running |
| `lsof -i:8000` | See what's using port 8000 |
| `ps aux \| grep python` | Check Python processes |

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i:8000

# Kill the process
kill -9 <PID>
```

#### Application Won't Start
```bash
# Check virtual environment
source venv/bin/activate

# Check dependencies
pip list | grep -E "(fastapi|uvicorn|sentence-transformers)"

# Check API key
echo $GEMINI_API_KEY
```

#### Application Won't Stop
```bash
# Force kill all related processes
pkill -f uvicorn
pkill -f "python start.py"
lsof -ti:8000 | xargs kill -9
```

### Health Check
```bash
# Test if application is working
curl http://localhost:8000/api/health

# Expected response: {"status": "healthy", ...}
```

## 📁 Project Structure

```
semantic-search-offline-minilm-faiss/
├── start.sh              # 🚀 Startup script
├── stop.sh               # 🛑 Stop script
├── start.py              # Main Python startup
├── chat_ui/              # Chat interface
├── api/                  # API endpoints
├── core/                 # Core functionality
├── configurations/       # Configuration files
└── docs/                 # Documentation
```

## 🎯 Features

- ✅ **Unified Application** - Everything in one place
- ✅ **Simple Scripts** - Easy start/stop commands
- ✅ **Chat Interface** - Interactive healthcare queries
- ✅ **Production APIs** - All search functionality
- ✅ **Health Monitoring** - System status and diagnostics
- ✅ **Query Routing** - Automatic healthcare classification
- ✅ **Semantic Search** - FAISS-based vector search

## 📋 Quick Reference

### Essential Commands
```bash
# Start
./start.sh

# Stop
./stop.sh

# Check status
curl http://localhost:8000/api/health

# Access
open http://localhost:8000
```

### Development Commands
```bash
# Start with auto-reload
uvicorn chat_ui.backend.app:app --reload --host 0.0.0.0 --port 8000

# Check logs
tail -f app.log
```

---

**This is the single source of truth for all setup, startup, and termination instructions.** 🎉

