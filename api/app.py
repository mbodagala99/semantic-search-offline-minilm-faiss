#!/usr/bin/env python3
"""
Production-Ready Healthcare Search API
FastAPI application with clean, modular architecture
"""

import sys
import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.initialization import initialize_components, get_components, health_check
from core.api_handlers import (
    SearchRequest, SearchResponse, HealthResponse,
    get_search_service, search_healthcare_data, get_health_status, get_available_indexes
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('healthcare_search_api.log')
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Healthcare Search API...")
    try:
        # Initialize all components
        components = initialize_components()
        logger.info("✓ All components initialized successfully")
        
        # Store components in app state for access in routes
        app.state.components = components
        
        # Run initial health check
        health = health_check()
        if health["overall_status"] != "healthy":
            logger.warning(f"Health check warning: {health}")
        else:
            logger.info("✓ Health check passed")
            
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise RuntimeError(f"Startup failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Healthcare Search API...")


# Create FastAPI application
app = FastAPI(
    title="Healthcare Search API",
    description="Production-ready API for healthcare data semantic search",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get components
def get_components_dependency():
    """Dependency to get initialized components"""
    return get_components()


# API Routes

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Healthcare Search API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """
    Health check endpoint.
    Returns comprehensive health status of all components.
    """
    try:
        return await get_health_status()
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")


@app.post("/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    """
    Main search endpoint.
    Performs semantic search on healthcare data.
    
    Args:
        request: SearchRequest with query and optional parameters
        
    Returns:
        SearchResponse with search results and metadata
    """
    try:
        logger.info(f"Search request: {request.query[:100]}...")
        
        result = await search_healthcare_data(
            query=request.query,
            index_name=request.index_name,
            max_results=request.max_results,
            include_metadata=request.include_metadata
        )
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")


@app.get("/indexes")
async def indexes_endpoint():
    """
    Get available indexes and their metadata.
    
    Returns:
        Dictionary with available indexes information
    """
    try:
        return await get_available_indexes()
    except Exception as e:
        logger.error(f"Failed to get indexes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get indexes: {e}")


@app.get("/status")
async def status_endpoint(components=Depends(get_components_dependency)):
    """
    Get system status and component information.
    
    Returns:
        Dictionary with system status
    """
    try:
        status = components.get_status()
        return {
            "api_status": "operational",
            "components": status,
            "timestamp": components.initialization_time.isoformat() if components.initialization_time else None
        }
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {e}")


# Error handlers

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url.path)}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
