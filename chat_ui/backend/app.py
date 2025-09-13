#!/usr/bin/env python3
"""
Healthcare Search Chat UI - FastAPI Backend
Provides API endpoints for the chat interface and serves the frontend
"""

import sys
import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Configure debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('debug.log')
    ]
)
logger = logging.getLogger(__name__)

# Add parent directory to path to import our modules
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

# Change to project root directory for relative imports
os.chdir(project_root)

try:
    from core.initialization import get_components, health_check
    from core.api_handlers import search_healthcare_data, get_health_status, get_available_indexes
except ImportError as e:
    print(f"Warning: Could not import production API modules: {e}")
    # Fallback to legacy imports for backward compatibility
    try:
        from opensearch_query_executor import QueryExecutorFactory
        from healthcare_query_processor import HealthcareQueryProcessor
        from dsl_query_generator import DSLQueryGenerator
        from embedding_generator import EmbeddingGenerator
        from config_reader import config
    except ImportError as e2:
        print(f"Warning: Could not import legacy modules: {e2}")
        QueryExecutorFactory = None
        HealthcareQueryProcessor = None
        DSLQueryGenerator = None
        EmbeddingGenerator = None
        config = None

# FastAPI App
app = FastAPI(
    title="Healthcare Search Assistant API",
    description="API for healthcare data search and chat interface",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent.parent)), name="static")

# Serve individual static files
@app.get("/styles/{filename}")
async def serve_css(filename: str):
    """Serve CSS files"""
    file_path = Path(__file__).parent.parent / "styles" / filename
    if file_path.exists():
        return FileResponse(file_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/scripts/{filename}")
async def serve_js(filename: str):
    """Serve JavaScript files"""
    file_path = Path(__file__).parent.parent / "scripts" / filename
    if file_path.exists():
        return FileResponse(file_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript file not found")

# Note: Using production APIs instead of direct component initialization

# Pydantic Models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query text", min_length=1, max_length=500)
    index_name: Optional[str] = Field(None, description="Specific index to search")
    max_results: int = Field(20, description="Maximum number of results", ge=1, le=100)

class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message", min_length=1, max_length=500)
    conversation_history: Optional[List[ChatMessage]] = Field(default_factory=list)

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    opensearch_status: str
    components: Dict[str, Any]

# Note: Using production APIs instead of component dependencies

# API Routes

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main chat UI"""
    return FileResponse(str(Path(__file__).parent.parent / "index.html"))

@app.get("/layout-test", response_class=HTMLResponse)
async def serve_layout_test():
    """Serve the layout test page"""
    return FileResponse(str(Path(__file__).parent.parent / "layout_test.html"))

@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint using production API"""
    
    try:
        # Use production health check
        health_result = await get_health_status()
        
        # Convert to legacy format for compatibility
        opensearch_status = "green" if health_result.status == "healthy" else "degraded"
        
        return HealthCheckResponse(
            status=health_result.status,
            timestamp=datetime.now(),
            version="1.0.0",
            opensearch_status=opensearch_status,
            components={
                "is_initialized": str(health_result.components.get("is_initialized", False)),
                "components": str(health_result.components.get("components", {})),
                "errors": str(health_result.components.get("errors", []))
            }
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.now(),
            version="1.0.0",
            opensearch_status="error",
            components={"error": str(e)}
        )

@app.post("/api/search")
async def search_healthcare(request: SearchRequest):
    """Search healthcare data using production API"""
    
    try:
        # Use production search API
        search_result = await search_healthcare_data(
            query=request.query,
            index_name=request.index_name,
            max_results=request.max_results,
            include_metadata=True
        )
        
        # Convert to legacy format for compatibility
        result = {
            "success": search_result.success,
            "index_name": search_result.index_used,
            "total_hits": search_result.total_hits,
            "documents": search_result.results,
            "query_executed": {
                "query": {"match": {"_all": request.query}},
                "size": request.max_results
            },
            "execution_time_ms": search_result.execution_time_ms,
            "metadata": {
                "query": request.query,
                "index_used": search_result.index_used,
                "routing_result": search_result.routing_info,
                "timestamp": search_result.timestamp
            }
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/chat")
async def chat_with_assistant(request: ChatRequest):
    """Chat endpoint that processes user messages using production APIs"""
    
    logger.debug(f"🔍 Chat request received: {request.message}")
    
    try:
        # Use production API for search
        logger.debug("🔍 Calling production search API...")
        search_result = await search_healthcare_data(
            query=request.message,
            max_results=10,
            include_metadata=True
        )
        logger.debug(f"📊 Search result: {search_result.success}, {search_result.total_hits} hits")
        
        # Generate a conversational response
        logger.debug("💬 Generating chat response...")
        response_message = generate_chat_response(request.message, search_result.dict())
        logger.debug(f"💬 Response message: {response_message}")
        
        result = {
            "response": response_message,
            "search_results": search_result.dict(),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.debug(f"✅ Chat response generated successfully")
        return result
        
    except Exception as e:
        logger.error(f"❌ Chat processing failed: {e}")
        
        # Return error response
        return {
            "response": f"I apologize, but I encountered an error while processing your request: {str(e)}",
            "search_results": {
                "success": False,
                "error": str(e),
                "results": [],
                "total_hits": 0
            },
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/indices")
async def list_indices():
    """List available OpenSearch indices using production API"""
    
    try:
        # Use production API to get indexes
        indexes_result = await get_available_indexes()
        
        # Convert to legacy format for compatibility
        indices = [
            "healthcare_claims_index",
            "healthcare_providers_index", 
            "healthcare_procedures_index",
            "healthcare_members_index"
        ]
        
        index_info = {}
        for index_name in indices:
            index_info[index_name] = {
                "available": indexes_result.get("success", False),
                "info": indexes_result.get("indexes", {})
            }
        
        return {"indices": index_info}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list indices: {str(e)}")

@app.get("/api/suggestions")
async def get_query_suggestions():
    """Get suggested queries for the quick query buttons"""
    
    return {
        "suggestions": [
            {
                "query": "Find all claims for patient John Smith",
                "category": "Claims",
                "icon": "file-text"
            },
            {
                "query": "Show me providers in New York with high ratings",
                "category": "Providers", 
                "icon": "user-check"
            },
            {
                "query": "List all procedures performed last month",
                "category": "Procedures",
                "icon": "activity"
            },
            {
                "query": "Find members with diabetes diagnosis",
                "category": "Members",
                "icon": "users"
            },
            {
                "query": "Show claims over $5000",
                "category": "Claims",
                "icon": "dollar-sign"
            },
            {
                "query": "Find recent claims from last week",
                "category": "Claims",
                "icon": "calendar"
            }
        ]
    }

# Utility Functions

def generate_chat_response(user_message: str, search_result: Dict[str, Any]) -> str:
    """Generate a conversational response based on search results"""
    
    if not search_result.get("success", False):
        return "I'm sorry, I couldn't find any results for your query. Please try rephrasing your question."
    
    total_hits = search_result.get("total_hits", 0)
    execution_time = search_result.get("execution_time_ms", 0)
    index_used = search_result.get("index_name", "unknown")
    
    if total_hits == 0:
        return "I searched through the healthcare data but didn't find any matching results. You might want to try different keywords or check the spelling."
    
    # Generate contextual response
    response_parts = []
    
    if total_hits == 1:
        response_parts.append(f"I found 1 result for your query about '{user_message}'.")
    else:
        response_parts.append(f"I found {total_hits} results for your query about '{user_message}'.")
    
    response_parts.append(f"The search took {execution_time}ms to complete.")
    
    if total_hits > 20:
        response_parts.append("Showing the first 20 results. You can ask me to show more specific results or refine your search.")
    
    # Add some context about the data type
    if "claims" in index_used.lower():
        response_parts.append("These are healthcare claims records with patient, provider, and billing information.")
    elif "providers" in index_used.lower():
        response_parts.append("These are healthcare provider records with contact and specialty information.")
    elif "procedures" in index_used.lower():
        response_parts.append("These are medical procedure records with codes and descriptions.")
    elif "members" in index_used.lower():
        response_parts.append("These are member/enrollee records with demographic and enrollment information.")
    
    return " ".join(response_parts)

# Error Handlers

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors"""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors"""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Startup and Shutdown Events

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    print("🚀 Starting Healthcare Search Assistant API...")
    print("📊 Initializing components...")
    
    # Initialize production components (not async)
    try:
        from core.initialization import get_components
        components = get_components()
        print(f"✅ Components initialized: {components.is_initialized}")
    except Exception as e:
        print(f"⚠️ Component initialization warning: {e}")
    
    print("✅ API ready! Visit http://localhost:8000 for the chat interface")
    print("📚 API documentation available at http://localhost:8000/api/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down Healthcare Search Assistant API...")

# Main execution
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
