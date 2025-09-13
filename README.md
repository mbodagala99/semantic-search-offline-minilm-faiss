# semantic-search-offline-minilm-faiss
Offline semantic search using FAISS and Sentence Transformers (all-MiniLM-L6-v2) for accurate, private, and efficient similarity search on small datasets—no external APIs or servers required.

## Required Software

- **Python**: 3.13.3 or higher

### Required Packages

- **sentence-transformers** (>=2.2.2): Hugging Face library for generating high-quality sentence embeddings using pre-trained transformer models. Used to convert text documents into vector representations for semantic similarity search.

- **faiss-cpu** (>=1.7.4): Facebook AI Similarity Search library for efficient similarity search and clustering of dense vectors. Provides fast indexing and retrieval capabilities for large-scale vector databases without requiring GPU acceleration.

- **google-generativeai** (>=0.3.0): Google's Generative AI library for integrating Gemini API for DSL query generation and natural language processing capabilities.

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd semantic-search-offline-minilm-faiss

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Key Configuration

The system uses Google Gemini API for LLM integration. You need to set up your API key:

#### Option A: Shell Profile (Recommended)
```bash
# Get your API key from: https://makersuite.google.com/app/apikey
# Add to your ~/.zshrc (or ~/.bashrc):
export GEMINI_API_KEY="your_actual_api_key_here"

# Reload your shell profile
source ~/.zshrc
```

#### Option B: Direct Environment Variable
```bash
# Set the API key directly in your current session
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 3. Verify Configuration

```bash
# Check if API key is set
echo $GEMINI_API_KEY

# Test the configuration
python -c "from config_reader import config; print('API Key Set:', config.is_api_key_set())"
```

## 🚀 Running the Application

### Quick Start
```bash
# Start the application
./start.sh

# Stop the application
./stop.sh
```

### Manual Commands
```bash
# Start manually
source venv/bin/activate
python start.py

# Stop manually
Ctrl+C  # or pkill -f "python start.py"
```

## 📚 Complete Setup Instructions

For detailed setup, startup, termination, and troubleshooting instructions, see:
**[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Complete setup documentation

## 🌐 Access the Application

Once started, you can access:
- **Chat UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/health
