#!/usr/bin/env python3
"""
Healthcare Search Chat UI - FastAPI Backend
Provides API endpoints for the chat interface and serves the frontend
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Add parent directory to path to import our modules
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

# Change to project root directory for relative imports
os.chdir(project_root)

try:
    from opensearch_query_executor import QueryExecutorFactory
    from healthcare_query_processor import HealthcareQueryProcessor
    from dsl_query_generator import DSLQueryGenerator
    from embedding_generator import EmbeddingGenerator
    from config_reader import config
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")
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

# Global instances
query_executor = None
query_processor = None
dsl_generator = None

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
    components: Dict[str, str]

# Dependency to get initialized components
async def get_components():
    """Initialize components if not already done"""
    global query_executor, query_processor, dsl_generator
    
    if query_executor is None:
        query_executor = QueryExecutorFactory.create_executor()
    
    if query_processor is None:
        try:
            query_processor = HealthcareQueryProcessor(EmbeddingGenerator())
        except Exception as e:
            print(f"Warning: Could not initialize query processor: {e}")
    
    if dsl_generator is None:
        try:
            dsl_generator = DSLQueryGenerator()
        except Exception as e:
            print(f"Warning: Could not initialize DSL generator: {e}")
    
    return {
        "executor": query_executor,
        "processor": query_processor,
        "dsl_generator": dsl_generator
    }

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
async def health_check(components: Dict[str, Any] = Depends(get_components)):
    """Health check endpoint"""
    
    # Check OpenSearch connection
    opensearch_status = "unknown"
    try:
        health_result = components["executor"].health_check()
        opensearch_status = health_result.get("status", "unknown")
    except Exception as e:
        opensearch_status = f"error: {str(e)}"
    
    # Check component status
    component_status = {}
    for name, component in components.items():
        if component is None:
            component_status[name] = "not_available"
        else:
            component_status[name] = "available"
    
    return HealthCheckResponse(
        status="healthy" if opensearch_status == "green" else "degraded",
        timestamp=datetime.now(),
        version="1.0.0",
        opensearch_status=opensearch_status,
        components=component_status
    )

@app.post("/api/search")
async def search_healthcare(
    request: SearchRequest,
    components: Dict[str, Any] = Depends(get_components)
):
    """Search healthcare data using OpenSearch"""
    
    try:
        # If no specific index provided, try to route the query
        index_name = request.index_name
        routing_result = None
        
        if not index_name and components["processor"]:
            try:
                routing_result = components["processor"].route_healthcare_query(request.query)
                if routing_result.get("success", False):
                    index_name = routing_result.get("routing_analysis", {}).get("index_name")
            except Exception as e:
                print(f"Routing failed: {e}")
        
        # Default to claims index if routing failed
        if not index_name:
            index_name = "healthcare_claims_index"
        
        # Generate DSL query if DSL generator is available
        dsl_query = {"query": {"match_all": {}}, "size": request.max_results}
        
        if components["dsl_generator"]:
            try:
                index_info = {"index_name": index_name}
                schema_info = {"fields": ["patient", "provider", "claim_id"]}
                
                dsl_result = components["dsl_generator"].generate_dsl_query(
                    request.query, index_info, schema_info
                )
                
                if dsl_result.get("success", False):
                    dsl_query = dsl_result.get("dsl_query", dsl_query)
            except Exception as e:
                print(f"DSL generation failed: {e}")
        
        # Execute the query
        result = components["executor"].execute_query(dsl_query, index_name)
        
        # Add metadata
        result["metadata"] = {
            "query": request.query,
            "index_used": index_name,
            "routing_result": routing_result,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/chat")
async def chat_with_assistant(
    request: ChatRequest,
    components: Dict[str, Any] = Depends(get_components)
):
    """Chat endpoint that processes user messages and returns responses"""
    
    try:
        # Process the user message through the search pipeline
        search_request = SearchRequest(query=request.message)
        search_result = await search_healthcare(search_request, components)
        
        # Generate a conversational response
        response_message = generate_chat_response(request.message, search_result)
        
        return {
            "response": response_message,
            "search_results": search_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "response": f"I'm sorry, I encountered an error processing your request: {str(e)}",
            "search_results": None,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/api/indices")
async def list_indices(components: Dict[str, Any] = Depends(get_components)):
    """List available OpenSearch indices"""
    
    try:
        indices = [
            "healthcare_claims_index",
            "healthcare_providers_index", 
            "healthcare_procedures_index",
            "healthcare_members_index"
        ]
        
        index_info = {}
        for index_name in indices:
            try:
                info = components["executor"].get_index_info(index_name)
                index_info[index_name] = {
                    "available": "error" not in info,
                    "info": info if "error" not in info else None
                }
            except Exception as e:
                index_info[index_name] = {
                    "available": False,
                    "error": str(e)
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
    
    # Initialize components
    await get_components()
    
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
